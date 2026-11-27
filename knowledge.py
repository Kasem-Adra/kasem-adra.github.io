from pathlib import Path
from html import escape
from json import dumps
import re
import xml.etree.ElementTree as ET

ORIGIN = "https://kasemadra.com"
PERSON_ID = ORIGIN + "/#person"
WEBSITE_ID = ORIGIN + "/#website"
ORGANIZATION_ID = ORIGIN + "/#qassem-ai"
LANGS = ("en", "ar", "fr")
LINKEDIN = "https://www.linkedin.com/in/kasem-adra/"
GITHUB = "https://github.com/Kasem-Adra"
GITHUB_PROJECTS = "https://github.com/QassemAi"
ORCID = "https://orcid.org/0009-0004-7615-4978"
QASSEM_SITE = "https://qassem.net/"
X_PROFILE = "https://x.com/QassemAdra"
INSTAGRAM = "https://www.instagram.com/qassemadra/"
PROTOCOL_DOI = "https://doi.org/10.5281/zenodo.24488951"
RESULTS_DOI = "https://doi.org/10.5281/zenodo.24549236"
ARCHIVE_ROUTE = "/archive/"

PERSON = {
    "@type": "Person",
    "@id": PERSON_ID,
    "name": "Kasem Adra",
    "alternateName": ["قاسم عدرا", "Qassem Adra"],
    "url": ORIGIN + "/en/about/",
    "image": ORIGIN + "/assets/kasem-adra-portrait.jpg",
    "jobTitle": "Independent AI Researcher",
    "description": "Kasem Adra (قاسم عدرا) is an independent AI researcher based in France. His work examines how local AI assistants verify task completion and recover from errors, including the ACO-LLM research protocol and evaluation.",
    "identifier": {
        "@type": "PropertyValue",
        "propertyID": "ORCID",
        "value": "0009-0004-7615-4978",
        "url": ORCID
    },
    "sameAs": [ORCID, GITHUB, LINKEDIN, QASSEM_SITE, X_PROFILE, INSTAGRAM],
    "affiliation": {"@id": ORGANIZATION_ID},
    "subjectOf": [
        {
            "@type": "ScholarlyArticle",
            "@id": PROTOCOL_DOI,
            "name": "Adaptive Cognitive Orchestration for Resource-Constrained Local Language Models (ACO-LLM): A Contract-Driven Research Protocol with Formal Guarantees and Reference Implementation",
            "url": PROTOCOL_DOI
        },
        {
            "@type": "ScholarlyArticle",
            "@id": RESULTS_DOI,
            "name": "Adaptive Cognitive Orchestration for Local Language Models: A Held-Out Evaluation of Structural Verification and Repair",
            "url": RESULTS_DOI
        }
    ],
    "knowsAbout": [
        "Local artificial intelligence assistants",
        "Large language model evaluation",
        "Task completion verification",
        "Tool use and error recovery in AI agents",
        "Arabic language technology",
    ]
}

ORGANIZATION = {
    "@type": "Organization",
    "@id": ORGANIZATION_ID,
    "name": "QassemAi",
    "url": GITHUB_PROJECTS,
    "description": "GitHub organization hosting technical projects associated with Kasem Adra.",
    "sameAs": [GITHUB_PROJECTS]
}

UI = {
    "en": {
        "home": "Home", "projects": "Projects", "research": "Research", "writing": "Writing",
        "about": "About", "archive": "Research archive", "contact": "Contact",
        "archive_title": "Research and project index",
        "archive_desc": "A structured index of Kasem Adra’s research publications, projects and writing, with links to original records.",
        "archive_intro": "This index brings together research publications, projects and writing by Kasem Adra, with links to the original records and publication pages.",
        "research_archive": "Research archive",
        "protocol_title": "ACO-LLM research protocol",
        "results_title": "ACO-LLM evaluation results",
        "writing_archive": "Writing and research notes",
        "projects_archive": "Projects",
        "profile_archive": "Author profile",
        "open": "Open record",
        "about_archive": "About this archive",
        "about_archive_text": "The multilingual site connects the author profile with research publications, projects and writing.",
        "lang_gateway": "Choose a language",
        "gateway_label": "Independent AI Researcher · Official Website",
        "gateway_desc": "Research on local language models, AI agents, task verification and ACO-LLM.",
        "language_en": "English", "language_ar": "العربية", "language_fr": "Français",
        "footer": "Official website of Kasem Adra",
    },
    "ar": {
        "home": "الرئيسية", "projects": "المشاريع", "research": "الأبحاث", "writing": "الكتابات",
        "about": "عني", "archive": "الأرشيف البحثي", "contact": "تواصل",
        "archive_title": "فهرس الأبحاث والمشاريع",
        "archive_desc": "فهرس منظم لمنشورات قاسم عدرا البحثية ومشاريعه وكتاباته، مع روابط إلى السجلات والصفحات الأصلية.",
        "archive_intro": "يجمع هذا الفهرس منشورات قاسم عدرا البحثية ومشاريعه وكتاباته، مع روابط إلى السجلات وصفحات النشر الأصلية.",
        "research_archive": "الأرشيف البحثي",
        "protocol_title": "بروتوكول ACO-LLM البحثي",
        "results_title": "نتائج تقييم ACO-LLM",
        "writing_archive": "الكتابات والملاحظات البحثية",
        "projects_archive": "المشاريع",
        "profile_archive": "صفحة المؤلف",
        "open": "فتح السجل",
        "about_archive": "حول هذا الأرشيف",
        "about_archive_text": "يربط الموقع متعدد اللغات الملف التعريفي بالمؤلفات البحثية والمشاريع والكتابات.",
        "lang_gateway": "اختر اللغة",
        "gateway_label": "باحث مستقل في الذكاء الاصطناعي · الموقع الرسمي",
        "gateway_desc": "أبحاث حول النماذج اللغوية المحلية والوكلاء الأذكياء والتحقق من المهام وبروتوكول ACO-LLM.",
        "language_en": "English", "language_ar": "العربية", "language_fr": "Français",
        "footer": "الموقع الرسمي لقاسم عدرا",
    },
    "fr": {
        "home": "Accueil", "projects": "Projets", "research": "Recherche", "writing": "Écrits",
        "about": "À propos", "archive": "Archives de recherche", "contact": "Contact",
        "archive_title": "Index des recherches et des projets",
        "archive_desc": "Un index structuré des publications de recherche, projets et écrits de Kasem Adra, avec des liens vers les références originales.",
        "archive_intro": "Cet index rassemble les publications de recherche, projets et écrits de Kasem Adra, avec des liens vers les références et pages de publication originales.",
        "research_archive": "Archives de recherche",
        "protocol_title": "Protocole de recherche ACO-LLM",
        "results_title": "Résultats de l’évaluation ACO-LLM",
        "writing_archive": "Écrits et notes de recherche",
        "projects_archive": "Projets",
        "profile_archive": "Profil de l’auteur",
        "open": "Consulter la fiche",
        "about_archive": "À propos de ces archives",
        "about_archive_text": "Le site multilingue relie le profil de l’auteur à ses publications de recherche, ses projets et ses écrits.",
        "lang_gateway": "Choisir une langue",
        "gateway_label": "Chercheur indépendant en IA · Site officiel",
        "gateway_desc": "Recherche sur les modèles de langage locaux, les agents IA, la vérification des tâches et ACO-LLM.",
        "language_en": "English", "language_ar": "العربية", "language_fr": "Français",
        "footer": "Site officiel de Kasem Adra",
    }
}

def nav(lang):
    u = UI[lang]
    links = [
        (u["home"], f"/{lang}/"),
        (u["projects"], f"/{lang}/projects/"),
        (u["research"], f"/{lang}/publications/"),
        (u["writing"], f"/{lang}/blog/"),
        (u["about"], f"/{lang}/about/"),
        (u["archive"], f"/{lang}/archive/")
    ]
    return "".join(f'<a href="{href}">{escape(label)}</a>' for label, href in links)

def language_switcher(lang, route):
    return '<div class="languages">' + "".join(
        f'<a href="/{other}{route}" hreflang="{other}" lang="{other}"' +
        (' aria-current="page"' if other == lang else '') + f'>{other.upper()}</a>'
        for other in LANGS
    ) + '</div>'

def shell_page(dist, lang, route, title, description, main, public_build):
    u = UI[lang]
    direction = "rtl" if lang == "ar" else "ltr"
    canonical = ORIGIN + f"/{lang}" + route
    alternates = "".join(
        f'<link rel="alternate" hreflang="{other}" href="{ORIGIN}/{other}{route}">'
        for other in LANGS
    ) + f'<link rel="alternate" hreflang="x-default" href="{ORIGIN}/">'
    og_image = f'<meta property="og:image" content="{ORIGIN}/assets/kasem-adra-portrait.jpg">'
    head = f'''<!doctype html>
<html lang="{lang}" dir="{direction}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)} · Kasem Adra</title>
<meta name="description" content="{escape(description, quote=True)}">
<meta name="author" content="Kasem Adra">
<meta name="robots" content="{'index,follow' if public_build else 'noindex'}">
<link rel="canonical" href="{canonical}">
{alternates}
<link rel="icon" type="image/png" href="/assets/kasem-calligraphy-transparent.png">
<meta property="og:site_name" content="Kasem Adra">
<meta property="og:type" content="article">
<meta property="og:title" content="{escape(title, quote=True)}">
<meta property="og:description" content="{escape(description, quote=True)}">
<meta property="og:url" content="{canonical}">
<meta property="og:locale" content="{'ar_SY' if lang == 'ar' else 'fr_FR' if lang == 'fr' else 'en_US'}">
{og_image}
<meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="/style.css">
</head>
<body>
<div class="shell">
<header><a class="wordmark" href="/{lang}/">Kasem Adra</a><nav aria-label="Main navigation">{nav(lang)}</nav><div class="header-controls">{language_switcher(lang, route)}</div></header>
<main><div class="subpage" dir="{direction}">{main}</div></main>
<footer><span>{escape(u["footer"])}</span><div class="profiles"><a href="{GITHUB}">GitHub</a><a href="{GITHUB_PROJECTS}">Qassem projects</a><a href="{ORCID}">ORCID</a><a href="{LINKEDIN}">LinkedIn</a><a href="{X_PROFILE}">X</a><a href="{INSTAGRAM}">Instagram</a><a href="{QASSEM_SITE}">Qassem.net</a></div></footer>
</div>
</body>
</html>'''
    out = dist / lang / route.strip("/") / "index.html"
    if route == "/":
        out = dist / lang / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(head, encoding="utf-8")

def archive_index_html(lang):
    u = UI[lang]
    rows = [
        (u["protocol_title"], "ACO-LLM protocol, DOI and full text." if lang == "en" else "البروتوكول البحثي ومعرّف DOI والنص الكامل." if lang == "ar" else "Protocole de recherche, DOI et texte intégral.", f"/{lang}/publications/aco-llm/"),
        (u["results_title"], "Held-out evaluation preprint, findings and limitations." if lang == "en" else "ورقة نتائج التقييم المحجوب ونتائجه وحدوده." if lang == "ar" else "Prépublication de l’évaluation réservée, résultats et limites.", f"/{lang}/publications/aco-llm-results/"),
        (u["projects_archive"], "Local AI assistant and selected data-science projects." if lang == "en" else "المساعد المحلي ومشاريع مختارة في علم البيانات." if lang == "ar" else "Assistant IA local et projets sélectionnés en science des données.", f"/{lang}/projects/"),
        (u["writing_archive"], "Research notes and writing by Kasem Adra." if lang == "en" else "ملاحظات بحثية وكتابات قاسم عدرا." if lang == "ar" else "Notes de recherche et textes de Kasem Adra.", f"/{lang}/blog/")
    ]
    cards = "".join(
        f'<article class="archive-card"><span>{escape(u["open"])}</span><div><h2><a href="{href}">{escape(title)}</a></h2><p>{escape(desc)}</p></div></article>'
        for title, desc, href in rows
    )
    main = f'''<p class="label">{escape(u["archive"])}</p>
<h1>{escape(u["archive_title"])}</h1>
<p class="archive-lead">{escape(u["archive_intro"])}</p>
<section><h2>{escape(u["about_archive"])}</h2>
<p>{escape(u["profile_archive"])}: <a href="/{lang}/about/">Kasem Adra / قاسم عدرا</a>. {escape(u["about_archive_text"])}</p>
</section>
<section><h2>{escape(u["archive"])}</h2>{cards}</section>
<section><h2>{escape(u["research_archive"])}</h2>
<p><a href="/{lang}/publications/"> {escape(u["research"])} </a> · <a href="{PROTOCOL_DOI}">DOI 10.5281/zenodo.24488951</a> · <a href="{RESULTS_DOI}">DOI 10.5281/zenodo.24549236</a></p>
</section>'''
    return main

def page_schema(lang, route, title, description):
    canonical = ORIGIN + f"/{lang}" + route
    webpage = {
        "@type": "WebPage",
        "@id": canonical + "#webpage",
        "url": canonical,
        "name": title,
        "description": description,
        "inLanguage": lang,
        "isPartOf": {"@id": WEBSITE_ID},
        "about": {"@id": PERSON_ID},
        "author": {"@id": PERSON_ID}
    }
    graph = [PERSON, ORGANIZATION, webpage]
    if route == "/about/":
        webpage["@type"] = "ProfilePage"
        webpage["mainEntity"] = {"@id": PERSON_ID}
    elif route == ARCHIVE_ROUTE:
        webpage["@type"] = "CollectionPage"
        webpage["hasPart"] = [
            {"@id": PROTOCOL_DOI},
            {"@id": RESULTS_DOI}
        ]
    elif route == "/publications/":
        webpage["@type"] = "CollectionPage"
    elif route == "/publications/aco-llm/":
        graph.append({
            "@type": "ScholarlyArticle",
            "@id": PROTOCOL_DOI,
            "headline": "Adaptive Cognitive Orchestration for Resource-Constrained Local Language Models (ACO-LLM): A Contract-Driven Research Protocol with Formal Guarantees and Reference Implementation",
            "author": {"@id": PERSON_ID},
            "datePublished": "2026-11-24",
            "url": canonical,
            "sameAs": PROTOCOL_DOI,
            "identifier": {"@type":"PropertyValue","propertyID":"DOI","value":"10.5281/zenodo.24488951"},
            "inLanguage": "en",
            "isPartOf": {"@id": ORIGIN + f"/{lang}/publications/#collection"}
        })
        webpage["mainEntity"] = {"@id": PROTOCOL_DOI}
    elif route == "/publications/aco-llm-results/":
        graph.append({
            "@type": "ScholarlyArticle",
            "@id": RESULTS_DOI,
            "headline": "Adaptive Cognitive Orchestration for Local Language Models: A Held-Out Evaluation of Structural Verification and Repair",
            "author": {"@id": PERSON_ID},
            "datePublished": "2026-11-26",
            "url": canonical,
            "sameAs": RESULTS_DOI,
            "identifier": {"@type":"PropertyValue","propertyID":"DOI","value":"10.5281/zenodo.24549236"},
            "inLanguage": "en",
            "isPartOf": {"@id": ORIGIN + f"/{lang}/publications/#collection"},
            "description": "Research preprint; not peer reviewed."
        })
        webpage["mainEntity"] = {"@id": RESULTS_DOI}
    elif route.startswith("/blog/") and route != "/blog/":
        slug = route.strip("/").split("/")[-1]
        post_titles = {
            "checking-work": {"en":"How to Verify an AI Assistant’s Work: A Practical Guide","ar":"كيف نتحقّق من عمل المساعد الذكي؟ دليل عملي","fr":"Comment vérifier le travail d’un assistant IA ? Guide pratique"},
            "arabic-calligraphy": {"en":"When Letters Become a Drawing","ar":"حين تصبح الحروف رسمة","fr":"Quand les lettres deviennent un dessin"},
            "local-ai-agent-reliability": {"en":"Can We Trust a Local AI Assistant?","ar":"هل يمكن الوثوق بمساعد ذكاء اصطناعي محلي؟","fr":"Peut-on faire confiance à un assistant IA local ?"}
        }
        post = {
            "@type":"BlogPosting",
            "@id":canonical+"#article",
            "headline":post_titles.get(slug,{}).get(lang,title),
            "description":description,
            "author":{"@id":PERSON_ID},
            "publisher":{"@id":PERSON_ID},
            "datePublished":"2026-11-27" if slug == "local-ai-agent-reliability" else "2026-11-26",
            "dateModified":"2026-11-27" if slug in ("local-ai-agent-reliability", "checking-work") else "2026-11-26",
            "inLanguage":lang,
            "url":canonical,
            "mainEntityOfPage":{"@id":canonical+"#webpage"},
            "isPartOf":{"@id":ORIGIN+f"/{lang}/blog/#collection"}
        }
        if slug == "checking-work":
            post["articleSection"] = "AI agent reliability; task verification"
            post["keywords"] = ["AI assistant verification", "task completion", "silent tool failure", "structural validation", "semantic correctness", "ACO-LLM"]
            post["about"] = [
                {"@type":"Thing","name":"AI agent reliability"},
                {"@type":"Thing","name":"Task completion verification"},
                {"@type":"Thing","name":"Data validation"}
            ]
            post["citation"] = [PROTOCOL_DOI, RESULTS_DOI]
            post["isAccessibleForFree"] = True
        if slug == "arabic-calligraphy":
            post["image"] = ORIGIN + "/assets/kasem-calligraphy-transparent.png"
        if slug == "local-ai-agent-reliability":
            post["image"] = ORIGIN + "/assets/local-ai-agent-reliability-hero.webp"
            post["articleSection"] = "Local AI; AI agents; reliability engineering"
            post["keywords"] = ["local AI", "AI agent reliability", "silent failure", "independent verification", "ACO-LLM", "Gemma 4"]
            post["about"] = [
                {"@type":"Thing","name":"Local artificial intelligence"},
                {"@type":"Thing","name":"AI agents"},
                {"@type":"Thing","name":"Task completion verification"},
                {"@type":"Thing","name":"Reliability engineering"}
            ]
            post["citation"] = [
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
                "https://arxiv.org/abs/2406.13352"
            ]
            post["isAccessibleForFree"] = True
        graph.append(post)
        webpage["mainEntity"] = {"@id":canonical+"#article"}
    elif route in ("/blog/","/projects/"):
        webpage["@type"] = "CollectionPage"
    elif route == "/projects/local-assistant/":
        graph.append({
            "@type":"CreativeWork",
            "@id":canonical+"#project",
            "author":{"@id":PERSON_ID},
            "name": {
                "en": "A local AI assistant for Arabic",
                "ar": "مساعد ذكاء اصطناعي محلي بالعربية",
                "fr": "Un assistant IA local en arabe"
            }[lang],
            "description": description,
            "url": canonical,
            "inLanguage": ["ar","en","fr"],
            "about": ["Local AI assistants","Arabic language technology","On-device AI","Speech recognition","Task verification"],
            "keywords": ["local AI", "Gemma 4", "Arabic", "Whisper", "Edge TTS", "task verification"]
        })
        webpage["mainEntity"]={"@id":canonical+"#project"}
    if route == "/blog/":
        graph.append({
            "@type":"CollectionPage",
            "@id":ORIGIN+f"/{lang}/blog/#collection",
            "url":canonical,
            "name":UI[lang]["writing_archive"],
            "about":{"@id":PERSON_ID},
            "hasPart":[
                {"@id":ORIGIN+f"/{lang}/blog/local-ai-agent-reliability/#article"},
                {"@id":ORIGIN+f"/{lang}/blog/checking-work/#article"},
                {"@id":ORIGIN+f"/{lang}/blog/arabic-calligraphy/#article"}
            ]
        })
    if route == "/publications/":
        graph.append({
            "@type":"CollectionPage",
            "@id":ORIGIN+f"/{lang}/publications/#collection",
            "url":canonical,
            "name":UI[lang]["research_archive"],
            "about":{"@id":PERSON_ID},
            "hasPart":[{"@id":PROTOCOL_DOI},{"@id":RESULTS_DOI}]
        })
    if route == "/archive/":
        graph.append({
            "@type":"CollectionPage",
            "@id":ORIGIN+f"/{lang}/archive/#collection",
            "url":canonical,
            "name":UI[lang]["archive_title"],
            "about":{"@id":PERSON_ID},
            "hasPart":[{"@id":PROTOCOL_DOI},{"@id":RESULTS_DOI}]
        })
    # Add a breadcrumb trail for every page.
    crumbs = [{"name":UI[lang]["home"],"item":ORIGIN+f"/{lang}/"}]
    if route != "/":
        segments = [s for s in route.strip("/").split("/") if s]
        path = ""
        for i, segment in enumerate(segments):
            path += "/" + segment
            href = ORIGIN + f"/{lang}" + path + "/"
            labels = {
                "about":UI[lang]["about"],"archive":UI[lang]["archive"],
                "projects":UI[lang]["projects"],"local-assistant":"A local AI assistant",
                "publications":UI[lang]["research"],"aco-llm":UI[lang]["protocol_title"],
                "aco-llm-results":UI[lang]["results_title"],"blog":UI[lang]["writing"],
                "checking-work":{
                    "en":"How to Verify an AI Assistant’s Work",
                    "ar":"كيف نتحقّق من عمل المساعد الذكي؟",
                    "fr":"Comment vérifier le travail d’un assistant IA ?"
                }[lang],
                "arabic-calligraphy":"When Letters Become a Drawing"
            }
            crumbs.append({"name":labels.get(segment,segment.replace("-"," ").title()),"item":href})
    graph.append({
        "@type":"BreadcrumbList",
        "@id":canonical+"#breadcrumb",
        "itemListElement":[
            {"@type":"ListItem","position":i+1,"name":item["name"],"item":item["item"]}
            for i,item in enumerate(crumbs)
        ]
    })
    return {"@context":"https://schema.org","@graph":graph}

def meta_replace(doc, pattern, replacement):
    if re.search(pattern, doc, flags=re.I):
        return re.sub(pattern, replacement, doc, count=1, flags=re.I)
    return doc

def route_for_file(file, dist):
    rel = file.parent.relative_to(dist)
    parts = rel.parts
    if parts and parts[0] in LANGS:
        lang = parts[0]
        route_parts = parts[1:]
        route = "/" + "/".join(route_parts) + "/" if route_parts else "/"
        return lang, route
    route = "/" + "/".join(parts) + "/" if parts else "/"
    return "en", route

def enrich_existing_pages(dist, public_build):
    descriptions = {
        "/": {
            "en":("Kasem Adra | Independent AI Researcher","Official profile of Kasem Adra: independent AI research in local assistants, ACO-LLM publications, projects and writing."),
            "ar":("قاسم عدرا | باحث مستقل في الذكاء الاصطناعي","الملف الرسمي لقاسم عدرا: أبحاث الذكاء الاصطناعي المحلي، منشورات ACO-LLM، المشاريع والكتابات."),
            "fr":("Kasem Adra | Chercheur indépendant en IA","Profil officiel de Kasem Adra : recherche sur les assistants IA locaux, publications ACO-LLM, projets et écrits.")
        },
        "/about/":{
            "en":("About Kasem Adra | Biography, Research and Public Profiles","Biographical profile of Kasem Adra, independent AI researcher in France: research focus, education, projects, publications and verified public identifiers."),
            "ar":("قاسم عدرا | السيرة والأبحاث والهوية الرقمية","نبذة موثقة عن قاسم عدرا، الباحث المستقل في الذكاء الاصطناعي: مجال البحث والمشاريع والمنشورات والمعرّفات العامة."),
            "fr":("À propos de Kasem Adra | Parcours, recherche et profils publics","Profil biographique de Kasem Adra, chercheur indépendant en IA en France : recherche, projets, publications et identifiants publics.")
        },
        "/projects/":{
            "en":("Projects by Kasem Adra","Selected projects by Kasem Adra, including a local Arabic AI assistant and data-science work."),
            "ar":("مشاريع قاسم عدرا","مشاريع قاسم عدرا، ومنها مساعد ذكاء اصطناعي محلي يدعم العربية ومشاريع في علم البيانات."),
            "fr":("Projets de Kasem Adra","Projets sélectionnés de Kasem Adra, dont un assistant IA local prenant en charge l’arabe et des travaux en science des données.")
        },
        "/projects/local-assistant/":{
            "en":("Local Arabic AI Assistant | Kasem Adra","A local Arabic AI assistant using Gemma 4, local Whisper speech recognition, Edge TTS speech output and independently checked tool actions."),
            "ar":("مساعد ذكاء اصطناعي محلي بالعربية | قاسم عدرا","مشروع مساعد محلي يستخدم Gemma 4 والتعرّف الصوتي المحلي عبر Whisper وتوليد الصوت عبر Edge TTS مع التحقق من نتائج الأدوات."),
            "fr":("Assistant IA local en arabe | Kasem Adra","Assistant IA local en arabe utilisant Gemma 4, la reconnaissance vocale locale Whisper, la synthèse Edge TTS et la vérification des actions des outils.")
        },
        "/publications/":{
            "en":("Research by Kasem Adra | ACO-LLM Publications","Research publications by Kasem Adra, including the ACO-LLM protocol and its separate held-out evaluation preprint."),
            "ar":("أبحاث قاسم عدرا | منشورات ACO-LLM","الأبحاث المنشورة لقاسم عدرا، ومنها بروتوكول ACO-LLM وورقة نتائج التقييم المستقلة."),
            "fr":("Recherche de Kasem Adra | Publications ACO-LLM","Publications de recherche de Kasem Adra : protocole ACO-LLM et prépublication distincte des résultats.")
        },
        "/publications/aco-llm/":{
            "en":("ACO-LLM Research Protocol | Kasem Adra | DOI 10.5281/zenodo.24488951","The ACO-LLM research protocol by Kasem Adra: contract-driven routing, structural verification and bounded repair for resource-constrained local language models."),
            "ar":("بروتوكول ACO-LLM البحثي | قاسم عدرا","بروتوكول ACO-LLM لقاسم عدرا: توجيه المهام والتحقق البنيوي والإصلاح المحدود للنماذج اللغوية المحلية."),
            "fr":("Protocole de recherche ACO-LLM | Kasem Adra","Protocole ACO-LLM de Kasem Adra : orientation des tâches, vérification structurelle et correction limitée pour les modèles locaux.")
        },
        "/publications/aco-llm-results/":{
            "en":("ACO-LLM Evaluation Results | Kasem Adra | Preprint","Held-out ACO-LLM evaluation results by Kasem Adra. The preprint reports a 20.83 percentage-point primary gain and is not peer reviewed."),
            "ar":("نتائج تقييم ACO-LLM | قاسم عدرا | ورقة أولية","نتائج التقييم المحجوب لـ ACO-LLM بقلم قاسم عدرا؛ تسجل الورقة تحسنًا رئيسيًا قدره 20.83 نقطة مئوية وهي غير محكّمة."),
            "fr":("Résultats de l’évaluation ACO-LLM | Kasem Adra | Prépublication","Résultats de l’évaluation réservée ACO-LLM par Kasem Adra : gain principal de 20,83 points ; prépublication non évaluée par les pairs.")
        },
        "/blog/":{
            "en":("Writing by Kasem Adra | Articles and Research Notes","Articles, technical notes and writing by Kasem Adra on local AI, task verification and design."),
            "ar":("كتابات قاسم عدرا | مقالات وملاحظات بحثية","مقالات وملاحظات تقنية وكتابات قاسم عدرا حول الذكاء الاصطناعي المحلي والتحقق من المهام والتصميم."),
            "fr":("Écrits de Kasem Adra | Articles et notes de recherche","Articles, notes techniques et textes de Kasem Adra sur l’IA locale, la vérification des tâches et le design.")
        },
        "/blog/checking-work/":{
            "en":("How to Verify an AI Assistant’s Work: A Practical Guide | Kasem Adra","A practical guide to checking files, values and tool outcomes independently of an AI assistant’s completion claim, including silent failures and validation limits."),
            "ar":("كيف نتحقّق من عمل المساعد الذكي؟ دليل عملي | قاسم عدرا","دليل عملي للتحقق من الملفات والقيم ونتائج الأدوات بصورة مستقلة، مع شرح الأعطال الصامتة وحدود الفحص البنيوي."),
            "fr":("Comment vérifier le travail d’un assistant IA ? Guide pratique | Kasem Adra","Guide pratique pour vérifier les fichiers, les valeurs et les résultats des outils indépendamment de l’assistant, avec les pannes silencieuses et les limites des contrôles.")
        },
        "/blog/local-ai-agent-reliability/":{
            "en":("Can We Trust a Local AI Assistant? | Kasem Adra","An evidence-based guide to local AI, agent reliability, silent tool failures, independent verification and the ACO-LLM evaluation."),
            "ar":("هل يمكن الوثوق بمساعد ذكاء اصطناعي محلي؟ | قاسم عدرا","دليل موثق عن الذكاء الاصطناعي المحلي وموثوقية الوكلاء وفشل الأدوات الصامت والتحقق المستقل ونتائج ACO-LLM."),
            "fr":("Peut-on faire confiance à un assistant IA local ? | Kasem Adra","Guide documenté sur l’IA locale, la fiabilité des agents, les défaillances silencieuses des outils, la vérification indépendante et l’évaluation ACO-LLM.")
        },
        "/blog/arabic-calligraphy/":{
            "en":("Arabic Calligraphy and the Kasem Adra Signature","A short design note about the Arabic calligraphic signature used on Kasem Adra’s website."),
            "ar":("الخط العربي وتوقيع قاسم عدرا","ملاحظة تصميمية عن التوقيع الحروفي العربي المستخدم في موقع قاسم عدرا."),
            "fr":("Calligraphie arabe et signature de Kasem Adra","Une note de design sur la signature calligraphique arabe utilisée sur le site de Kasem Adra.")
        }
    }
    for file in dist.rglob("index.html"):
        if file == dist / "index.html":
            continue
        lang, route = route_for_file(file, dist)
        doc = file.read_text(encoding="utf-8")
        if route in descriptions:
            title, desc = descriptions[route][lang]
            doc = meta_replace(doc, r"<title>.*?</title>", f"<title>{escape(title)}</title>")
            doc = meta_replace(doc, r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{escape(desc, quote=True)}">')
        else:
            m = re.search(r"<title>(.*?)</title>", doc, flags=re.I|re.S)
            title = re.sub(r"\s*·\s*Kasem Adra\s*$","",m.group(1) if m else "Kasem Adra")
            d = re.search(r'<meta name="description" content="([^"]*)">',doc,flags=re.I)
            desc = d.group(1) if d else "Kasem Adra — official profile, research and archive."
        # All pages use the same Person identifier; replace older isolated JSON-LD blocks with one connected graph.
        doc = re.sub(r'<script type="application/ld\+json">.*?</script>',"",doc,flags=re.I|re.S)
        graph = page_schema(lang,route,title,desc)
        doc = doc.replace("</head>", '<script type="application/ld+json">' + dumps(graph,ensure_ascii=False,separators=(",",":")) + '</script></head>',1)
        if route == "/about/":
            profile_titles = {
                "en": {
                    "bio":"Biography","contents":"Contents","facts":"Profile at a glance","name":"Name","occupation":"Occupation","occupation_value":"Independent AI researcher","origin":"Origin","origin_value":"Baniyas, Syria","location":"Based in","location_value":"France","education":"Education","research":"Research and publications","projects":"Projects","writing":"Writing","writing_link":"View all writing","featured_article":"Can We Trust a Local AI Assistant? — Evidence-based article on local assistant reliability","interests":"Other interests","identifiers":"Public identifiers","protocol_link":"ACO-LLM research protocol","results_link":"ACO-LLM evaluation results","projects_link":"View selected projects","preprint":"preprint",
                    "bio_text":"Kasem Adra (قاسم عدرا) is an independent AI researcher based in France and originally from Baniyas, Syria. He studies computer science and artificial intelligence. His work focuses on local AI assistants and methods for verifying task completion and recovering from errors. He published the ACO-LLM research protocol and a separate evaluation preprint. His academic background includes an MBA and a master’s degree in Digital Marketing and Analytics.",
                    "education_text":"MBA (Master of Business Administration); Master in Digital Marketing and Analytics; current studies in computer science and artificial intelligence.",
                    "research_text":"His independent research examines how local language models and AI agents can select tools, verify their outputs and recover from observable failures. The ACO-LLM protocol and its held-out evaluation are separate research records; the results paper is a preprint and has not been peer reviewed.",
                    "projects_text":"Selected work includes a local AI assistant designed to support Arabic text and speech, alongside data-science projects involving launch data and financial datasets.",
                                        "interests_text":"He also explores Arabic calligraphy and visual design, including the calligraphic signature used on this website."
                },
                "ar": {
                    "bio":"السيرة","contents":"المحتويات","facts":"بطاقة تعريفية","name":"الاسم","occupation":"الصفة","occupation_value":"باحث مستقل في الذكاء الاصطناعي","origin":"الأصل","origin_value":"بانياس، سوريا","location":"الإقامة","location_value":"فرنسا","education":"التعليم","research":"الأبحاث والمنشورات","projects":"المشاريع","writing":"الكتابات","writing_link":"عرض جميع الكتابات","featured_article":"هل يمكن الوثوق بمساعد ذكاء اصطناعي محلي؟ — مقالة موثقة عن موثوقية المساعدات المحلية","interests":"اهتمامات أخرى","identifiers":"المعرّفات العامة","protocol_link":"بروتوكول ACO-LLM البحثي","results_link":"نتائج تقييم ACO-LLM","projects_link":"عرض المشاريع المختارة","preprint":"ورقة أولية",
                    "bio_text":"قاسم عدرا باحث مستقل في الذكاء الاصطناعي يقيم في فرنسا وينحدر من مدينة بانياس السورية. يدرس علوم الحاسوب والذكاء الاصطناعي. يركز عمله على المساعدات الذكية المحلية وطرق التحقق من إنجاز المهام والتعافي من الأخطاء. نشر بروتوكول ACO-LLM البحثي، ثم ورقة أولية مستقلة لنتائج التقييم. وتشمل خلفيته الأكاديمية ماجستير إدارة الأعمال (MBA) وماجستير التسويق الرقمي وتحليل البيانات.",
                    "education_text":"ماجستير إدارة الأعمال (MBA)، وماجستير التسويق الرقمي وتحليل البيانات، مع متابعة دراسة علوم الحاسوب والذكاء الاصطناعي.",
                    "research_text":"تتناول أبحاثه المستقلة كيفية اختيار النماذج اللغوية المحلية والوكلاء الأذكياء للأدوات، والتحقق من مخرجاتها، والتعافي من الإخفاقات القابلة للرصد. بروتوكول ACO-LLM وورقة نتائج تقييمه سجلان بحثيان منفصلان؛ وورقة النتائج أولية وغير محكّمة.",
                    "projects_text":"تشمل أعماله مساعد ذكاء اصطناعي محليًا يدعم النص والصوت العربيين، إلى جانب مشاريع في علم البيانات تتناول بيانات إطلاق الصواريخ والبيانات المالية.",
                                        "interests_text":"يهتم أيضًا بالرسم والخط العربي والتصميم البصري، ومن ذلك التوقيع الحروفي المستخدم في هذا الموقع."
                },
                "fr": {
                    "bio":"Biographie","contents":"Sommaire","facts":"Profil en bref","name":"Nom","occupation":"Fonction","occupation_value":"Chercheur indépendant en IA","origin":"Origine","origin_value":"Baniyas, Syrie","location":"Résidence","location_value":"France","education":"Formation","research":"Recherche et publications","projects":"Projets","writing":"Écrits","writing_link":"Voir tous les écrits","featured_article":"Peut-on faire confiance à un assistant IA local ? — Article documenté sur la fiabilité des assistants locaux","interests":"Autres intérêts","identifiers":"Identifiants publics","protocol_link":"Protocole de recherche ACO-LLM","results_link":"Résultats de l’évaluation ACO-LLM","projects_link":"Voir les projets sélectionnés","preprint":"prépublication",
                    "bio_text":"Kasem Adra (قاسم عدرا) est un chercheur indépendant en intelligence artificielle basé en France et originaire de Baniyas, en Syrie. Il étudie l’informatique et l’intelligence artificielle. Ses travaux portent sur les assistants IA locaux et les méthodes permettant de vérifier l’achèvement des tâches et de corriger les erreurs. Il a publié le protocole de recherche ACO-LLM, puis une prépublication distincte présentant les résultats de l’évaluation. Sa formation comprend un MBA et un master en marketing numérique et analyse de données.",
                    "education_text":"MBA (Master of Business Administration), master en marketing numérique et analyse de données ; études en cours en informatique et intelligence artificielle.",
                    "research_text":"Ses recherches indépendantes portent sur la manière dont les modèles de langage locaux et les agents IA sélectionnent des outils, vérifient leurs résultats et récupèrent après des défaillances observables. Le protocole ACO-LLM et sa prépublication de résultats constituent deux références distinctes ; cette dernière n’a pas été évaluée par les pairs.",
                    "projects_text":"Ses projets comprennent un assistant IA local prenant en charge le texte et la voix en arabe, ainsi que des travaux en science des données portant sur les données de lancement spatial et les données financières.",
                                        "interests_text":"Il s’intéresse également au dessin, à la calligraphie arabe et au design visuel, notamment à la signature calligraphique de ce site."
                }
            }[lang]
            if 'id="profile-facts"' not in doc:
                infobox = f'<aside class="profile-infobox" id="profile-facts"><h2>{profile_titles["facts"]}</h2><dl><dt>{profile_titles["name"]}</dt><dd>Kasem Adra · قاسم عدرا</dd><dt>{profile_titles["occupation"]}</dt><dd>{profile_titles["occupation_value"]}</dd><dt>{profile_titles["origin"]}</dt><dd>{profile_titles["origin_value"]}</dd><dt>{profile_titles["location"]}</dt><dd>{profile_titles["location_value"]}</dd><dt>{profile_titles["education"]}</dt><dd>{profile_titles["education_text"]}</dd><dt>ORCID</dt><dd><a href="{ORCID}">0009-0004-7615-4978</a></dd></dl></aside>'
                toc = f'<nav class="profile-toc"><h2>{profile_titles["contents"]}</h2><ol><li><a href="#biography">{profile_titles["bio"]}</a></li><li><a href="#research-profile">{profile_titles["research"]}</a></li><li><a href="#projects-profile">{profile_titles["projects"]}</a></li><li><a href="#writing-profile">{profile_titles["writing"]}</a></li><li><a href="#identifiers">{profile_titles["identifiers"]}</a></li></ol></nav>'
                doc = doc.replace("</h1>", "</h1>" + infobox + toc + f'<h2 id="biography">{profile_titles["bio"]}</h2>', 1)
                pattern = r'(<img class="portrait"[^>]*>).*?(<p>(?:Member|عضو|Membre)[^<]*</p>)'
                replacement = lambda m: m.group(1) + f'<p class="profile-biography">{profile_titles["bio_text"]}</p>' + m.group(2)
                doc, replaced = re.subn(pattern, replacement, doc, count=1, flags=re.S)
                if replaced != 1:
                    raise RuntimeError("Could not locate the localized biography on " + str(file))
                extras = f'<section id="research-profile"><h2>{profile_titles["research"]}</h2><p>{profile_titles["research_text"]}</p><ul><li><a href="/{lang}/publications/aco-llm/">{profile_titles["protocol_link"]}</a> · <a href="{PROTOCOL_DOI}">DOI</a></li><li><a href="/{lang}/publications/aco-llm-results/">{profile_titles["results_link"]}</a> · <a href="{RESULTS_DOI}">DOI · {profile_titles["preprint"]}</a></li></ul></section><section id="projects-profile"><h2>{profile_titles["projects"]}</h2><p>{profile_titles["projects_text"]}</p><p><a href="/{lang}/projects/">{profile_titles["projects_link"]}</a></p></section><section id="writing-profile"><h2>{profile_titles["writing"]}</h2><p><a href="/{lang}/blog/local-ai-agent-reliability/">{profile_titles["featured_article"]}</a></p><p><a href="/{lang}/blog/">{profile_titles["writing_link"]}</a></p></section><section id="other-interests"><h2>{profile_titles["interests"]}</h2><p>{profile_titles["interests_text"]}</p></section>'
                if 'id="research-profile"' not in doc:
                    doc = doc.replace("</div></main>", extras + "</div></main>", 1)
            profile_section = {
                "en": '<section class="profile-identifiers" id="identifiers"><h2>Public identity and research records</h2><p>Public identifiers and author-controlled records help distinguish this profile from people with similar names. They do not replace independent coverage or peer review.</p><ul><li><a href="' + ORCID + '">ORCID iD: 0009-0004-7615-4978</a></li><li><a href="' + LINKEDIN + '">LinkedIn profile</a></li><li><a href="' + GITHUB + '">Primary GitHub profile</a></li><li><a href="' + GITHUB_PROJECTS + '">QassemAi GitHub organization</a></li><li><a href="' + X_PROFILE + '">X profile</a></li><li><a href="' + INSTAGRAM + '">Instagram profile</a></li><li><a href="' + QASSEM_SITE + '">Qassem.net · related personal domain</a></li><li><a href="' + PROTOCOL_DOI + '">ACO-LLM research protocol (DOI)</a></li><li><a href="' + RESULTS_DOI + '">ACO-LLM evaluation results (preprint DOI)</a></li><li><a href="/en/archive/">Research archive</a></li></ul></section>',
                "ar": '<section class="profile-identifiers" id="identifiers"><h2>الهوية العامة والسجلات البحثية</h2><p>تساعد المعرّفات والسجلات التي يديرها المؤلف على تمييز هذا الملف عن الأشخاص المتشابهة أسماؤهم، لكنها لا تحل محل التغطية المستقلة أو التحكيم العلمي.</p><ul><li><a href="' + ORCID + '">معرّف ORCID: 0009-0004-7615-4978</a></li><li><a href="' + LINKEDIN + '">الملف المهني على LinkedIn</a></li><li><a href="' + GITHUB + '">ملف GitHub الأساسي</a></li><li><a href="' + GITHUB_PROJECTS + '">منظمة QassemAi على GitHub</a></li><li><a href="' + X_PROFILE + '">حساب X</a></li><li><a href="' + INSTAGRAM + '">حساب Instagram</a></li><li><a href="' + QASSEM_SITE + '">Qassem.net · النطاق الشخصي المرتبط</a></li><li><a href="' + PROTOCOL_DOI + '">بروتوكول ACO-LLM البحثي (DOI)</a></li><li><a href="' + RESULTS_DOI + '">نتائج تقييم ACO-LLM (DOI الورقة الأولية)</a></li><li><a href="/ar/archive/">الأرشيف البحثي</a></li></ul></section>',
                "fr": '<section class="profile-identifiers" id="identifiers"><h2>Identité publique et références de recherche</h2><p>Les identifiants publics et les références contrôlées par l’auteur aident à distinguer ce profil des personnes portant un nom similaire. Ils ne remplacent ni la couverture indépendante ni l’évaluation par les pairs.</p><ul><li><a href="' + ORCID + '">Identifiant ORCID : 0009-0004-7615-4978</a></li><li><a href="' + LINKEDIN + '">Profil LinkedIn</a></li><li><a href="' + GITHUB + '">Profil GitHub principal</a></li><li><a href="' + GITHUB_PROJECTS + '">Organisation GitHub QassemAi</a></li><li><a href="' + X_PROFILE + '">Profil X</a></li><li><a href="' + INSTAGRAM + '">Profil Instagram</a></li><li><a href="' + QASSEM_SITE + '">Qassem.net · domaine personnel associé</a></li><li><a href="' + PROTOCOL_DOI + '">Protocole de recherche ACO-LLM (DOI)</a></li><li><a href="' + RESULTS_DOI + '">Résultats de l’évaluation ACO-LLM (DOI de la prépublication)</a></li><li><a href="/fr/archive/">Archives de recherche</a></li></ul></section>'
            }[lang]
            if "profile-identifiers" not in doc:
                doc = doc.replace("</div></main>", profile_section + "</div></main>", 1)
        if public_build:
            canonical = ORIGIN + f"/{lang}" + route
            if route == "/" and lang == "en":
                canonical = ORIGIN + "/en/"
            doc = meta_replace(doc,r'<link rel="canonical" href="[^"]*">',f'<link rel="canonical" href="{canonical}">')
        # Keep the archive discoverable from every page through a normal crawlable anchor.
        archive_label = UI[lang]["archive"]
        archive_href = f"/{lang}/archive/"
        if archive_href not in doc:
            doc = doc.replace("</nav>", f'<a href="{archive_href}">{escape(archive_label)}</a></nav>',1)
        # Add social metadata without duplicating existing properties.
        og_type = (
            "profile" if route == "/about/" else
            "article" if (route.startswith("/blog/") and route != "/blog/") or route in ("/publications/aco-llm/", "/publications/aco-llm-results/") else
            "website"
        )
        image_match = re.search(r'<meta property="og:image" content="([^"]+)"', doc, flags=re.I)
        social_image = image_match.group(1) if image_match else ORIGIN + "/assets/kasem-adra-portrait.jpg"
        image_alt_match = re.search(r'<meta property="og:image:alt" content="([^"]*)"', doc, flags=re.I)
        social_image_alt = image_alt_match.group(1) if image_alt_match else "Portrait of Kasem Adra"
        social = [
            ("og:site_name","Kasem Adra"),("og:title",title),("og:description",desc),
            ("og:type",og_type),
            ("og:url",ORIGIN+f"/{lang}"+route),("og:locale",{"ar":"ar_SY","fr":"fr_FR","en":"en_US"}[lang]),
            ("og:image:alt",social_image_alt),
            ("twitter:card","summary_large_image"),("twitter:title",title),
            ("twitter:description",desc),("twitter:image",social_image),
            ("twitter:image:alt",social_image_alt)
        ]
        for prop,value in social:
            attr = "name" if prop.startswith("twitter:") else "property"
            pattern = rf'<meta {attr}="{re.escape(prop)}" content="[^"]*">'
            tag = f'<meta {attr}="{prop}" content="{escape(value,quote=True)}">'
            doc = meta_replace(doc,pattern,tag)
            if not re.search(pattern,doc,flags=re.I):
                doc = doc.replace("</head>",tag+"</head>",1)
        if public_build:
            # Normalize indexability and canonical metadata on every generated language page.
            doc = re.sub(r'<meta name="robots" content="[^"]*">', "", doc, flags=re.I)
            doc = doc.replace("</head>", '<meta name="robots" content="index,follow"></head>', 1)
            canonical = ORIGIN + f"/{lang}" + route
            doc = re.sub(r'<link rel="canonical" href="[^"]*">', "", doc, flags=re.I)
            doc = doc.replace("</head>", f'<link rel="canonical" href="{canonical}"></head>', 1)

        # One consistent hreflang set per page; x-default is the root language selector.
        alternate_tags = "".join(
            f'<link rel="alternate" hreflang="{other}" href="{ORIGIN}/{other}{route}">'
            for other in LANGS
        ) + f'<link rel="alternate" hreflang="x-default" href="{ORIGIN}/">'
        doc = re.sub(r'<link rel="alternate" hreflang="[^"]+" href="[^"]*">', "", doc, flags=re.I)
        doc = doc.replace("</head>", alternate_tags + "</head>", 1)
        file.write_text(doc,encoding="utf-8")

def write_root_gateway(dist, public_build):
    title = "Kasem Adra | Independent AI Researcher"
    desc = "Official website of Kasem Adra (قاسم عدرا), independent AI researcher studying local language models, AI agents, task verification and ACO-LLM."
    person = dict(PERSON)
    website = {
        "@type":"WebSite","@id":WEBSITE_ID,"url":ORIGIN+"/","name":"Kasem Adra",
        "alternateName":["قاسم عدرا"],
        "description":desc,"inLanguage":["en","ar","fr"],
        "publisher":{"@id":PERSON_ID}
    }
    graph = {"@context":"https://schema.org","@graph":[person,ORGANIZATION,website,{
        "@type":"WebPage","@id":ORIGIN+"/#webpage","url":ORIGIN+"/","name":title,
        "description":desc,"inLanguage":"en","isPartOf":{"@id":WEBSITE_ID},
        "about":{"@id":PERSON_ID},"mainEntity":{"@id":PERSON_ID}
    }]}
    choices = [
        ("English","en","Independent AI researcher · Research, projects and writing"),
        ("العربية","ar","باحث مستقل في الذكاء الاصطناعي · الأبحاث والمشاريع والكتابات"),
        ("Français","fr","Chercheur indépendant en IA · Recherche, projets et écrits")
    ]
    buttons = "".join(f'<a class="language-choice" href="/{lang}/" hreflang="{lang}"><strong>{label}</strong><span>{escape(subtitle)}</span></a>' for label,lang,subtitle in choices)
    index = "index,follow" if public_build else "noindex"
    doc = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title><meta name="description" content="{escape(desc,quote=True)}">
<meta name="robots" content="{index}"><link rel="canonical" href="{ORIGIN}/">
<link rel="alternate" hreflang="en" href="{ORIGIN}/en/"><link rel="alternate" hreflang="ar" href="{ORIGIN}/ar/"><link rel="alternate" hreflang="fr" href="{ORIGIN}/fr/"><link rel="alternate" hreflang="x-default" href="{ORIGIN}/">
<link rel="icon" type="image/png" href="/assets/kasem-calligraphy-transparent.png">
<meta property="og:site_name" content="Kasem Adra"><meta property="og:type" content="website">
<meta property="og:title" content="{escape(title,quote=True)}"><meta property="og:description" content="{escape(desc,quote=True)}">
<meta property="og:url" content="{ORIGIN}/"><meta property="og:locale" content="en_US"><meta property="og:image" content="{ORIGIN}/assets/kasem-adra-portrait.jpg"><meta property="og:image:alt" content="Portrait of Kasem Adra">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{escape(title,quote=True)}"><meta name="twitter:description" content="{escape(desc,quote=True)}"><meta name="twitter:image" content="{ORIGIN}/assets/kasem-adra-portrait.jpg"><meta name="twitter:image:alt" content="Portrait of Kasem Adra">
<script type="application/ld+json">{dumps(graph,ensure_ascii=False,separators=(",",":"))}</script>
<link rel="stylesheet" href="/style.css"></head>
<body><div class="shell"><header><a class="wordmark" href="/">Kasem Adra</a><span>قاسم عدرا</span></header>
<main class="gateway"><figure><img src="/assets/kasem-adra-portrait.jpg" alt="Portrait of Kasem Adra" width="782" height="1024"></figure>
<div><p class="label">{escape(UI["en"]["gateway_label"])}</p><h1>Kasem Adra</h1><p class="gateway-desc">{escape(UI["en"]["gateway_desc"])}</p><h2>{escape(UI["en"]["lang_gateway"])}</h2><div class="language-choices">{buttons}</div></div>
</main><footer><span>Kasem Adra · قاسم عدرا</span><div class="profiles"><a href="{GITHUB}">GitHub</a><a href="{GITHUB_PROJECTS}">Qassem projects</a><a href="{ORCID}">ORCID</a><a href="{LINKEDIN}">LinkedIn</a><a href="{X_PROFILE}">X</a><a href="{INSTAGRAM}">Instagram</a><a href="{QASSEM_SITE}">Qassem.net</a></div></footer></div></body></html>'''
    (dist/"index.html").write_text(doc,encoding="utf-8")

def build_site(dist, origin, public_build):
    # Generate the general research archive index only.
    for lang in LANGS:
        u = UI[lang]
        shell_page(dist,lang,ARCHIVE_ROUTE,u["archive_title"],u["archive_desc"],archive_index_html(lang),public_build)
    # Preserve the root-level research archive alias; its canonical points to /en/.
    route = ARCHIVE_ROUTE
    source = dist / "en" / route.strip("/") / "index.html"
    target = dist / route.strip("/") / "index.html"
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(source.read_text(encoding="utf-8"),encoding="utf-8")
    enrich_existing_pages(dist,public_build)
    write_root_gateway(dist,public_build)
    css = dist / "style.css"
    extra = """
/* Knowledge archive and encyclopedic record layout */
.archive-lead{font-size:1.12rem;max-width:55rem;margin-block:1rem 1.6rem!important}
.archive-card{grid-template-columns:9rem 1fr}
.archive-card h2{font-size:1.35rem;margin:0 0 .25rem}
.archive-infobox{border:1px solid var(--line);padding:1rem 1.2rem;margin:1.5rem 0;max-width:34rem;background:var(--surface)}
.archive-infobox h2{font-size:1.35rem}
.archive-infobox dl{display:grid;grid-template-columns:minmax(7rem,9rem) 1fr;gap:.35rem .8rem;margin:.5rem 0 0}
.archive-infobox dt{font-weight:650;color:var(--muted)}
.archive-infobox dd{margin:0}
.timeline{border-inline-start:2px solid var(--line);margin:1.2rem 0 1.5rem;padding-inline-start:1.1rem}
.timeline-entry{display:grid;grid-template-columns:minmax(8rem,10rem) 1fr;gap:1rem;padding:1rem 0;border-bottom:1px solid var(--line)}
.timeline-date{font-weight:700;color:var(--red)}
.timeline-entry h3{font:600 1.2rem/1.4 var(--serif);margin:0 0 .4rem}
.timeline-entry p{margin:.3rem 0}
.source-basis{font-size:.85rem;color:var(--muted);font-weight:650}
.citation{font-size:.78em;vertical-align:super;margin-inline-start:.12rem}
.citation a{text-decoration:none;color:var(--red)}
.references{padding-inline-start:1.7rem}
.references li{padding:.35rem 0;border-bottom:1px solid var(--line);overflow-wrap:anywhere}
.ref-number{font-weight:700;color:var(--red);margin-inline-end:.3rem}
.gateway{display:grid;grid-template-columns:minmax(10rem,17rem) minmax(0,1fr);gap:2.5rem;align-items:center;padding:3rem 0}
.gateway figure img{width:100%;height:auto;border-radius:.5rem}
.gateway h1{font-size:clamp(3rem,8vw,5.5rem)}
.gateway-desc{color:var(--muted);font-size:1.1rem;max-width:38rem}
.language-choices{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:.8rem;margin-top:1rem}
.language-choice{border:1px solid var(--line);padding:1rem;text-decoration:none;display:flex;flex-direction:column;gap:.35rem;border-radius:.45rem}
.language-choice:hover{border-color:var(--red);color:var(--red)}
.language-choice span{font-size:.9rem;color:var(--muted)}
.toc,.profile-toc{border:1px solid var(--line);padding:1rem 1.25rem;margin:1.5rem 0;max-width:32rem;background:var(--surface)}
.toc h2,.profile-toc h2{font-size:1.35rem;margin:0 0 .45rem}
.toc ol,.profile-toc ol{margin:.25rem 0;padding-inline-start:1.4rem}
.toc li,.profile-toc li{padding:.15rem 0}
.profile-infobox{border:1px solid var(--line);padding:1rem 1.2rem;margin:1.5rem 0;max-width:36rem;background:var(--surface)}
.profile-infobox h2{font-size:1.35rem}
.profile-infobox dl{display:grid;grid-template-columns:minmax(7rem,9rem) 1fr;gap:.35rem .8rem;margin:.5rem 0 0}
.profile-infobox dt{font-weight:650;color:var(--muted)}
.profile-infobox dd{margin:0}
.profile-identifiers{border-top:1px solid var(--line);margin-top:2rem;padding-top:1rem}
.profile-identifiers ul{padding-inline-start:1.4rem}
@media(max-width:680px){.timeline-entry{grid-template-columns:1fr;gap:.25rem}.archive-infobox dl,.profile-infobox dl{grid-template-columns:1fr;gap:.1rem}.archive-infobox dd,.profile-infobox dd{margin-bottom:.55rem}.gateway{grid-template-columns:1fr;gap:1rem}.gateway figure{width:min(100%,12rem);margin-inline:auto}.language-choices{grid-template-columns:1fr}}
"""
    current = css.read_text(encoding="utf-8")
    if "Knowledge archive and encyclopedic record layout" not in current:
        css.write_text(current + "\n" + extra,encoding="utf-8")

def write_sitemap(dist, origin):
    ns = "http://www.sitemaps.org/schemas/sitemap/0.9"
    xns = "http://www.w3.org/1999/xhtml"
    ET.register_namespace("",ns)
    ET.register_namespace("xhtml",xns)
    root = ET.Element(f"{{{ns}}}urlset")
    paths = set()
    for lang in LANGS:
        base = dist / lang
        for file in base.rglob("index.html"):
            route_parts = file.parent.relative_to(base).parts
            route = "/" + "/".join(route_parts) + "/" if route_parts else "/"
            paths.add(route)
    paths.add("/")
    for route in sorted(paths):
        # The root language selector is its own URL; each translated page also gets a URL entry.
        urls_for_route = [origin + "/"] if route == "/" else []
        urls_for_route.extend(origin + f"/{lang}" + route for lang in LANGS)
        for loc in urls_for_route:
            url_node = ET.SubElement(root,f"{{{ns}}}url")
            ET.SubElement(url_node,f"{{{ns}}}loc").text = loc
            for lang in LANGS:
                href = origin + f"/{lang}" + route
                ET.SubElement(url_node,f"{{{xns}}}link",{
                    "rel":"alternate","hreflang":lang,"href":href
                })
            ET.SubElement(url_node,f"{{{xns}}}link",{
                "rel":"alternate","hreflang":"x-default","href":origin+"/"
            })
    ET.ElementTree(root).write(dist/"sitemap.xml",encoding="utf-8",xml_declaration=True)

