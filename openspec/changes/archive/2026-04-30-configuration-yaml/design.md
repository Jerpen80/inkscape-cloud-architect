## Context

The aws-auto-diagram extension currently hardcodes all layout values (margins, gaps, sizes) as module-level constants. As the extension grows, users need a way to customize these values without editing Python code. No configuration system exists yet.

## Goals / Non-Goals

**Goals:**
- Provide a YAML-based configuration system with sensible defaults
- Allow user overrides without modifying the shipped extension files
- Deep-merge user config over defaults so users only need to specify what they change

**Non-Goals:**
- GUI for editing config (users edit YAML directly)
- Runtime config reloading (config is read once per extension invocation)
- Validation schema for config values (keep it simple for now)

## Decisions

### 1. YAML format over JSON or INI
YAML is human-readable and already familiar in the cloud/DevOps space where this extension's users live. Python's PyYAML is available in Inkscape's bundled Python.

### 2. File naming: `default-config.yaml`
The default config shipped with the extension is named `default-config.yaml` to make it clear this is the baseline. The user override is simply `config.yaml`.

### 3. Override location: `~/.config/inkscape/extensions/aws-auto-diagram/config.yaml`
This follows Inkscape's existing convention of using `~/.config/inkscape/` for user customization. The path is predictable and survives extension updates.

### 4. Deep merge strategy
User config is deep-merged over defaults using a simple recursive dict merge. This means users can override a single nested value without repeating the entire structure. Example:

```yaml
# User only needs to specify what they change
document:
  margin: 40
```

### 5. Config module exposes a `load_config()` function
Returns the merged dict. Called once in `effect()` and passed to consumers. No global state.

## Risks / Trade-offs

- [PyYAML availability] → Inkscape bundles Python with PyYAML. If missing, fall back to an error message. Not worth bundling a YAML parser.
- [No validation] → Invalid config values will cause runtime errors. Acceptable for now — users who edit YAML are expected to understand the format. Can add validation later if needed.
