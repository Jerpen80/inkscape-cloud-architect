import json
import os
from ica_utils.icalog import debug


def _get_name(resource, fallback_id, cidr):
    tags = resource.get("Tags", [])
    name_tag = next((t["Value"] for t in tags if t["Key"] == "Name"), None)
    if name_tag:
        return f"{name_tag} ({cidr})"
    return f"{fallback_id} ({cidr})"


def _load_json(filepath):
    if not os.path.isfile(filepath):
        debug(f"File not found: {filepath}")
        return None
    with open(filepath, 'r') as f:
        return json.load(f)


def parse_region(data_dir, region):
    region_dir = os.path.join(data_dir, region)

    if not os.path.isdir(region_dir):
        debug(f"Region directory not found: {region_dir}")
        return [], [], [], [], [], [], [], [], [], [], []

    vpcs = []
    vpc_data = _load_json(os.path.join(region_dir, "ec2-describe-vpcs.json"))
    if vpc_data:
        for vpc in vpc_data.get("Vpcs", []):
            cidr = vpc.get("CidrBlock", "")
            vpcs.append({
                "type": "vpc",
                "name": _get_name(vpc, vpc.get("VpcId", ""), cidr),
                "vpc_id": vpc.get("VpcId", ""),
                "cidr": cidr,
                "is_default": vpc.get("IsDefault", False),
            })

    subnets = []
    subnet_data = _load_json(os.path.join(region_dir, "ec2-describe-subnets.json"))
    if subnet_data:
        for subnet in subnet_data.get("Subnets", []):
            cidr = subnet.get("CidrBlock", "")
            subnets.append({
                "type": "subnet",
                "name": _get_name(subnet, subnet.get("SubnetId", ""), cidr),
                "subnet_id": subnet.get("SubnetId", ""),
                "vpc_id": subnet.get("VpcId", ""),
                "cidr": cidr,
                "az": subnet.get("AvailabilityZone", ""),
                "is_public": subnet.get("MapPublicIpOnLaunch", False),
            })

    instances = []
    instance_data = _load_json(os.path.join(region_dir, "ec2-describe-instances.json"))
    if instance_data:
        for reservation in instance_data.get("Reservations", []):
            for inst in reservation.get("Instances", []):
                state = inst.get("State", {}).get("Name", "")
                if state != "running":
                    continue
                tags = inst.get("Tags", [])
                name = next((t["Value"] for t in tags if t["Key"] == "Name"), inst.get("InstanceId", ""))
                instances.append({
                    "type": "ec2",
                    "name": name,
                    "instance_id": inst.get("InstanceId", ""),
                    "instance_type": inst.get("InstanceType", ""),
                    "subnet_id": inst.get("SubnetId", ""),
                    "vpc_id": inst.get("VpcId", ""),
                    "state": state,
                })

    load_balancers = []
    lb_data = _load_json(os.path.join(region_dir, "elbv2-describe-load-balancers.json"))
    if lb_data:
        for lb in lb_data.get("LoadBalancers", []):
            subnet_ids = [az.get("SubnetId", "") for az in lb.get("AvailabilityZones", []) if az.get("SubnetId")]
            load_balancers.append({
                "type": "load_balancer",
                "name": lb.get("LoadBalancerName", ""),
                "lb_type": lb.get("Type", ""),
                "scheme": lb.get("Scheme", ""),
                "vpc_id": lb.get("VpcId", ""),
                "subnet_ids": subnet_ids,
            })

    db_instances = []

    # RDS instances — exact subnet resolution via AZ + DBSubnetGroup
    rds_data = _load_json(os.path.join(region_dir, "rds-describe-db-instances.json"))
    if rds_data:
        for db in rds_data.get("DBInstances", []):
            az = db.get("AvailabilityZone", "")
            subnet_group = db.get("DBSubnetGroup", {})
            vpc_id = subnet_group.get("VpcId", "")
            # Find the subnet in the group that matches this instance's AZ
            subnet_id = ""
            for sg_subnet in subnet_group.get("Subnets", []):
                sg_az = sg_subnet.get("SubnetAvailabilityZone", {}).get("Name", "")
                if sg_az == az:
                    subnet_id = sg_subnet.get("SubnetIdentifier", "")
                    break
            if subnet_id:
                db_instances.append({
                    "type": "rds",
                    "db_type": "rds",
                    "name": db.get("DBInstanceIdentifier", ""),
                    "engine": db.get("Engine", ""),
                    "instance_class": db.get("DBInstanceClass", ""),
                    "subnet_id": subnet_id,
                    "vpc_id": vpc_id,
                })

    # ElastiCache clusters — AZ heuristic for subnet placement
    ec_data = _load_json(os.path.join(region_dir, "elasticache-describe-cache-clusters.json"))
    if ec_data:
        # Build AZ → non-public subnets lookup from already-parsed subnets
        az_private_subnets = {}
        for s in subnets:
            if not s.get("is_public", False):
                az_private_subnets.setdefault(s["az"], []).append(s)

        for cluster in ec_data.get("CacheClusters", []):
            az = cluster.get("PreferredAvailabilityZone", "")
            matching = az_private_subnets.get(az, [])
            if matching:
                target_subnet = matching[0]
                db_instances.append({
                    "type": "elasticache",
                    "db_type": "elasticache",
                    "name": cluster.get("CacheClusterId", ""),
                    "engine": cluster.get("Engine", ""),
                    "instance_class": cluster.get("CacheNodeType", ""),
                    "subnet_id": target_subnet["subnet_id"],
                    "vpc_id": target_subnet["vpc_id"],
                })

    eks_clusters = []
    eks_list = _load_json(os.path.join(region_dir, "eks-list-clusters.json"))
    if eks_list:
        for cluster_name in eks_list.get("clusters", []):
            describe_path = os.path.join(region_dir, "eks-describe-cluster", cluster_name)
            cluster_data = _load_json(describe_path)
            if not cluster_data:
                debug(f"EKS describe file not found for cluster: {cluster_name}")
                continue
            cluster = cluster_data.get("cluster", {})
            if cluster.get("status", "") != "ACTIVE":
                continue
            vpc_config = cluster.get("resourcesVpcConfig", {})
            eks_clusters.append({
                "type": "eks",
                "name": cluster.get("name", ""),
                "version": cluster.get("version", ""),
                "vpc_id": vpc_config.get("vpcId", ""),
                "subnet_ids": vpc_config.get("subnetIds", []),
                "status": cluster.get("status", ""),
            })

    vpc_lambdas = []
    non_vpc_lambdas = []
    lambda_data = _load_json(os.path.join(region_dir, "lambda-list-functions.json"))
    if lambda_data:
        for fn in lambda_data.get("Functions", []):
            vpc_config = fn.get("VpcConfig", {})
            vpc_id = vpc_config.get("VpcId", "")
            subnet_ids = vpc_config.get("SubnetIds", [])
            name = fn.get("FunctionName", "")
            runtime = fn.get("Runtime", "")
            if vpc_id and subnet_ids:
                vpc_lambdas.append({
                    "type": "lambda",
                    "name": name,
                    "runtime": runtime,
                    "vpc_id": vpc_id,
                    "subnet_ids": subnet_ids,
                })
            else:
                non_vpc_lambdas.append({
                    "type": "lambda",
                    "name": name,
                    "runtime": runtime,
                })

    nat_gateways = []
    ni_data = _load_json(os.path.join(region_dir, "ec2-describe-network-interfaces.json"))
    if ni_data:
        for ni in ni_data.get("NetworkInterfaces", []):
            if ni.get("InterfaceType", "") == "nat_gateway":
                desc = ni.get("Description", "")
                # Extract NAT gateway ID from "Interface for NAT Gateway nat-..."
                nat_id = desc.split("NAT Gateway ")[-1] if "NAT Gateway " in desc else desc
                nat_gateways.append({
                    "type": "nat_gateway",
                    "name": nat_id,
                    "nat_gateway_id": nat_id,
                    "subnet_id": ni.get("SubnetId", ""),
                    "vpc_id": ni.get("VpcId", ""),
                })

    auto_scaling_groups = []
    asg_data = _load_json(os.path.join(region_dir, "autoscaling-describe-auto-scaling-groups.json"))
    if asg_data:
        for asg in asg_data.get("AutoScalingGroups", []):
            asg_instances = [i.get("InstanceId", "") for i in asg.get("Instances", []) if i.get("LifecycleState") == "InService"]
            if not asg_instances:
                continue
            subnet_ids = [s.strip() for s in asg.get("VPCZoneIdentifier", "").split(",") if s.strip()]
            # Derive VPC from first subnet match
            vpc_id = ""
            for s in subnets:
                if s["subnet_id"] in subnet_ids:
                    vpc_id = s["vpc_id"]
                    break
            auto_scaling_groups.append({
                "type": "asg",
                "name": asg.get("AutoScalingGroupName", ""),
                "instance_ids": asg_instances,
                "subnet_ids": subnet_ids,
                "min_size": asg.get("MinSize", 0),
                "max_size": asg.get("MaxSize", 0),
                "desired_capacity": asg.get("DesiredCapacity", 0),
                "vpc_id": vpc_id,
            })

    dynamodb_tables = []
    ddb_data = _load_json(os.path.join(region_dir, "dynamodb-list-tables.json"))
    if ddb_data:
        for table_name in ddb_data.get("TableNames", []):
            dynamodb_tables.append({
                "type": "dynamodb",
                "name": table_name,
            })

    return vpcs, subnets, instances, load_balancers, db_instances, eks_clusters, vpc_lambdas, non_vpc_lambdas, nat_gateways, auto_scaling_groups, dynamodb_tables


def parse_global_services(data_dir):
    """Scan region subdirectories for global service data (S3, CloudFront, Route 53).

    Returns dict with global data, e.g. {"s3_buckets": [...], "cloudfront_distributions": [...],
    "route53_public_zones": [...], "route53_private_zones": [...]}, or empty dict if none found.
    """
    s3_buckets = []
    cloudfront_distributions = []
    route53_public_zones = []
    route53_private_zones = []

    if os.path.isdir(data_dir):
        for entry in sorted(os.listdir(data_dir)):
            region_dir = os.path.join(data_dir, entry)
            if not os.path.isdir(region_dir):
                continue

            # S3 — global API call, typically in us-east-1
            if not s3_buckets:
                s3_data = _load_json(os.path.join(region_dir, "s3-list-buckets.json"))
                if s3_data:
                    for bucket in s3_data.get("Buckets", []):
                        s3_buckets.append({
                            "type": "s3",
                            "name": bucket.get("Name", ""),
                        })

            # CloudFront — global API, typically in us-east-1
            if not cloudfront_distributions:
                cf_data = _load_json(os.path.join(region_dir, "cloudfront-list-distributions.json"))
                if cf_data:
                    for dist in cf_data.get("DistributionList", {}).get("Items", []):
                        aliases = dist.get("Aliases", {}).get("Items", [])
                        cloudfront_distributions.append({
                            "type": "cloudfront",
                            "distribution_id": dist.get("Id", ""),
                            "domain_name": dist.get("DomainName", ""),
                            "aliases": aliases,
                            "comment": dist.get("Comment", ""),
                            "status": dist.get("Status", ""),
                        })

            # Route 53 — global API, typically in us-east-1
            if not route53_public_zones and not route53_private_zones:
                r53_data = _load_json(os.path.join(region_dir, "route53-list-hosted-zones.json"))
                if r53_data:
                    for zone in r53_data.get("HostedZones", []):
                        name = zone.get("Name", "").rstrip(".")
                        is_private = zone.get("Config", {}).get("PrivateZone", False)
                        zone_entry = {
                            "type": "route53",
                            "zone_id": zone.get("Id", "").replace("/hostedzone/", ""),
                            "name": name,
                            "record_count": zone.get("ResourceRecordSetCount", 0),
                            "is_private": is_private,
                        }
                        if is_private:
                            route53_private_zones.append(zone_entry)
                        else:
                            route53_public_zones.append(zone_entry)

    result = {}
    if s3_buckets:
        result["s3_buckets"] = s3_buckets
    if cloudfront_distributions:
        result["cloudfront_distributions"] = cloudfront_distributions
    if route53_public_zones:
        result["route53_public_zones"] = route53_public_zones
    if route53_private_zones:
        result["route53_private_zones"] = route53_private_zones
    return result


def parse_all_regions(data_dir):
    """Scan all region subdirectories, parse each, filter out regions with only default VPCs.

    Returns list of entries. Real regions are tuples:
        (region_name, vpcs, subnets, instances, load_balancers, db_instances, eks_clusters, vpc_lambdas)
    Global region (if any) is:
        ("Global", {"s3_buckets": [...], "lambdas": [...]})
    Global is prepended as the first entry.
    """
    if not os.path.isdir(data_dir):
        debug(f"Data directory not found: {data_dir}")
        return []

    results = []
    all_non_vpc_lambdas = []

    # Prepend Global region placeholder — filled after scanning all regions
    global_data = parse_global_services(data_dir)

    for entry in sorted(os.listdir(data_dir)):
        region_dir = os.path.join(data_dir, entry)
        if not os.path.isdir(region_dir):
            continue
        vpcs, subnets, instances, load_balancers, db_instances, eks_clusters, vpc_lambdas, non_vpc_lambdas, nat_gateways, auto_scaling_groups, dynamodb_tables = parse_region(data_dir, entry)

        # Collect non-VPC lambdas from all regions
        all_non_vpc_lambdas.extend(non_vpc_lambdas)

        if not vpcs:
            continue
        # Filter: skip default-only regions unless they have resources
        has_non_default = any(not v.get("is_default", False) for v in vpcs)
        if not has_non_default:
            has_resources = instances or load_balancers or db_instances or eks_clusters or vpc_lambdas or nat_gateways or auto_scaling_groups
            if not has_resources:
                debug(f"Skipping region {entry}: only empty default VPCs")
                continue
        results.append((entry, vpcs, subnets, instances, load_balancers, db_instances, eks_clusters, vpc_lambdas, nat_gateways, auto_scaling_groups, dynamodb_tables))

    # Add non-VPC lambdas to global data
    if all_non_vpc_lambdas:
        global_data["lambdas"] = all_non_vpc_lambdas

    # Prepend Global region if any global data exists
    if global_data:
        results.insert(0, ("Global", global_data))

    return results
