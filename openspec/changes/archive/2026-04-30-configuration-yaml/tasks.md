## 1. Default Config File

- [x] 1.1 Create `extensions/aws-auto-diagram/default-config.yaml` with `document.margin: 20`

## 2. Config Module

- [x] 2.1 Create `extensions/aws-auto-diagram/ica_utils/config.py` with `load_config(extension_dir)` function
- [x] 2.2 Implement default config loading from `default-config.yaml`
- [x] 2.3 Implement user override loading from `~/.config/inkscape/extensions/aws-auto-diagram/config.yaml`
- [x] 2.4 Implement recursive deep-merge (user values override defaults)

## 3. Extension Integration

- [x] 3.1 Load config in `aws-auto-diagram.py` `effect()` before rendering
