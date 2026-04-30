## ADDED Requirements

### Requirement: Legend registry
Resource modules SHALL self-register legend entries via `register_legend()` at import time.

#### Scenario: Module registers at import
- **WHEN** a resource module is imported
- **THEN** it SHALL call `register_legend()` with category, name, symbol, layer, and optional border_key

#### Scenario: New module auto-registers
- **WHEN** a new resource module is added and calls `register_legend()`
- **THEN** its entry SHALL appear in the legend without modifying legend rendering code

### Requirement: Dynamic legend filtering
The legend SHALL only show entries for resource types actually present in the diagram.

#### Scenario: Layer with content
- **WHEN** a registered layer has children (rendered content)
- **THEN** its legend entry SHALL be included

#### Scenario: Layer without content
- **WHEN** a registered layer has no children
- **THEN** its legend entry SHALL be excluded

### Requirement: Legend sections
The legend SHALL have two sections: Containers and Resources.

#### Scenario: Container entry rendering
- **WHEN** a container legend entry is rendered
- **THEN** it SHALL display a small colored rectangle (border color from theme) with icon and name

#### Scenario: Resource entry rendering
- **WHEN** a resource legend entry is rendered
- **THEN** it SHALL display the resource icon with name text

### Requirement: Legend layer
The legend SHALL be rendered on a dedicated "Legend" layer.

#### Scenario: Legend layer z-order
- **WHEN** the extension creates layers
- **THEN** the "Legend" layer SHALL be created at the top of z-order

### Requirement: Legend positioning
The legend SHALL be positioned below all other diagram content.

#### Scenario: Legend below content
- **WHEN** the legend is rendered
- **THEN** it SHALL appear below all other content with a configurable gap (`layout.legend.top_spacing`)

### Requirement: Legend can be disabled
The legend SHALL be disableable via config.

#### Scenario: Legend disabled
- **WHEN** `layout.legend.enabled` is `false`
- **THEN** no legend SHALL be rendered
