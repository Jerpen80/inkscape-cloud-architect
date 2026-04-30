## 1. Config Defaults

- [x] 1.1 Add `vpc` and `subnet` sections to `default-config.yaml` with current hardcoded values

## 2. Replace Constants with Config Lookups

- [x] 2.1 Replace spacing constants in `resource_vpc.py` with `inkdoc.config` lookups and remove the old constants
- [x] 2.2 Replace `resource_vpc.VPC_GAP` in `aws-auto-diagram.py` with `self.config["vpc"]["gap"]`

## 3. Verify

- [x] 3.1 Run headless extension and confirm output is unchanged
