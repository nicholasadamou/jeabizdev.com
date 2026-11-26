# <img src="public/brand/mark.svg" alt="" height="64" /> JEA BizDev Consulting

<img src="public/brand/social.png" alt="JEA BizDev Consulting — Cross-border deals. Lasting value." width="1280" />

[![CI](https://img.shields.io/github/actions/workflow/status/nicholasadamou/jeabizdev.com/ci.yml?branch=master&label=CI&labelColor=111F38)](https://github.com/nicholasadamou/jeabizdev.com/actions/workflows/ci.yml)
![Astro](https://img.shields.io/badge/Astro-2563EB?labelColor=111F38&logoColor=FFFFFF&logo=astro)
![React](https://img.shields.io/badge/React-2563EB?labelColor=111F38&logoColor=FFFFFF&logo=react)
![TypeScript](https://img.shields.io/badge/TypeScript-2563EB?labelColor=111F38&logoColor=FFFFFF&logo=typescript)
![Bun](https://img.shields.io/badge/Bun-2563EB?labelColor=111F38&logoColor=FFFFFF&logo=bun)
![Flox](https://img.shields.io/badge/Flox-2563EB?labelColor=111F38&logoColor=FFFFFF)
[![License](https://img.shields.io/badge/License-PolyForm_Shield_1.0.0-2563EB?labelColor=111F38)](LICENSE)

JEA’s website for biotech and biopharma advisory work. Visitors can explore
partnering assets, read transaction announcements, and send an inquiry.

[Visit JEA](https://www.jeabizdev.com)

## Getting started

```sh
flox activate
bun install --frozen-lockfile
bun run dev
```

## Documentation

- [Documentation](docs/README.md): visitor guides, content editing, and inquiry setup.
- [Getting started](docs/development/setup.md): locked tools, local previews, and browser setup.
- [Local verification](docs/development/quality.md): formatting, types, tests, and production checks.
- [Brand assets](docs/brand.md): the DNA mark, palette, photography, and attribution.
- [Releases](docs/development/releases.md): CI-verified tags and published archives.

## Local verification

Run `bun run check` inside Flox. The shared gate checks formatting, Markdown and
Mermaid, source budgets, workflows, types, unit tests, the production build,
links, and desktop/mobile browser journeys. Install Chromium as described in
[development setup](docs/development/setup.md).

The pre-commit hook and GitHub Actions run the same gate.

## License

Copyright © 2026 Nicholas Adamou.

The project is licensed under [PolyForm Shield License 1.0.0](LICENSE), with Nicholas Adamou as
the holder.
