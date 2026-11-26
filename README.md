# Kasem Adra

Trilingual static site. Edit the biography and page templates in `build.py`, existing articles in `_posts/`, and research metadata in `_publications/`.

This site uses root-relative URLs. Use the account's user-site repository, `Kasem-Adra/kasem-adra.github.io`, for the first deployment. Select GitHub Actions in Pages settings, then run the Deploy website to GitHub Pages workflow. Leave indexing disabled during review. Once the custom domain kasemadra.com serves the site over HTTPS, run the workflow again with indexing enabled.

Locally run `python3 build.py`; set `SITE_PUBLIC=1` only when building for the official domain.
