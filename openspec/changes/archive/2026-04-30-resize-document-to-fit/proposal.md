## Why

The SVG document is currently fixed at 800x600 regardless of content size. Diagrams with many VPCs overflow the canvas, while small diagrams waste space. The document should automatically resize to fit all rendered components.

Related task: [inkscape-cloud-architect-1c38](.beans/inkscape-cloud-architect-1c38--resize-document-to-fit-all-components.md)

## What Changes

- After all components are rendered, compute the bounding box of all elements using Inkex's `get_bbox()`
- Resize the SVG document (width, height, viewBox) to fit the content plus a configurable margin
- Read the margin value from the configuration system (see `configuration-yaml` change)

## Capabilities

### New Capabilities
- `document-resize`: Automatically resize the SVG document to fit all rendered content with configurable margin

### Modified Capabilities
<!-- None -->

## Impact

- Modified: `extensions/aws-auto-diagram/aws-auto-diagram.py` (add resize step after rendering)
- Depends on: `configuration-yaml` change (for margin config value)
