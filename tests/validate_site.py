#!/usr/bin/env python3
"""Validate the generated public site: HTML metadata, crawlability, links and structured data."""

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path("dist")
ORIGIN = "https://kasemadra.com"
HOST = "kasemadra.com"
LANGS = ("en", "ar", "fr")
ROUTES = (
    "/",
    "/about/",
    "/projects/",
    "/projects/local-assistant/",
    "/publications/",
    "/publications/aco-llm/",
    "/publications/aco-llm-results/",
    "/blog/",
    "/blog/checking-work/",
    "/blog/arabic-calligraphy/",
    "/blog/local-ai-agent-reliability/",
    "/archive/",
)
ERRORS = []


def fail(message):
    ERRORS.append(message)


class PageAudit(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.source = source
        self.html_attrs = {}
        self.meta = {}
        self.canonicals = []
        self.alternates = {}
        self.images = []
        self.local_refs = []
        self.jsonld = []
        self._jsonld_buffer = None
        self._title_depth = 0
        self.title_text = []

    def handle_starttag(self, tag, attrs):
        names = [name for name, _ in attrs if name]
        duplicates = sorted({name for name in names if names.count(name) > 1})
        if duplicates:
            fail(f"{self.source}: duplicate HTML attributes on <{tag}>: {duplicates}")

        values = dict(attrs)
        if tag == "html":
            self.html_attrs = values

        if tag == "title":
            self._title_depth += 1

        if tag == "meta":
            key = values.get("name") or values.get("property")
            if key:
                self.meta.setdefault(key.lower(), []).append(values.get("content"))

        if tag == "link":
            rel = set((values.get("rel") or "").lower().split())
            href = values.get("href")
            if "canonical" in rel:
                self.canonicals.append(href)
            if "alternate" in rel and values.get("hreflang"):
                lang = values["hreflang"].lower()
                if lang in self.alternates:
                    fail(f"{self.source}: duplicate hreflang={lang}")
                self.alternates[lang] = href
            if href:
                self.local_refs.append(href)

        if tag == "a" and values.get("href"):
            self.local_refs.append(values["href"])

        if tag in ("img", "source") and values.get("src"):
            self.local_refs.append(values["src"])

        if tag == "img":
            self.images.append(values)
            if "alt" not in values or not (values.get("alt") or "").strip():
                fail(f"{self.source}: image is missing meaningful alt text")

        if tag == "script":
            if values.get("src"):
                self.local_refs.append(values["src"])
            if (values.get("type") or "").lower() == "application/ld+json":
                self._jsonld_buffer = []

    def handle_endtag(self, tag):
        if tag == "title" and self._title_depth:
            self._title_depth -= 1
        if tag == "script" and self._jsonld_buffer is not None:
            raw = "".join(self._jsonld_buffer).strip()
            try:
                self.jsonld.append(json.loads(raw))
            except json.JSONDecodeError as exc:
                fail(f"{self.source}: invalid JSON-LD: {exc}")
            self._jsonld_buffer = None

    def handle_data(self, data):
        if self._title_depth:
            self.title_text.append(data)
        if self._jsonld_buffer is not None:
            self._jsonld_buffer.append(data)


def parse_page(path):
    source = path.read_text(encoding="utf-8")
    parser = PageAudit(path.as_posix())
    try:
        parser.feed(source)
        parser.close()
    except Exception as exc:
        fail(f"{path}: HTML parser failed: {exc}")
    return source, parser


def page_path(lang, route):
    return ROOT / lang / route.strip("/") / "index.html" if route != "/" else ROOT / lang / "index.html"


def flatten_schemas(parser):
    nodes = []
    for value in parser.jsonld:
        if isinstance(value, dict) and isinstance(value.get("@graph"), list):
            nodes.extend(value["@graph"])
        elif isinstance(value, dict):
            nodes.append(value)
    return nodes


def check_local_reference(reference, source):
    if not reference:
        return
    parts = urlsplit(reference)
    if parts.scheme and parts.scheme not in ("http", "https"):
        return
    if parts.netloc and parts.netloc.lower() not in (HOST, "www." + HOST):
        return
    if not parts.path:
        return
    path = unquote(parts.path)
    if not path.startswith("/"):
        return
    target = ROOT / path.lstrip("/")
    if path.endswith("/") or target.is_dir() or (not target.exists() and not target.suffix):
        target = target / "index.html"
    if not target.is_file():
        fail(f"{source}: broken local URL {reference} (expected {target})")


def check_common_metadata(path, parser):
    source = path.as_posix()
    if len(parser.canonicals) != 1 or not parser.canonicals[0]:
        fail(f"{source}: expected exactly one canonical link")

    robots = parser.meta.get("robots", [])
    if len(robots) != 1 or robots[0] != "index,follow":
        fail(f"{source}: public page must have one robots=index,follow directive")

    descriptions = parser.meta.get("description", [])
    if len(descriptions) != 1 or not (descriptions[0] or "").strip():
        fail(f"{source}: missing or duplicate meta description")

    og_images = parser.meta.get("og:image", [])
    if len(og_images) != 1 or not og_images[0]:
        fail(f"{source}: expected exactly one Open Graph image")
    elif "<" in og_images[0] or ">" in og_images[0]:
        fail(f"{source}: malformed og:image content attribute: {og_images[0]}")

    twitter_cards = parser.meta.get("twitter:card", [])
    if len(twitter_cards) != 1 or twitter_cards[0] != "summary_large_image":
        fail(f"{source}: expected one valid Twitter summary_large_image card")

    required_social = (
        "og:title", "og:description", "og:url", "og:type", "og:locale",
        "og:image:alt", "twitter:title", "twitter:description",
        "twitter:image", "twitter:image:alt",
    )
    for key in required_social:
        values = parser.meta.get(key, [])
        if len(values) != 1 or not (values[0] or "").strip():
            fail(f"{source}: expected exactly one non-empty {key} metadata value")

    if parser.meta.get("og:url") != parser.canonicals:
        fail(f"{source}: og:url must match the canonical URL")
    if parser.meta.get("twitter:title") != parser.meta.get("og:title"):
        fail(f"{source}: Twitter and Open Graph titles must match")
    if parser.meta.get("twitter:description") != parser.meta.get("og:description"):
        fail(f"{source}: Twitter and Open Graph descriptions must match")
    if parser.meta.get("twitter:image") != parser.meta.get("og:image"):
        fail(f"{source}: Twitter and Open Graph images must match")

    if not parser.title_text or not "".join(parser.title_text).strip():
        fail(f"{source}: missing page title")

    if not parser.jsonld:
        fail(f"{source}: missing JSON-LD structured data")

    for reference in parser.local_refs:
        check_local_reference(reference, source)

    for key in ("og:image", "twitter:image"):
        for reference in parser.meta.get(key, []):
            check_local_reference(reference, source)


def check_localized_page(lang, route):
    path = page_path(lang, route)
    if not path.is_file():
        fail(f"Missing localized page: {path}")
        return None

    source, parser = parse_page(path)
    check_common_metadata(path, parser)

    expected_canonical = ORIGIN + f"/{lang}" + route
    if parser.canonicals != [expected_canonical]:
        fail(f"{path}: canonical should be {expected_canonical}, got {parser.canonicals}")

    expected_alternates = {
        other: ORIGIN + f"/{other}" + route for other in LANGS
    }
    expected_alternates["x-default"] = ORIGIN + "/"
    if parser.alternates != expected_alternates:
        fail(f"{path}: incorrect hreflang set: {parser.alternates}")

    html_lang = (parser.html_attrs.get("lang") or "").lower()
    if html_lang != lang:
        fail(f"{path}: html lang should be {lang}, got {html_lang!r}")
    direction = parser.html_attrs.get("dir")
    if lang == "ar" and direction != "rtl":
        fail(f"{path}: Arabic document must use dir=rtl")
    if lang != "ar" and direction not in (None, "ltr"):
        fail(f"{path}: non-Arabic document must use left-to-right direction")

    if re.search(r'<meta\s+name=["\']robots["\']\s+content=["\'][^"\']*noindex', source, re.I):
        fail(f"{path}: indexable page contains noindex")

    expected_og_type = (
        "profile" if route == "/about/" else
        "article" if (route.startswith("/blog/") and route != "/blog/") or route in (
            "/publications/aco-llm/", "/publications/aco-llm-results/"
        ) else
        "website"
    )
    if parser.meta.get("og:type") != [expected_og_type]:
        fail(f"{path}: expected og:type={expected_og_type}")

    nodes = flatten_schemas(parser)
    breadcrumb = next((node for node in nodes if node.get("@type") == "BreadcrumbList"), None)
    if breadcrumb is None or not breadcrumb.get("itemListElement"):
        fail(f"{path}: missing BreadcrumbList structured data")
    elif [item.get("position") for item in breadcrumb["itemListElement"]] != list(range(1, len(breadcrumb["itemListElement"]) + 1)):
        fail(f"{path}: BreadcrumbList positions are not sequential")

    return source, parser


def main():
    if not ROOT.is_dir():
        fail("dist/ does not exist; run python3 build.py with SITE_PUBLIC=1 first")
        return

    # Audit every emitted HTML page, including root-level English aliases.
    html_files = sorted(ROOT.rglob("*.html"))
    if not html_files:
        fail("No HTML pages were generated")
    for path in html_files:
        _, parser = parse_page(path)
        check_common_metadata(path, parser)
        robots = parser.meta.get("robots", [])
        if len(robots) != 1 or robots[0] != "index,follow":
            fail(f"{path}: expected one explicit robots=index,follow directive")

    # All three language versions must have the complete, connected route set.
    for lang in LANGS:
        localized = sorted((ROOT / lang).rglob("index.html"))
        if len(localized) != len(ROUTES):
            fail(f"{lang}: expected {len(ROUTES)} localized pages, found {len(localized)}")
        for route in ROUTES:
            check_localized_page(lang, route)

    # Root language selector and its author/site entity graph.
    root_path = ROOT / "index.html"
    if root_path.is_file():
        _, root_parser = parse_page(root_path)
        check_common_metadata(root_path, root_parser)

        # The root language selector is also the primary branded search result.
        expected_root_title = "Kasem Adra | Independent AI Researcher"
        expected_root_description = (
            "Official website of Kasem Adra (قاسم عدرا), independent AI researcher "
            "studying local language models, AI agents, task verification and ACO-LLM."
        )
        if "".join(root_parser.title_text).strip() != expected_root_title:
            fail(f"Root page title should be {expected_root_title!r}")
        for key, expected in (
            ("description", expected_root_description),
            ("og:title", expected_root_title),
            ("og:description", expected_root_description),
            ("twitter:title", expected_root_title),
            ("twitter:description", expected_root_description),
            ("twitter:image", ORIGIN + "/assets/kasem-adra-portrait.jpg"),
        ):
            if root_parser.meta.get(key) != [expected]:
                fail(f"Root page {key} metadata is inconsistent: {root_parser.meta.get(key)}")

        if root_parser.canonicals != [ORIGIN + "/"]:
            fail("Root language selector must canonicalize to https://kasemadra.com/")
        expected_root_alternates = {
            "en": ORIGIN + "/en/",
            "ar": ORIGIN + "/ar/",
            "fr": ORIGIN + "/fr/",
            "x-default": ORIGIN + "/",
        }
        if root_parser.alternates != expected_root_alternates:
            fail(f"Root language selector has incorrect hreflang links: {root_parser.alternates}")
        root_nodes = flatten_schemas(root_parser)
        website = next((x for x in root_nodes if x.get("@type") == "WebSite" and x.get("name") == "Kasem Adra"), None)
        if website is None:
            fail("Root page is missing the WebSite entity")
        elif website.get("description") != expected_root_description:
            fail("Root WebSite description does not match the search snippet")

        webpage = next((x for x in root_nodes if x.get("@type") == "WebPage" and x.get("@id") == ORIGIN + "/#webpage"), None)
        if webpage is None:
            fail("Root page is missing its connected WebPage entity")
        elif webpage.get("name") != expected_root_title or webpage.get("description") != expected_root_description:
            fail("Root WebPage name/description do not match the search metadata")

        person = next((x for x in root_nodes if x.get("@type") == "Person" and x.get("@id") == ORIGIN + "/#person"), None)
        if person is None:
            fail("Root page is missing the connected Person entity")
        else:
            same_as = person.get("sameAs", [])
            for identifier in (
                "https://orcid.org/0009-0004-7615-4978",
                "https://github.com/Kasem-Adra",
                "https://github.com/Qassemai",
                "https://www.linkedin.com/in/kasem-adra/",
                "https://qassem.net/",
                "https://x.com/QassemAdra",
                "https://www.instagram.com/qassemadra/",
            ):
                if identifier not in same_as:
                    fail(f"Person entity is missing sameAs identifier: {identifier}")
            for lang, expected_links in {
            "en": ("https://github.com/Qassemai", "https://www.instagram.com/qassemadra/"),
            "ar": ("https://github.com/Qassemai", "https://www.instagram.com/qassemadra/"),
            "fr": ("https://github.com/Qassemai", "https://www.instagram.com/qassemadra/"),
        }.items():
            profile = page_path(lang, "/about/").read_text(encoding="utf-8")
            for link in expected_links:
                if f'href="{link}"' not in profile:
                    fail(f"{lang}: author profile is missing verified identity link {link}")
        if "قاسم عدرا" not in person.get("alternateName", []):
                fail("Person entity is missing the Arabic alternate name")
            if "Qassem Adra" not in person.get("alternateName", []):
                fail("Person entity is missing the documented alternate Latin transliteration")
            if person.get("name") != "Kasem Adra":
                fail("Person entity must use Kasem Adra as the canonical name")
        if website is not None and website.get("alternateName") != ["قاسم عدرا"]:
            fail("WebSite entity must use the canonical site name and Arabic alternate name only")

    # Encyclopedic profile, research archive and featured article.
    for lang in LANGS:
        about = page_path(lang, "/about/").read_text(encoding="utf-8")
        about_nodes = flatten_schemas(parse_page(page_path(lang, "/about/"))[1])
        if not any(x.get("@type") == "ProfilePage" and x.get("mainEntity", {}).get("@id") == ORIGIN + "/#person" for x in about_nodes):
            fail(f"{lang}: missing connected ProfilePage schema")
        for section_id in ("profile-facts", "biography", "research-profile", "projects-profile", "writing-profile", "identifiers"):
            if f'id="{section_id}"' not in about:
                fail(f"{lang}: missing encyclopedic profile section {section_id}")
        if 'class="profile-toc"' not in about or 'class="profile-infobox"' not in about:
            fail(f"{lang}: missing profile table of contents or infobox")
        if 'href="/' + lang + '/archive/"' not in about:
            fail(f"{lang}: profile does not link to the research archive")
        if "baniyas-revolution-2010-2025" in about.lower():
            fail(f"{lang}: forbidden Baniyas chronology link found in profile")

        archive_path = page_path(lang, "/archive/")
        archive = archive_path.read_text(encoding="utf-8")
        archive_nodes = flatten_schemas(parse_page(archive_path)[1])
        if not any(x.get("@type") == "CollectionPage" for x in archive_nodes):
            fail(f"{lang}: research archive is missing CollectionPage schema")
        if "ACO-LLM" not in archive:
            fail(f"{lang}: research archive is missing ACO-LLM records")
        if "baniyas-revolution-2010-2025" in archive.lower():
            fail(f"{lang}: Baniyas chronology must not appear in the research archive")
        if (ROOT / lang / "archive" / "baniyas-revolution-2010-2025" / "index.html").exists():
            fail(f"{lang}: forbidden Baniyas historical archive page was generated")

        for route in ("/", "/projects/", "/publications/", "/blog/"):
            path = page_path(lang, route)
            html = path.read_text(encoding="utf-8")
            if f'href="/{lang}/archive/"' not in html:
                fail(f"{lang} {route}: research archive is not internally linked")

        note_path = page_path(lang, "/blog/checking-work/")
        note = note_path.read_text(encoding="utf-8")
        note_text = re.sub(r"<[^>]+>", " ", note)
        if len(note_text.split()) < 300:
            fail(f"{lang}: verification guide is too short to serve as a substantive article")
        note_nodes = flatten_schemas(parse_page(note_path)[1])
        note_schema = next((node for node in note_nodes if node.get("@type") == "BlogPosting"), None)
        if note_schema is None:
            fail(f"{lang}: verification guide is missing BlogPosting structured data")
        else:
            if note_schema.get("dateModified") != "2026-11-27":
                fail(f"{lang}: verification guide has an incorrect modification date")
            if len(note_schema.get("citation", [])) != 2:
                fail(f"{lang}: verification guide must cite the ACO-LLM protocol and results")

        project_page = page_path(lang, "/projects/local-assistant/").read_text(encoding="utf-8")
        for term in ("gemma4:12b-it-qat", "Whisper", "Edge TTS"):
            if term not in project_page:
                fail(f"{lang}: local assistant page is missing the documented component {term}")
        if not any(term in project_page.lower() for term in ("not be described as fully offline", "لا يصح وصف مسار الصوت بالكامل", "ne faut pas décrire l’ensemble du parcours vocal")):
            fail(f"{lang}: local assistant page must disclose the external speech-synthesis path")

        protocol_page = page_path(lang, "/publications/aco-llm/").read_text(encoding="utf-8")
        plain_language_labels = {
            "en": "In plain language", "ar": "بعبارة مبسطة", "fr": "En termes simples"
        }
        if plain_language_labels[lang] not in protocol_page:
            fail(f"{lang}: protocol page is missing a plain-language summary")

        results_page = page_path(lang, "/publications/aco-llm-results/").read_text(encoding="utf-8")
        results_summary_labels = {
            "en": "In plain terms", "ar": "بعبارة مبسطة", "fr": "En termes simples"
        }
        if results_summary_labels[lang] not in results_page:
            fail(f"{lang}: results page is missing a plain-language summary")

        featured_path = page_path(lang, "/blog/local-ai-agent-reliability/")
        featured = featured_path.read_text(encoding="utf-8")
        article_titles = {
            "en": "Can We Trust a Local AI Assistant?",
            "ar": "هل يمكن الوثوق بمساعد ذكاء اصطناعي محلي؟",
            "fr": "Peut-on faire confiance à un assistant IA local ?",
        }
        if article_titles[lang] not in featured:
            fail(f"{lang}: missing localized featured article title")
        if "20.83" not in featured and "20,83" not in featured:
            fail(f"{lang}: missing primary evaluation estimate")
        if "8,064" not in featured and "8 064" not in featured:
            fail(f"{lang}: missing episode count")
        if not any(term in featured.lower() for term in ("not been peer reviewed", "غير محكّمة", "non évaluée par les pairs")):
            fail(f"{lang}: missing explicit preprint status")

        article_urls = (
            "https://doi.org/10.5281/zenodo.24488951",
            "https://doi.org/10.5281/zenodo.24549236",
            "https://deepmind.google/models/gemma/gemma-4/",
            "https://ollama.com/library/gemma4:12b-it-qat",
            "https://doi.org/10.6028/NIST.AI.600-1",
            "https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/",
            "https://arxiv.org/abs/2210.03629",
            "https://arxiv.org/abs/2303.11366",
            "https://arxiv.org/abs/2308.03688",
            "https://arxiv.org/abs/2406.12045",
            "https://arxiv.org/abs/2406.13352",
        )
        for url in article_urls:
            if url not in featured:
                fail(f"{lang}: missing featured article reference {url}")

        article_nodes = flatten_schemas(parse_page(featured_path)[1])
        article_node = next((x for x in article_nodes if x.get("@type") == "BlogPosting"), None)
        if article_node is None:
            fail(f"{lang}: missing BlogPosting structured data")
        else:
            if len(article_node.get("citation", [])) != 11:
                fail(f"{lang}: expected 11 structured article citations")
            if article_node.get("datePublished") != "2026-11-27":
                fail(f"{lang}: incorrect article publication date")
            if article_node.get("image") != ORIGIN + "/assets/local-ai-agent-reliability-hero.webp":
                fail(f"{lang}: incorrect featured article structured image")

        if featured.count('property="og:image"') != 1:
            fail(f"{lang}: featured article must have exactly one Open Graph image")
        toc_ids = set(re.findall(r'href="#(section-[0-9]+)"', featured))
        heading_ids = set(re.findall(r'id="(section-[0-9]+)"', featured))
        if not toc_ids or toc_ids != heading_ids:
            fail(f"{lang}: broken featured article table of contents")
        if 'name="robots" content="noindex"' in featured:
            fail(f"{lang}: featured article is marked noindex")
        blog_index = page_path(lang, "/blog/").read_text(encoding="utf-8")
        if f'href="/{lang}/blog/local-ai-agent-reliability/"' not in blog_index:
            fail(f"{lang}: featured article is not linked from the blog index")
        for route in ("/publications/aco-llm/", "/publications/aco-llm-results/"):
            if "local-ai-agent-reliability" not in page_path(lang, route).read_text(encoding="utf-8"):
                fail(f"{lang} {route}: missing cross-link to the featured article")

    # The article hero must be the expected WebP asset, not a missing or corrupted image.
    hero = ROOT / "assets" / "local-ai-agent-reliability-hero.webp"
    if not hero.is_file():
        fail("Missing generated featured-article hero image")
    else:
        hero_bytes = hero.read_bytes()
        if hero_bytes[:4] != b"RIFF" or hero_bytes[8:12] != b"WEBP":
            fail("Featured-article hero is not a valid WebP")
        expected_hash = "02e985665e63a3988c01ddfbfb64f546134c958898962cd9a8d9462518e1929b"
        if hashlib.sha256(hero_bytes).hexdigest() != expected_hash:
            fail("Featured-article hero image hash mismatch")

    # Robots and XML sitemap must expose exactly the intended 37 canonical URLs.
    robots_path = ROOT / "robots.txt"
    if not robots_path.is_file():
        fail("Missing robots.txt")
    else:
        robots = robots_path.read_text(encoding="utf-8")
        if "User-agent: *" not in robots or "Allow: /" not in robots or f"Sitemap: {ORIGIN}/sitemap.xml" not in robots:
            fail("robots.txt must allow crawling and point to the XML sitemap")
        if "Disallow: /" in robots:
            fail("Public robots.txt must not disallow the entire site")

    sitemap_path = ROOT / "sitemap.xml"
    if not sitemap_path.is_file():
        fail("Missing sitemap.xml")
    else:
        ns = {
            "sm": "http://www.sitemaps.org/schemas/sitemap/0.9",
            "xhtml": "http://www.w3.org/1999/xhtml",
        }
        try:
            sitemap = ET.parse(sitemap_path).getroot()
            url_nodes = sitemap.findall("sm:url", ns)
            locs = [node.findtext("sm:loc", namespaces=ns) for node in url_nodes]
            expected_locs = {ORIGIN + "/"}
            expected_locs.update(ORIGIN + f"/{lang}" + route for lang in LANGS for route in ROUTES)
            if len(url_nodes) != 37 or set(locs) != expected_locs or len(set(locs)) != len(locs):
                fail(f"Sitemap must contain exactly the 37 intended URLs; found {len(url_nodes)}")
            for node in url_nodes:
                alternates = {
                    item.attrib.get("hreflang"): item.attrib.get("href")
                    for item in node.findall("xhtml:link", ns)
                }
                loc = node.findtext("sm:loc", namespaces=ns)
                route = "/" if loc == ORIGIN + "/" else next(
                    (candidate for candidate in ROUTES if any(loc == ORIGIN + f"/{lang}" + candidate for lang in LANGS)),
                    None,
                )
                expected = {lang: ORIGIN + f"/{lang}" + route for lang in LANGS} if route else {}
                expected["x-default"] = ORIGIN + "/"
                if alternates != expected:
                    fail(f"Sitemap hreflang alternates are incorrect for {loc}")
        except (ET.ParseError, OSError) as exc:
            fail(f"Could not parse sitemap.xml: {exc}")

    if ERRORS:
        print(f"FAIL: {len(ERRORS)} validation error(s)")
        for error in ERRORS:
            print(" - " + error)
        raise SystemExit(1)

    print(
        "PASS: generated HTML attributes, social metadata, robots directives, "
        "canonical URLs, hreflang, local links, JSON-LD, multilingual profile, "
        "research archive, featured article, hero image and 37-entry sitemap."
    )


if __name__ == "__main__":
    main()
