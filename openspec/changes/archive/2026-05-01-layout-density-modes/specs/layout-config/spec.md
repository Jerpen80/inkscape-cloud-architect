## MODIFIED Requirements

### Requirement: Layout values from resolved density mode
All layout spacing values SHALL come from the resolved density mode preset rather than flat top-level defaults.

#### Scenario: Spaced mode active
- **WHEN** the spaced layout mode is resolved
- **THEN** `config["layout"]["account"]`, `config["layout"]["vpc"]`, `config["layout"]["subnet"]`, and all other layout sub-sections SHALL contain the spaced preset values

#### Scenario: Dense mode active
- **WHEN** the dense layout mode is resolved
- **THEN** `config["layout"]["account"]`, `config["layout"]["vpc"]`, `config["layout"]["subnet"]`, and all other layout sub-sections SHALL contain the dense preset values (matching previous defaults)

#### Scenario: Renderers unchanged
- **WHEN** any renderer reads from `config["layout"]`
- **THEN** it SHALL find the same key structure as before (e.g., `config["layout"]["vpc"]["padding"]["top"]`), regardless of which mode is active
