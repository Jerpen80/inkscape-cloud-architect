### Requirement: Document resizes to fit content
After all components are rendered, the extension SHALL shift all content so the bounding box top-left is at (margin, margin), then resize the SVG document to fit.

#### Scenario: Document with rendered components
- **WHEN** one or more components have been rendered
- **THEN** all top-level layers SHALL be translated so the content bounding box starts at (margin, margin)
- **THEN** the document width and height SHALL equal the content bounding box dimensions plus twice the configured margin (margin on each side)

#### Scenario: viewBox matches dimensions
- **WHEN** the document is resized
- **THEN** the viewBox attribute SHALL be set to `0 0 <width> <height>` matching the new document dimensions

### Requirement: Margin is configurable
The margin applied around content SHALL be read from the config system at `document.margin`.

#### Scenario: Default margin applied
- **WHEN** no user config override exists
- **THEN** the default margin of 20px SHALL be applied on all sides

#### Scenario: Custom margin applied
- **WHEN** the user config sets `document.margin: 40`
- **THEN** 40px of margin SHALL be applied on all sides

### Requirement: Graceful handling of empty document
The resize logic SHALL handle the case where no elements are rendered.

#### Scenario: No data loaded
- **WHEN** no VPCs or subnets are rendered (empty bounding box)
- **THEN** the document dimensions SHALL remain unchanged
