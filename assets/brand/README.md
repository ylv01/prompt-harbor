# PromptHarbor brand

Original mark: three routes converge above a curved harbor. The branches represent
different tasks/models; the harbor represents the main conversation that brings
their work together. It is deliberately abstract rather than a provider mascot.

| Asset | Purpose |
|---|---|
| logo.svg / logo.png | Transparent standalone mark, 256 × 256 |
| logo-dark.svg / logo-dark.png | Light teal mark for dark backgrounds |
| avatar.png | Square avatar, 512 × 512 |
| hero.svg / hero.png | README wordmark and positioning, 1200 × 340 |
| social-preview.png / .svg | GitHub social preview, 1280 × 640 |

Palette: deep navy `#132D38`, harbor teal `#087F8C`, signal coral `#F07167`,
paper `#F5F8F6`. Preserve a clear space of roughly one node around the mark.
Use the transparent light variant on dark surfaces and avoid recoloring the
signal dot to match model providers. All original artwork is Apache-2.0.

Regenerate with `python scripts/build_brand.py` after installing Pillow as a
development-only dependency. SVGs are editable, self-contained vector files with
no remote fonts or scripts. Set PROMPTHARBOR_FONT / PROMPTHARBOR_FONT_BOLD to local
font files to control PNG typography. System font files are not redistributed.

Badges are generated locally from real project metadata. They are not remote CI
status claims, popularity metrics, or endorsement marks.
