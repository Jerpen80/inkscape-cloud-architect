# Match template visual style

## Summary

Align the generated diagram output with the hand-crafted templates by fixing icon scale, sizing, and label positioning. The current icons are 11px — the templates render them at 40px. Subnet cells need to grow to accommodate the larger icons.

## Motivation

- Icons are scaled to 11px but templates use 40px — looks completely different
- Text baseline doesn't align with icon center as in templates
- Subnet cell height (35px) is too small for 40px icons
- Generated output should look like it was made with the same templates

## Scope

### In scope
- Fix icon scale to render at 40px (matching template)
- Increase subnet cell height to fit icon + padding
- Increase VPC padding top to fit larger VPC icon + label
- Align text baseline with icon center
- Update text_utils RENDER_MARGIN and layout constants

### Out of scope
- Switching to mm-based document units (we stay in px)
- Changing colors or stroke widths (already match)

## Files

| Action | File |
|--------|------|
| Update | `extensions/aws-auto-diagram/ica_utils/resource_vpc.py` |
| Create | `openspec/changes/match-template-style/specs/visual-style/spec.md` |
