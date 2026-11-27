# Kasem Adra

Trilingual static website for Kasem Adra. The source of truth is the content and build code in the repository; `dist/` contains the static assets and generated site output.

## Build and validate locally

```bash
python3 build.py
SITE_PUBLIC=1 python3 build.py
python3 tests/validate_site.py
```

The public validation command must be run after building with `SITE_PUBLIC=1`. It checks the three language versions, HTML attributes, canonical URLs, hreflang alternates, Open Graph and Twitter metadata, robots directives, internal links, JSON-LD entities, the research archive, the featured article, the hero image and the XML sitemap.

## Deployment

- Pull requests to `main` run the public build and the complete validation suite.
- Every push to `main` builds the indexable site, validates the generated output, and only then deploys it to GitHub Pages.
- The manual `Deploy website to GitHub Pages` workflow remains available for previews. Its `indexable` option defaults to `false`; enable it only when intentionally publishing to the official HTTPS domain.

The site uses the custom domain `kasemadra.com`. Keep the language selector at the root URL and do not add a Baniyas historical archive to this website.
