from html import escape
import json
import math
import re


def _inline(text):
    code_items = []
    link_items = []

    def hold_code(match):
        token = f"@@CODE{len(code_items)}@@"
        code_items.append(f"<code>{escape(match.group(1))}</code>")
        return token

    text = re.sub(r"\x60([^\x60]+)\x60", hold_code, text)

    link_pattern = re.compile(r"\[([^\]]+)\]\((https?://[^\s)]+|/[^)\s]+|#[A-Za-z0-9_-]+|mailto:[^)\s]+)\)")

    def hold_link(match):
        token = f"@@LINK{len(link_items)}@@"
        href = escape(match.group(2), quote=True)
        label = escape(match.group(1))
        external = match.group(2).startswith("http")
        rel = ' rel="noopener noreferrer"' if external else ""
        link_items.append(f'<a href="{href}"{rel}>{label}</a>')
        return token

    text = link_pattern.sub(hold_link, text)
    text = escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", text)

    for i, value in enumerate(code_items):
        text = text.replace(f"@@CODE{i}@@", value)
    for i, value in enumerate(link_items):
        text = text.replace(f"@@LINK{i}@@", value)
    return text


def _plain(text):
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"[\x60*_]", "", text)
    return text.strip()


def _cells(line):
    value = line.strip()
    if value.startswith("|"):
        value = value[1:]
    if value.endswith("|"):
        value = value[:-1]
    return [cell.strip() for cell in value.split("|")]


def _is_table_rule(line):
    cells = _cells(line)
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell.replace(" ", "")) for cell in cells)


def render_markdown(source):
    lines = source.splitlines()
    output = []
    headings = []
    i = 0
    word_count = len(re.findall(r"\b[\w'-]+\b", source, flags=re.UNICODE))
    section_number = 0
    fence = chr(96) * 3

    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue

        if line.startswith(fence):
            language = re.sub(r"[^a-zA-Z0-9_-]", "", line[3:].strip())
            i += 1
            code_lines = []
            while i < len(lines) and not lines[i].strip().startswith(fence):
                code_lines.append(lines[i])
                i += 1
            i += 1
            cls = f' class="language-{language}"' if language else ""
            output.append(f"<pre><code{cls}>{escape(chr(10).join(code_lines))}</code></pre>")
            continue

        heading = re.match(r"^(#{2,4})\s+(.+)$", line)
        if heading:
            level = len(heading.group(1))
            section_number += 1
            title = _plain(heading.group(2))
            anchor = f"section-{section_number:02d}"
            headings.append({"level": level, "title": title, "id": anchor})
            output.append(f'<h{level} id="{anchor}">{_inline(heading.group(2))}</h{level}>')
            i += 1
            continue

        if i + 1 < len(lines) and "|" in line and _is_table_rule(lines[i + 1].strip()):
            headers = _cells(line)
            i += 2
            rows = []
            while i < len(lines) and "|" in lines[i] and lines[i].strip():
                rows.append(_cells(lines[i]))
                i += 1
            head_html = "".join(f"<th scope=\"col\">{_inline(cell)}</th>" for cell in headers)
            body_html = []
            for row in rows:
                cells = "".join(f"<td>{_inline(cell)}</td>" for cell in row[:len(headers)])
                if len(row) < len(headers):
                    cells += "".join("<td></td>" for _ in range(len(headers) - len(row)))
                body_html.append(f"<tr>{cells}</tr>")
            output.append(
                '<div class="article-table" role="region" tabindex="0">'
                f'<table><thead><tr>{head_html}</tr></thead><tbody>{"".join(body_html)}</tbody></table></div>'
            )
            continue

        if re.fullmatch(r"[-*_]{3,}", line):
            output.append("<hr>")
            i += 1
            continue

        if line.startswith("> "):
            quote_lines = []
            while i < len(lines) and lines[i].strip().startswith("> "):
                quote_lines.append(lines[i].strip()[2:])
                i += 1
            output.append(f'<blockquote><p>{_inline(" ".join(quote_lines))}</p></blockquote>')
            continue

        if line.startswith("- ") or line.startswith("* "):
            items = []
            while i < len(lines) and (lines[i].strip().startswith("- ") or lines[i].strip().startswith("* ")):
                items.append(lines[i].strip()[2:])
                i += 1
            output.append("<ul>" + "".join(f"<li>{_inline(item)}</li>" for item in items) + "</ul>")
            continue

        if re.match(r"^\d+[.)]\s+", line):
            items = []
            while i < len(lines) and re.match(r"^\d+[.)]\s+", lines[i].strip()):
                items.append(re.sub(r"^\d+[.)]\s+", "", lines[i].strip()))
                i += 1
            output.append("<ol>" + "".join(f"<li>{_inline(item)}</li>" for item in items) + "</ol>")
            continue

        paragraph = [line]
        i += 1
        while i < len(lines):
            candidate = lines[i].strip()
            if (
                not candidate
                or candidate.startswith(fence)
                or re.match(r"^#{2,4}\s+", candidate)
                or candidate.startswith("> ")
                or candidate.startswith("- ")
                or candidate.startswith("* ")
                or re.match(r"^\d+[.)]\s+", candidate)
                or re.fullmatch(r"[-*_]{3,}", candidate)
                or (i + 1 < len(lines) and "|" in candidate and _is_table_rule(lines[i + 1].strip()))
            ):
                break
            paragraph.append(candidate)
            i += 1
        output.append(f"<p>{_inline(' '.join(paragraph))}</p>")

    return "".join(output), headings, word_count


def render_article(fields, content, lang):
    body, headings, word_count = render_markdown(content)
    reading_time = max(1, math.ceil(word_count / 180))
    direction = "rtl" if lang == "ar" else "ltr"
    labels = {
        "ar": {
            "published": "نُشر", "updated": "آخر تحديث", "reading": "دقيقة قراءة",
            "summary": "ملخص المقال", "contents": "المحتويات",
        },
        "en": {
            "published": "Published", "updated": "Updated", "reading": "min read",
            "summary": "Article summary", "contents": "Contents",
        },
        "fr": {
            "published": "Publié", "updated": "Mis à jour", "reading": "min de lecture",
            "summary": "Résumé de l’article", "contents": "Sommaire",
        },
    }[lang]
    toc_items = []
    for item in headings:
        css = "toc-subsection" if item["level"] >= 3 else "toc-section"
        toc_items.append(
            f'<li class="{css}"><a href="#{item["id"]}">{escape(item["title"])}</a></li>'
        )
    toc = (
        f'<nav class="article-toc" aria-label="{escape(labels["contents"])}">'
        f'<h2>{escape(labels["contents"])}</h2><ol>{"".join(toc_items)}</ol></nav>'
        if toc_items else ""
    )
    image_html = ""
    if fields.get("image"):
        image_html = (
            f'<figure class="article-hero"><img src="{escape(fields["image"], quote=True)}" '
            f'alt="{escape(fields.get("image_alt", fields["title"]), quote=True)}" '
            'width="1024" height="576" loading="eager" fetchpriority="high" decoding="async">'
            f'<figcaption>{escape(fields.get("image_caption", ""))}</figcaption></figure>'
        )
    summary_html = (
        f'<section class="article-summary"><h2>{escape(labels["summary"])}</h2>'
        f'<p>{escape(fields.get("summary", ""))}</p></section>'
    )
    meta = (
        f'<div class="article-meta">'
        f'<span>{escape(fields.get("author_display", fields.get("author", "Kasem Adra")))}</span>'
        f'<span>{escape(labels["published"])}: <time datetime="{escape(fields["date_published"])}">{escape(fields.get("published_label", fields["date_published"]))}</time></span>'
        f'<span>{escape(labels["updated"])}: <time datetime="{escape(fields.get("date_modified", fields["date_published"]))}">{escape(fields.get("modified_label", fields.get("published_label", fields["date_published"])))}</time></span>'
        f'<span>{reading_time} {escape(labels["reading"])}</span></div>'
    )
    article_html = (
        f'<article class="subpage longform" lang="{lang}" dir="{direction}">'
        f'<p class="label">{escape(fields.get("category", ""))}</p>'
        f'<h1>{escape(fields["title"])}</h1>'
        f'<p class="article-deck">{escape(fields.get("subtitle", ""))}</p>'
        f'{meta}{image_html}{summary_html}{toc}'
        f'<div class="article-content">{body}</div>'
        f'<p class="article-editorial-note">{escape(fields.get("editorial_note", ""))}</p>'
        '</article>'
    )
    return article_html, word_count, reading_time


def build_article_head(fields, lang, page_url, origin, person, word_count, reading_time):
    image_url = origin + fields["image"]
    title = fields.get("seo_title", fields["title"])
    description = fields["description"]
    locale = {"ar": "ar_AR", "en": "en_US", "fr": "fr_FR"}[lang]
    keywords = fields.get("keywords", [])
    about = [{"@type": "Thing", "name": value} for value in fields.get("about", [])]
    citations = [{"@type": "CreativeWork", "name": value["name"], "url": value["url"]} for value in fields.get("citations", [])]
    article = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "@id": page_url + "#article",
        "mainEntityOfPage": {"@type": "WebPage", "@id": page_url},
        "headline": fields["title"],
        "description": description,
        "image": {
            "@type": "ImageObject",
            "url": image_url,
            "width": 1024,
            "height": 576,
            "caption": fields.get("image_caption", ""),
        },
        "author": {"@type": "Person", "@id": person["@id"], "name": person["name"]},
        "publisher": {"@type": "Person", "@id": person["@id"], "name": person["name"]},
        "datePublished": fields["date_published"],
        "dateModified": fields.get("date_modified", fields["date_published"]),
        "inLanguage": lang,
        "articleSection": fields.get("article_section", "Artificial intelligence"),
        "keywords": keywords,
        "about": about,
        "citation": citations,
        "wordCount": word_count,
        "timeRequired": f"PT{reading_time}M",
        "isAccessibleForFree": True,
        "isPartOf": {
            "@type": "Blog",
            "@id": origin + f"/{lang}/blog/#blog",
            "name": {"ar": "مدونة قاسم عدرا", "en": "Kasem Adra’s blog", "fr": "Blog de Kasem Adra"}[lang],
            "url": origin + f"/{lang}/blog/",
        },
    }
    breadcrumb_names = {
        "ar": ["الرئيسية", "المدونة", fields["title"]],
        "en": ["Home", "Blog", fields["title"]],
        "fr": ["Accueil", "Blog", fields["title"]],
    }[lang]
    breadcrumb_urls = [origin + f"/{lang}/", origin + f"/{lang}/blog/", page_url]
    breadcrumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "@id": page_url + "#breadcrumb",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": name, "item": breadcrumb_urls[i]}
            for i, name in enumerate(breadcrumb_names)
        ],
    }
    tags = [
        f'<meta name="author" content="{escape(fields.get("author_display", person["name"]), quote=True)}">',
        '<meta property="og:type" content="article">',
        '<meta property="og:site_name" content="Kasem Adra">',
        f'<meta property="og:locale" content="{locale}">',
        f'<meta property="og:title" content="{escape(title, quote=True)}">',
        f'<meta property="og:description" content="{escape(description, quote=True)}">',
        f'<meta property="og:url" content="{escape(page_url, quote=True)}">',
        f'<meta property="og:image" content="{escape(image_url, quote=True)}">',
        f'<meta property="og:image:alt" content="{escape(fields.get("image_alt", fields["title"]), quote=True)}">',
        f'<meta property="article:published_time" content="{escape(fields["date_published"], quote=True)}">',
        f'<meta property="article:modified_time" content="{escape(fields.get("date_modified", fields["date_published"]), quote=True)}">',
        f'<meta property="article:author" content="{escape(person["name"], quote=True)}">',
        f'<meta property="article:section" content="{escape(fields.get("article_section", "Artificial intelligence"), quote=True)}">',
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{escape(title, quote=True)}">',
        f'<meta name="twitter:description" content="{escape(description, quote=True)}">',
        f'<meta name="twitter:image" content="{escape(image_url, quote=True)}">',
        f'<meta name="twitter:image:alt" content="{escape(fields.get("image_alt", fields["title"]), quote=True)}">',
        '<script type="application/ld+json">' + json.dumps(article, ensure_ascii=False) + '</script>',
        '<script type="application/ld+json">' + json.dumps(breadcrumb, ensure_ascii=False) + '</script>',
    ]
    return "".join(tags)
