## 1. Data Parsing

- [x] 1.1 Add EC2 instance parsing to `cloudia_parser.py` — parse `ec2-describe-instances.json`, filter running only, return instances with `subnet_id`, `vpc_id`, `name`, `instance_type`, `state`
- [x] 1.2 Update `parse_region` return signature to include instances (third return value)

## 2. Symbol Import

- [x] 2.1 Generalize `import_defs_from_external_file_in_document` to accept a list of symbol files
- [x] 2.2 Add `AWS-Resource-compute-light.svg` to the import list

## 3. Layout: Variable Row Heights

- [x] 3.1 Update Grid to accept `row_heights` (list) instead of uniform `cell_height`
- [x] 3.2 Update `cell_position` to sum preceding row heights for y offset
- [x] 3.3 Update `bounds` to use sum of row heights

## 4. EC2 Rendering

- [x] 4.1 Create `resource_ec2.py` with function to render an instance card (icon centered, name centered, type centered, no border)
- [x] 4.2 Add EC2 config section to `default-config.yaml` under `layout.ec2`

## 5. Integration

- [x] 5.1 Compute per-row heights based on max instance count across cells in each row
- [x] 5.2 Pass instances to `render_vpc_with_subnets`, render EC2 cards after drawing each subnet
- [x] 5.3 Create "EC2" layer and pass to EC2 renderer
- [x] 5.4 Update `aws-auto-diagram.py` to pass instances from parser to VPC renderer

## 6. Verify

- [x] 6.1 Run headless with us-east-2 data and verify EC2 instances appear inside subnets
