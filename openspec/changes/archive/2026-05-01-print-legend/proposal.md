## Why

Diagrams use color-coded borders and AWS icons to differentiate resource types, but there's no legend explaining what each color and icon means. Users unfamiliar with AWS visual conventions can't interpret the diagram. A legend makes diagrams self-documenting.

Bean: [inkscape-cloud-architect-dh4j](.beans/inkscape-cloud-architect-dh4j--print-legenda.md)

## What Changes

- Add a central legend registry (`legend.py`) where resource modules self-register their legend entries at import time
- Each existing resource module registers with category, name, symbol, layer, and optional border_key
- After all content is rendered, render a legend below the diagram on its own "Legend" layer
- Legend is dynamic: only shows entries for layers that have content (children > 0)
- Two sections: Containers (colored border + icon + name) and Resources (icon + name)
- New resource modules automatically appear in the legend by calling `register_legend()` — no legend code changes needed
- Add `layout.legend` config section for styling

## Capabilities

### New Capabilities
- `legend-rendering`: Dynamic legend with self-registering resource modules, rendered on its own layer

### Modified Capabilities
- `config-loading`: Default config gains `layout.legend` section

## Impact

- **New file**: `ica_utils/legend.py` — registry + render function
- **Config**: `default-config.yaml` gains `layout.legend` section
- **Main**: `aws-auto-diagram.py` calls legend render after content, before resize
- **All resource modules**: Each gains a `register_legend()` call (16 modules)
- **Layers**: New "Legend" layer at the top of z-order
