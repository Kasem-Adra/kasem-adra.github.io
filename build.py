from pathlib import Path
from base64 import b64decode
from os import environ
from xml.etree.ElementTree import Element, SubElement, ElementTree
from html import escape
from json import dumps, loads
from re import sub
import results
import article_render as article_renderer

public_build = environ.get('SITE_PUBLIC') == '1'
origin = 'https://kasemadra.com'
robots_meta = '' if public_build else '<meta name="robots" content="noindex">'

nav = {'Home':'/', 'Projects':'/projects/', 'Research':'/publications/', 'Blog':'/blog/'}
def read_content(path):
    _, header, body = path.read_text(encoding='utf-8').split('---', 2)
    fields = {}
    for line in header.strip().splitlines():
        key, value = line.split(':', 1)
        fields[key] = loads(value.strip())
    return fields, body.strip()


publication, _ = read_content(Path('_publications/aco-llm.md'))
doi = 'https://doi.org/' + publication['doi']
project = '/projects/local-assistant/'
paper = '/publications/aco-llm/'
note = '/blog/checking-work/'
arabic = '/blog/arabic-calligraphy/'
article = '/blog/local-ai-agent-reliability/'
logo = '/assets/kasem-calligraphy-transparent.png'
paper_title = publication['title']
posts = {}
for path in sorted(Path('_posts').rglob('*.md')):
    fields, content = read_content(path)
    posts[fields['permalink']] = fields, content


def render_post(body, lang, path):
    fields, content = posts[locale_path(lang, path)]
    if path == article:
        article_html, _, _ = article_renderer.render_article(fields, content, lang)
        return sub(r'<main>.*?</main>', lambda _: f'<main>{article_html}</main>', body, count=1, flags=16)
    paragraphs = ''.join(f'<p>{escape(part)}</p>' for part in content.split('\n\n'))
    image = ''
    if 'image' in fields:
        image = f'<img class="article-logo" src="{escape(fields["image"])}" alt="{escape(fields["image_alt"])}" width="1254" height="1254">'
    post_html = f'<h1>{escape(fields["title"])}</h1>{paragraphs}{image}'
    return sub(r'(<div class="subpage"[^>]*>).*?(</div>)', lambda m: m[1] + post_html + m[2], body, count=1, flags=16)


def render_post_cards(body, lang):
    for permalink, (fields, _) in posts.items():
        if fields['lang'] != lang:
            continue
        pattern = f'(<h3><a href="{permalink}">).*?</a></h3><p>.*?</p>'
        card = escape(fields['title']) + '</a></h3><p>' + escape(fields['description']) + '</p>'
        body = sub(pattern, lambda m: m[1] + card, body)
    return body


person = {
    '@context': 'https://schema.org',
    '@type': 'Person',
    '@id': f'{origin}/#person',
    'image': f'{origin}/assets/kasem-adra-portrait.jpg',
    'name': 'Kasem Adra',
    'alternateName': 'قاسم عدرا',
    'url': 'https://kasemadra.com/',
    'jobTitle': 'Independent AI Researcher',
    'description': 'Independent AI researcher based in France studying task verification and error recovery in local AI assistants through ACO-LLM.',
    'sameAs': [
        'https://github.com/Kasem-Adra',
        'https://orcid.org/0009-0004-7615-4978',
    ],
}


results_pdf = '/files/aco-llm-results.pdf'
results_pdf_target = Path('dist' + results_pdf)
results_pdf_target.parent.mkdir(parents=True, exist_ok=True)
results_pdf_target.write_bytes(b64decode(Path('_publications/aco-llm-results.pdf.b64').read_text(encoding='ascii')))
hero_b64 = Path('_posts/assets/local-ai-agent-reliability-hero.webp.b64')
hero_parts = (
    [hero_b64, Path('_posts/assets/local-ai-agent-reliability-hero-part-02.b64')]
    + [Path(f'_posts/assets/local-ai-agent-reliability-hero-part-03{suffix}.b64') for suffix in ('a', 'b', 'c', 'd')]
    + [Path('_posts/assets/local-ai-agent-reliability-hero-part-04.b64')]
)
if all(part.exists() for part in hero_parts):
    hero_data = ''.join(part.read_text(encoding='ascii').strip() for part in hero_parts)
    hero_target = Path('dist/assets/local-ai-agent-reliability-hero.webp')
    hero_target.parent.mkdir(parents=True, exist_ok=True)
    hero_target.write_bytes(b64decode(hero_data))


def row(category, title, description, url, lang='en'):
    attrs = ' lang="ar" dir="rtl"' if lang == 'ar' else ''
    return f'<article><span>{category}</span><div{attrs}><h3><a href="{url}">{title}</a></h3><p>{description}</p></div></article>'

projects = row('PROJECT', 'A local AI assistant for Arabic', 'An on-device assistant for text, speech, and tool use.', project)
research = row('RESEARCH', 'ACO‑LLM', 'A protocol for testing how local models check and repair their work.', paper)
blog = row('FEATURED ARTICLE', 'Can We Trust a Local AI Assistant?', 'An evidence-based guide to local AI, agent reliability, verification, and ACO-LLM.', article) + row('RESEARCH NOTE', 'How do we verify an assistant’s work?', 'A small example of checking outcomes independently of the model.', note) + row('ART & DESIGN', 'حين تصبح الحروف رسمة', 'ملاحظة عن تصميم التوقيع الحروفي للموقع.', arabic, lang='ar')
profile = '<div class="profiles"><a href="https://github.com/Kasem-Adra">GitHub</a><a href="https://orcid.org/0009-0004-7615-4978">ORCID</a><a href="https://zenodo.org/records/24488951">Zenodo</a></div>'

def page(route, title, section, main):
    navigation = ''.join(f'<a href="{url}"'+(' aria-current="page"' if tab==section else '')+f'>{tab}</a>' for tab,url in nav.items())
    metadata = ''
    if route == '/':
        metadata = '<script type="application/ld+json">' + dumps(person, ensure_ascii=False) + '</script>'
    if route == paper:
        citations = {
            'title': paper_title,
            'author': publication['author'],
            'publication_date': publication['publication_date'],
            'doi': publication['doi'],
            'pdf_url': (origin if public_build else 'https://qassem-adra-demo.jerizsdbp9.chatgpt.site') + publication['pdf'],
        }
        metadata = ''.join(
            f'<meta name="citation_{key}" content="{escape(value, quote=True)}">'
            for key, value in citations.items()
        )
    if route == results.PATH:
        citations = {
            'title': 'Adaptive Cognitive Orchestration for Local Language Models: A Held-Out Evaluation of Structural Verification and Repair',
            'author': 'Kasem Adra',
            'publication_date': '2026/11/26',
            'doi': '10.5281/zenodo.24549236',
            'pdf_url': origin + results_pdf,
        }
        metadata = ''.join(
            f'<meta name="citation_{key}" content="{escape(value, quote=True)}">'
            for key, value in citations.items()
        )
    if route in (paper, results.PATH):
        article = {
            '@context': 'https://schema.org',
            '@type': 'ScholarlyArticle',
            '@id': f'{origin}/en{route}#article',
            'headline': paper_title if route == paper else 'ACO-LLM: evaluation results',
            'author': {'@id': person['@id'], 'name': person['name'], '@type': 'Person'},
            'url': f'{origin}/en{route}',
            'sameAs': doi if route == paper else 'https://doi.org/10.5281/zenodo.24549236',
        }
        article['identifier'] = {'@type': 'PropertyValue', 'propertyID': 'DOI', 'value': article['sameAs'].removeprefix('https://doi.org/')}
        if route == paper:
            article['isPartOf'] = {'@id': f'{origin}/en/publications/#collection'}
        else:
            article['isBasedOn'] = doi
            article['isPartOf'] = {'@id': f'{origin}/en/publications/#collection'}
        metadata += '<script type="application/ld+json">' + dumps(article, ensure_ascii=False) + '</script>'
    if route == '/publications/':
        collection = {'@context': 'https://schema.org', '@type': 'CollectionPage',
                      '@id': f'{origin}/en/publications/#collection',
                      'url': f'{origin}/en/publications/', 'about': {'@id': person['@id']}}
        metadata += '<script type="application/ld+json">' + dumps(collection) + '</script>'
    target = Path('dist'+route+'index.html')
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">{robots_meta}<meta name="description" content="Kasem Adra’s portfolio, research, and writing."><title>{title} · Kasem Adra</title>{metadata}<link rel="icon" type="image/png" href="{logo}"><meta property="og:image" content="{origin}/assets/kasem-adra-portrait.jpg"><link rel="stylesheet" href="/style.css"><style>.hero > figure > img {{ transform: scale(.88); }}</style></head>
<body><div class="shell"><header><a class="wordmark" href="/">Kasem Adra</a><nav aria-label="Main navigation">{navigation}</nav></header>
<main>{main}</main><footer><span>Kasem Adra</span>{profile}</footer></div></body></html>''', encoding='utf-8')

page('/', 'Home', 'Home', f'''<div class="hero"><figure><img width="1254" height="1254" src="{logo}" alt="قاسم عدرا — Arabic calligraphy in black with red flourishes"></figure><div class="intro"><p class="label">INDEPENDENT AI RESEARCHER</p><h1>Kasem Adra</h1><p class="bio">I build AI assistants that run locally and study how they can check their work and correct errors as they complete tasks. I’m based in France and build tools that support Arabic.</p>{profile}</div>
</div>
<section><h2>Selected work</h2>{projects}{research}</section><section><h2>Latest writing</h2>{blog}</section>''')
for route, title, section, content in [
    ('/projects/', 'Projects','Projects',projects),
    ('/publications/', 'Research','Research',research),
    ('/blog/', 'Blog','Blog',blog),
    (project, 'A local AI assistant for Arabic','Projects','<p>An experiment in running an assistant on-device with Arabic text and speech. It combines a local language model with tools for carrying out tasks.</p><p><a href="https://github.com/Kasem-Adra">GitHub profile</a></p>'),
    (paper, 'ACO‑LLM','Research',f'<p class="label">RESEARCH PROTOCOL · 2026</p><p>{paper_title}</p><p>The protocol describes a comparison of different ways to route tasks, verify their results, and repair failures under limited computing resources.</p><p><a href="{doi}">Open the protocol on Zenodo</a></p>'),
    (note, 'How do we verify an assistant’s work?','Blog','<p>If an assistant is asked to create a file, we can test the result by inspecting the file and its contents directly. This is one way to evaluate a task independently of the model’s own judgment.</p>'),
    (arabic, 'حين تصبح الحروف رسمة','Blog',f'<p>في هذا التكوين، تمنح امتدادات الحروف الاسم شكله. ويتفرّع الخط الأحمر على طرفه إلى نقطتين صغيرتين تلمّحان إلى التقنية.</p><img class="article-logo" src="{logo}" alt="توقيع قاسم عدرا بالخط العربي" width="1254" height="1254">'),
]:
    attrs = ' lang="ar" dir="rtl"' if route == arabic else ''
    page(route, title, section, f'<div class="subpage"{attrs}><h1>{title}</h1>{content}</div>')

# Each locale shares the same page structure and keeps stable content paths.
translations = {
    'ar': [
        'الرئيسية', 'المشاريع', 'الأبحاث', 'المدونة', 'قاسم عدرا',
        'باحث مستقل في الذكاء الاصطناعي',
        'أبني مساعدين أذكياء يعملون محليًا، وأدرس كيف يمكنهم التحقق من عملهم وتصحيح أخطائهم أثناء تنفيذ المهام. أعمل من فرنسا وأطوّر أدوات تدعم العربية.',
        'أعمال مختارة', 'أحدث المقالات', 'مشروع', 'بحث', 'ملاحظة بحثية', 'فن وتصميم',
        'مساعد ذكاء اصطناعي محلي بالعربية', 'مساعد يعمل على الجهاز ويدعم النص والصوت واستخدام الأدوات.',
        'بروتوكول لاختبار كيفية تحقّق النماذج المحلية من عملها وإصلاح أخطائها.',
        'كيف نتحقّق من عمل المساعد؟', 'مثال بسيط لفحص نتائج المهام بصورة مستقلة عن النموذج.',
        'تجربة لمساعد يعمل على الجهاز ويدعم العربية نصًا وصوتًا. يجمع بين نموذج لغوي محلي وأدوات لتنفيذ المهام.',
        'ملف GitHub', 'بروتوكول بحثي', 'يقارن البروتوكول أساليب توجيه المهام والتحقّق من نتائجها وإصلاح الإخفاقات في ظل موارد حاسوبية محدودة.',
        'اقرأ البروتوكول على Zenodo',
        'عندما يُطلب من المساعد إنشاء ملف، يمكن فحص الملف ومحتواه مباشرة للتحقق من النتيجة. هذه إحدى طرق تقييم المهمة بصورة مستقلة عن حكم النموذج على عمله.',
        'قاسم عدرا بالخط العربي الأسود مع امتدادات حمراء',
        'أبحاث قاسم عدرا ومشاريعه وكتاباته.', 'التنقّل الرئيسي',
    ],
    'fr': [
        'Accueil', 'Projets', 'Recherche', 'Blog', 'Kasem Adra',
        'Chercheur indépendant en IA',
        'Je développe des assistants IA qui fonctionnent en local et j’étudie comment ils peuvent vérifier leur travail et corriger leurs erreurs pendant une tâche. Basé en France, je crée des outils qui prennent en charge l’arabe.',
        'Travaux choisis', 'Derniers articles', 'PROJET', 'RECHERCHE', 'NOTE DE RECHERCHE', 'ART ET DESIGN',
        'Un assistant IA local en arabe', 'Un assistant sur appareil pour le texte, la voix et l’utilisation d’outils.',
        'Un protocole pour évaluer comment les modèles locaux vérifient et corrigent leur travail.',
        'Comment vérifier le travail d’un assistant ?', 'Un exemple de vérification des résultats indépendante du modèle.',
        'Une expérimentation autour d’un assistant sur appareil qui prend en charge l’arabe à l’écrit et à l’oral. Il associe un modèle de langage local à des outils pour exécuter des tâches.',
        'Profil GitHub', 'PROTOCOLE DE RECHERCHE', 'Le protocole compare plusieurs méthodes d’aiguillage des tâches, de vérification des résultats et de correction des erreurs avec des ressources de calcul limitées.',
        'Lire le protocole sur Zenodo',
        'Si l’on demande à un assistant de créer un fichier, on peut vérifier directement le fichier et son contenu. C’est une façon d’évaluer la tâche indépendamment du jugement du modèle.',
        'Calligraphie arabe de Kasem Adra en noir et rouge',
        'Recherches, projets et articles de Kasem Adra.', 'Navigation principale',
    ],
}
source_strings = [
    'Home', 'Projects', 'Research', 'Blog', 'Kasem Adra',
    'INDEPENDENT AI RESEARCHER',
    'I build AI assistants that run locally and study how they can check their work and correct errors as they complete tasks. I’m based in France and build tools that support Arabic.',
    'Selected work', 'Latest writing', 'PROJECT', 'RESEARCH', 'RESEARCH NOTE', 'ART & DESIGN',
    'A local AI assistant for Arabic', 'An on-device assistant for text, speech, and tool use.',
    'A protocol for testing how local models check and repair their work.',
    'How do we verify an assistant’s work?', 'A small example of checking outcomes independently of the model.',
    'An experiment in running an assistant on-device with Arabic text and speech. It combines a local language model with tools for carrying out tasks.',
    'GitHub profile', 'RESEARCH PROTOCOL', 'The protocol describes a comparison of different ways to route tasks, verify their results, and repair failures under limited computing resources.',
    'Open the protocol on Zenodo',
    'If an assistant is asked to create a file, we can test the result by inspecting the file and its contents directly. This is one way to evaluate a task independently of the model’s own judgment.',
    'قاسم عدرا — Arabic calligraphy in black with red flourishes',
    'Kasem Adra’s portfolio, research, and writing.', 'Main navigation',
]

def locale_path(lang, path):
    return f'/{lang}{path}'

biographies = {
    'ar': (
        'أنا قاسم عدرا، من مدينة بانياس الساحلية في سوريا. خرجتُ منها، لكنها لم تخرج مني أبدًا. أعيش اليوم في فرنسا. أدرس علوم الحاسوب والذكاء الاصطناعي، وأحمل ماجستير في إدارة الأعمال (MBA) وماجستير في التسويق الرقمي وتحليل البيانات. أعمل على مشاريع تجمع بين البرمجة وتحليل البيانات، من بينها مساعد ذكي يعمل محليًا ويدعم العربية كتابةً وصوتًا.',
        'في بحثي المستقل، أدرس سؤالًا يهمني كلما استخدمت مساعدًا ذكيًا: كيف أعرف أنه أنجز المهمة فعلًا؟ نشرتُ بروتوكول ACO‑LLM لدراسة كيف يمكن للمساعد التحقق من عمله وتصحيح أخطائه أثناء التنفيذ.',
        'أحب الرسم والخط العربي، ومن هنا جاءت فكرة توقيعي الحروفي في أعلى الموقع. أكتب هنا عن تجاربي مع التقنية وعن مواضيع أخرى تهمّني.',
        'صورة قاسم عدرا',
    ),
    'en': (
        'I’m Kasem Adra, from the coastal city of Baniyas, Syria. I left Baniyas, but it never left me. I now live in France. I study computer science and artificial intelligence, and hold an MBA (Master of Business Administration) and a Master in Digital Marketing and Analytics. I work on projects that bring together programming and data analysis, including a local AI assistant that supports Arabic text and speech.',
        'My independent research starts with a question I ask whenever I use an AI assistant: how do I know it actually completed the task? I published the ACO‑LLM research protocol to study how assistants can check their work and correct errors as they go.',
        'I enjoy drawing and Arabic calligraphy, which inspired the signature at the top of this site. I write here about my experiences with technology and other subjects that interest me.',
        'Portrait of Kasem Adra',
    ),
    'fr': (
        'Je suis Kasem Adra, originaire de Baniyas, une ville côtière de Syrie. J’ai quitté Baniyas, mais elle ne m’a jamais quitté. Je vis aujourd’hui en France. J’étudie l’informatique et l’intelligence artificielle. Je suis titulaire d’un MBA (Master of Business Administration) et d’un master en marketing numérique et analyse de données. Mes projets associent programmation et analyse de données. Parmi eux figure un assistant IA local qui prend en charge l’arabe à l’écrit et à l’oral.',
        'Mes recherches indépendantes partent d’une question que je me pose chaque fois que j’utilise un assistant IA : comment savoir s’il a réellement accompli la tâche ? J’ai publié le protocole ACO‑LLM pour étudier comment ces assistants peuvent vérifier leur travail et corriger leurs erreurs en cours de tâche.',
        'J’aime le dessin et la calligraphie arabe, qui ont inspiré la signature en haut du site. J’écris ici sur mes expériences avec la technologie et sur d’autres sujets qui m’intéressent.',
        'Portrait de Kasem Adra',
    ),
}


about = '/about/'
page(about, 'About', 'Home', '')
page(results.PATH, 'ACO‑LLM results', 'Research', '')
page(article, 'Can We Trust a Local AI Assistant?', 'Blog', '')


def localize_pages():
    import re
    labels = {'en': 'English', 'ar': 'العربية', 'fr': 'Français'}
    language_names = {
        'en': {'en': 'English', 'ar': 'Arabic', 'fr': 'French'},
        'ar': {'en': 'الإنجليزية', 'ar': 'العربية', 'fr': 'الفرنسية'},
        'fr': {'en': 'Anglais', 'ar': 'Arabe', 'fr': 'Français'},
    }
    paths = ('/', *tuple(nav.values())[1:], project, paper, results.PATH, about, note, arabic, article)
    for path in paths:
        base = Path(f'dist{path}index.html').read_text(encoding='utf-8')
        for lang in labels:
            head, body = base.split('<body>', 1)
            if lang != 'en':
                glossary = dict(zip(source_strings, translations[lang], strict=True))
                for original, translated in sorted(glossary.items(), key=lambda pair: -len(pair[0])):
                    body = body.replace(f'>{original}<', f'>{translated}<')
                    if original == 'RESEARCH PROTOCOL':
                        body = body.replace(f'>{original} ·', f'>{translated} ·')
                    body = body.replace(f'"{original}"', f'"{translated}"')
                    head = head.replace(f'<title>{original} ·', f'<title>{translated} ·').replace(f'content="{original}"', f'content="{translated}"') if original != 'Kasem Adra' else head
                head = head.replace('<html lang="en">', f'<html lang="{lang}" dir="{"rtl" if lang == "ar" else "ltr"}">')
            body = re.sub(r'href="(/[^"]*)"', lambda m: f'href="{locale_path(lang, m[1])}"', body)
            if lang == 'en':
                body = body.replace(' lang="ar" dir="rtl"', '')
                for original, translated in {
                    'حين تصبح الحروف رسمة': 'When Letters Become a Drawing',
                    'ملاحظة عن تصميم التوقيع الحروفي للموقع.': 'A note on designing the site’s calligraphic signature.',
                    'في هذا التكوين، تمنح امتدادات الحروف الاسم شكله. ويتفرّع الخط الأحمر على طرفه إلى نقطتين صغيرتين تلمّحان إلى التقنية.': 'In this composition, the extended letterforms give the name its shape. The red stroke splits into two tiny points that evoke electronic contacts.',
                    'توقيع قاسم عدرا بالخط العربي': 'Kasem Adra’s signature in Arabic calligraphy',
                    'قاسم عدرا — Arabic calligraphy in black with red flourishes': 'Kasem Adra’s Arabic calligraphy in black with red flourishes',
                }.items():
                    body = body.replace(original, translated)
                    head = head.replace(original, translated)
            if lang == 'fr':
                body = body.replace(' lang="ar" dir="rtl"', '')
                for original, translated in {
                    'حين تصبح الحروف رسمة': 'Quand les lettres deviennent un dessin',
                    'ملاحظة عن تصميم التوقيع الحروفي للموقع.': 'Une note sur la création de la signature calligraphique du site.',
                    'في هذا التكوين، تمنح امتدادات الحروف الاسم شكله. ويتفرّع الخط الأحمر على طرفه إلى نقطتين صغيرتين تلمّحان إلى التقنية.': 'Dans cette composition, les prolongements des lettres donnent sa forme au nom. Le trait rouge se divise en deux petites branches dont les points évoquent des contacts électroniques.',
                    'توقيع قاسم عدرا بالخط العربي': 'Signature de Kasem Adra en calligraphie arabe',
                }.items():
                    body = body.replace(original, translated)
                    head = head.replace(original, translated)
            if path in (note, arabic, article):
                body = render_post(body, lang, path)
                fields, content = posts[locale_path(lang, path)]
                if path == article:
                    seo_title = fields.get('seo_title', fields['title'] + ' · Kasem Adra')
                    head = sub(r'<title>[^<]*</title>', lambda _: f'<title>{escape(seo_title)}</title>', head)
                    head = sub(r'<meta name="description" content="[^"]*">', lambda _: f'<meta name="description" content="{escape(fields["description"], quote=True)}">', head)
                    head = sub(r'<meta property="og:image"[^>]*>', '', head)
                    _, word_count, reading_time = article_renderer.render_article(fields, content, lang)
                    article_meta = article_renderer.build_article_head(
                        fields, lang, origin + locale_path(lang, path), origin, person, word_count, reading_time
                    )
                    head = head.replace('</head>', article_meta + '</head>')
                else:
                    head = sub(r'<title>[^<]*</title>', lambda _: f'<title>{escape(fields["title"])} · Kasem Adra</title>', head)
            elif path in ('/', '/blog/'):
                body = render_post_cards(body, lang)
            body = body.replace(f'<p>{paper_title}</p>', f'<p lang="en" dir="ltr">{paper_title}</p>')
            switcher = '<div class="languages">' + ''.join(
                f'<a href="{locale_path(other, path)}" hreflang="{other}" aria-label="{language_names[lang][other]}"'
                + (' aria-current="page"' if other == lang else '') + f'>{other.upper()}</a>'
                for other in labels
            ) + '</div>'
            if path == '/':
                *paragraphs, portrait_alt = biographies[lang]
                lead = {
                    'ar': 'أدرس كيف تتحقّق مساعدات الذكاء الاصطناعي المحلية من إنجاز مهامها وتصحّح أخطاءها.',
                    'en': 'I study how local AI assistants verify that they’ve completed tasks and recover from errors.',
                    'fr': 'J’étudie comment les assistants d’IA locaux vérifient qu’ils ont accompli leurs tâches et corrigent leurs erreurs.',
                }[lang]
                paragraphs.insert(0, lead)
                bio = ''.join(f'<p>{escape(paragraph)}</p>' for paragraph in paragraphs)
                portrait = f'<img class="portrait" src="/assets/kasem-adra-portrait.jpg" alt="{escape(portrait_alt, quote=True)}" width="782" height="1024">'
                body = re.sub(r'<p class="bio">.*?</p>', lambda _: f'<div class="bio-panel"><div class="bio">{bio}</div>{portrait}</div>', body, count=1)
            if path == project:
                heading, introduction, steps, research_label = {
                    'en': ('Example: creating a file in Arabic', 'Imagine asking the assistant to create a text file containing «أهلًا من بانياس».', ('The assistant uses a local tool to create the file.', 'The check reads the file back and compares its content with the requested text.', 'If the file is missing or the content differs, the assistant can retry within a set limit and report the actual outcome.'), 'Read the ACO‑LLM protocol'),
                    'ar': ('مثال: إنشاء ملف نصي بالعربية', 'تخيّل أنك تطلب من المساعد إنشاء ملف نصي يحتوي على عبارة «أهلًا من بانياس».', ('يستخدم المساعد أداة محلية لإنشاء الملف.', 'تقرأ خطوة التحقق الملف وتقارن محتواه بالنص المطلوب.', 'إذا غاب الملف أو اختلف المحتوى، يمكن للمساعد إعادة المحاولة ضمن حد محدد والإبلاغ عن النتيجة الفعلية.'), 'اقرأ بروتوكول ACO‑LLM'),
                    'fr': ('Exemple : créer un fichier texte en arabe', 'Imaginez demander à l’assistant de créer un fichier texte contenant « أهلًا من بانياس ».', ('L’assistant utilise un outil local pour créer le fichier.', 'La vérification relit le fichier et compare son contenu au texte demandé.', 'Si le fichier manque ou si le contenu diffère, l’assistant peut réessayer dans une limite définie et indiquer le résultat réel.'), 'Lire le protocole ACO‑LLM'),
                }[lang]
                steps_html = ''.join(f'<li>{escape(step)}</li>' for step in steps)
                example = f'<h2>{escape(heading)}</h2><p>{escape(introduction)}</p><ol>{steps_html}</ol><p><a href="{locale_path(lang, paper)}">{research_label}</a></p>'
                body = body.replace('</div></main>', example + '</div></main>', 1)
            if path == paper:
                label = {'en': 'Download PDF', 'ar': 'تحميل ملف PDF', 'fr': 'Télécharger le PDF'}[lang]
                heading, summary = {
                    'en': ('Protocol summary', 'ACO‑LLM proposes a controller that uses a task contract to choose between direct inference and bounded tool use. Observable failures can trigger limited repair attempts. The evaluation compared it with the fixed-route reference arm with tool support using the same local model and execution budgets, on matched Arabic and English tasks with controlled tool failures. The protocol describes the study design. The evaluation results were published separately.'),
                    'ar': ('ملخّص البروتوكول', 'يقترح ACO‑LLM آلية تستخدم عقد المهمة للاختيار بين الاستدلال المباشر واستخدام الأدوات ضمن حدود محددة، مع محاولات إصلاح محدودة عند رصد إخفاق. وقارن التقييم هذه الآلية بالذراع المرجعية ذات المسار الثابت الداعم للأدوات باستخدام النموذج المحلي نفسه وميزانيات تنفيذ متساوية، على مهام متكافئة بالعربية والإنجليزية مع إدخال أعطال مضبوطة في الأدوات. يصف البروتوكول تصميم الدراسة. ونُشرت نتائج التقييم في ورقة مستقلة.'),
                    'fr': ('Résumé du protocole', 'ACO‑LLM propose un contrôleur qui s’appuie sur un contrat de tâche pour choisir entre inférence directe et usage limité des outils. Une défaillance observable peut déclencher un nombre limité de tentatives de correction. L’évaluation a comparé ce contrôleur au bras de référence utilisant un routage fixe avec accès aux outils, avec le même modèle local et les mêmes budgets, sur des tâches équivalentes en arabe et en anglais avec injection de pannes contrôlées. Le protocole décrit le plan de l’étude. Les résultats de l’évaluation ont été publiés séparément.'),
                }[lang]
                abstract = f'<h2>{heading}</h2><p>{summary}</p>'
                pdf_link = f'<p><a href="{escape(publication["pdf"], quote=True)}">{label} · v1.7</a></p>'
                results_label = {'en': 'Read the separate empirical results paper on Zenodo', 'ar': 'اقرأ ورقة النتائج التجريبية المستقلة على Zenodo', 'fr': 'Lire la publication distincte des résultats empiriques sur Zenodo'}[lang]
                results_link = f'<p><a href="https://doi.org/10.5281/zenodo.24549236">{results_label}</a></p>'
                body = body.replace('</div></main>', abstract + pdf_link + results_link + '</div></main>', 1)
            contact_label = {'en': 'Email', 'ar': 'راسلني', 'fr': 'Contact'}[lang]
            contact_link = f'<a href="mailto:hello@kasemadra.com">{contact_label}</a>'
            body = body.replace('>Zenodo</a></div>', '>Zenodo</a>' + contact_link + '</div>')
            if path == results.PATH:
                body = body.replace('<main></main>', '<main>' + results.render(lang).replace(results.J['pdf'], results_pdf) + '</main>')
                related_labels = {'ar': 'قراءة تحليلية مرتبطة', 'en': 'Related analysis', 'fr': 'Analyse associée'}
                related_titles = {
                    'ar': 'هل يمكن الوثوق بمساعد ذكاء اصطناعي محلي؟',
                    'en': 'Can We Trust a Local AI Assistant?',
                    'fr': 'Peut-on faire confiance à un assistant IA local ?',
                }
                related = (
                    f'<p class="related-article"><span>{related_labels[lang]}:</span> '
                    f'<a href="{locale_path(lang, article)}">{related_titles[lang]}</a></p>'
                )
                body = body.replace('</main>', related + '</main>')
            if path == '/':
                body = sub(r'(<section><h2>[^<]+</h2>.*?)(</section>)', lambda match: match[1] + results.homepage_summary(lang) + match[2], body, count=1)
            if path == paper:
                label = {'en':'View evaluation results','ar':'اطّلع على نتائج التقييم','fr':'Voir les résultats de l’évaluation'}[lang]
                related_labels = {'ar': 'قراءة تحليلية مرتبطة', 'en': 'Related analysis', 'fr': 'Analyse associée'}
                related_titles = {
                    'ar': 'هل يمكن الوثوق بمساعد ذكاء اصطناعي محلي؟',
                    'en': 'Can We Trust a Local AI Assistant?',
                    'fr': 'Peut-on faire confiance à un assistant IA local ?',
                }
                related = (
                    f'<p class="related-article"><span>{related_labels[lang]}:</span> '
                    f'<a href="{locale_path(lang, article)}">{related_titles[lang]}</a></p>'
                )
                body = body.replace('</div></main>', f'<p><a href="{locale_path(lang, results.PATH)}">{label}</a></p>' + related + '</div></main>', 1)
            if path == '/projects/':
                project_cards = {
                    'ar': (('توقّع هبوط المرحلة الأولى من Falcon 9', 'مشروع تدريبي في علم البيانات يجمع بيانات الإطلاق ويحللها باستخدام SQL والرسوم والخرائط، ثم يختبر نماذج لتصنيف نتيجة الهبوط.'), ('استخراج بيانات الأسهم وعرضها', 'ستة دفاتر Jupyter من تدريب IBM في علم البيانات لاستخراج بيانات أسهم Tesla وGameStop وإيراداتهما وعرضها بيانيًا.')),
                    'en': (('Falcon 9 landing prediction', 'A data science coursework project that collects and explores launch data with SQL, charts, and maps, then tests classifiers for first-stage landing outcomes.'), ('Extracting and visualizing stock data', 'Six Jupyter notebooks from IBM Data Science coursework that collect and chart stock and revenue data for Tesla and GameStop.')),
                    'fr': (('Prédiction de l’atterrissage de Falcon 9', 'Un projet de formation en science des données qui collecte et explore les données de lancement avec SQL, des graphiques et des cartes, puis teste des modèles de classification des atterrissages.'), ('Extraction et visualisation de données boursières', 'Six notebooks Jupyter du cursus IBM Data Science pour collecter et visualiser les cours et les revenus de Tesla et GameStop.')),
                }[lang]
                project_repos = ('SpaceX-Falcon9-Landing-Prediction', 'Extracting-Visualizing-Stock-Data')
                cards = ''.join(
                    row('GitHub', escape(name), escape(description), f'https://github.com/Kasem-Adra/{repo}')
                    for (name, description), repo in zip(project_cards, project_repos, strict=True)
                )
                body = body.replace('</div></main>', cards + '</div></main>', 1)
            if path == '/publications/':
                category, card_title, card_description = {
                    'en': ('PREPRINT', 'ACO‑LLM evaluation results', 'Results from the held-out evaluation of structural verification and repair.'),
                    'ar': ('ورقة أولية', 'نتائج تقييم ACO‑LLM', 'نتائج تقييم التحقق البنيوي والإصلاح على مجموعة مهام مستقلة عن التجربة التمهيدية.'),
                    'fr': ('PRÉPUBLICATION', 'Résultats de l’évaluation ACO‑LLM', 'Résultats de l’évaluation de la vérification structurelle et de la réparation sur des tâches réservées au test.'),
                }[lang]
                overview, protocol_label, results_label, pdf_label = {
                    'ar': ('قاسم عدرا (Kasem Adra) باحث مستقل يدرس كيف تتحقق المساعدات الذكية المحلية من إنجاز المهام وتتعافى من الأخطاء. اختبرت دراسة ACO-LLM هذه الآليات على مهام بالعربية والإنجليزية باستخدام نموذج محلي واحد وأدوات محاكاة.', 'البروتوكول البحثي', 'ورقة نتائج التقييم', 'النص الكامل'),
                    'en': ('Kasem Adra (قاسم عدرا) is an independent researcher studying how local AI assistants verify task completion and recover from errors. The ACO-LLM evaluation tested these mechanisms on Arabic and English tasks using one local model and simulated tools.', 'Research protocol', 'Evaluation results paper', 'Full text'),
                    'fr': ('Kasem Adra (قاسم عدرا) étudie en tant que chercheur indépendant comment les assistants d’IA locaux vérifient l’exécution des tâches et corrigent leurs erreurs. L’étude ACO-LLM évalue ces mécanismes sur des tâches en arabe et en anglais, avec un seul modèle local et des outils simulés.', 'Protocole de recherche', 'Article de résultats', 'Texte intégral'),
                }[lang]
                works = (
                    (protocol_label, paper, publication['doi'], publication['pdf']),
                    (results_label, results.PATH, '10.5281/zenodo.24549236', results_pdf),
                )
                links = ''.join(
                    f'<li><a href="{locale_path(lang, route)}">{label}</a> · '
                    f'<a href="https://doi.org/{work_doi}">DOI: {work_doi}</a> · '
                    f'<a href="{escape(pdf, quote=True)}">{pdf_label} (PDF)</a></li>'
                    for label, route, work_doi, pdf in works
                )
                summary = f'<p>{escape(overview)}</p><ul>{links}</ul><p><a href="https://orcid.org/0009-0004-7615-4978">ORCID · Kasem Adra</a></p>'
                body = body.replace('</h1>', '</h1>' + summary, 1)
                card = row(category, card_title, card_description, locale_path(lang, results.PATH))
                body = body.replace('</div></main>', card + '</div></main>', 1)
            about_title, membership = {
                'en': ('About', 'Member of the Association nationale de l’intelligence artificielle (ANIA), France.'),
                'ar': ('عني', 'عضو في الجمعية الوطنية للذكاء الاصطناعي (ANIA)، فرنسا.'),
                'fr': ('À propos', 'Membre de l’Association nationale de l’intelligence artificielle (ANIA).'),
            }[lang]
            about_link = f'<a href="{locale_path(lang, about)}">{about_title}</a>'
            body = body.replace('</nav></header>', about_link + '</nav></header>', 1)
            if path == about:
                *bio, portrait_alt = biographies[lang]
                paragraphs = ''.join(f'<p>{escape(paragraph)}</p>' for paragraph in bio)
                portrait = f'<img class="portrait" src="/assets/kasem-adra-portrait.jpg" alt="{escape(portrait_alt, quote=True)}" width="782" height="1024" style="width:min(160px,100%);height:auto">'
                identity = {k: v for k, v in person.items() if k != '@context'}
                identity['name'], identity['alternateName'] = ('قاسم عدرا', 'Kasem Adra') if lang == 'ar' else ('Kasem Adra', 'قاسم عدرا')
                profile_page = {
                    '@context': 'https://schema.org', '@type': 'ProfilePage',
                    'url': origin + locale_path(lang, path), 'inLanguage': lang,
                    'mainEntity': identity,
                }
                head = head.replace('</head>', '<script type="application/ld+json">' + dumps(profile_page, ensure_ascii=False) + '</script></head>')
                research_label = {'en': 'ACO-LLM research', 'ar': 'أبحاث ACO-LLM', 'fr': 'Recherche ACO-LLM'}[lang]
                research_links = f'<p><a href="{locale_path(lang, paper)}">{research_label}</a></p>'
                identity_links = '<div class="profiles">' + ''.join(f'<a href="{url}">{label}</a>' for label, url in [('ORCID', 'https://orcid.org/0009-0004-7615-4978'), ('GitHub', 'https://github.com/Kasem-Adra')]) + '</div>'
                body = body.replace('<main></main>', f'<main><div class="subpage"><h1>{about_title} · {identity["name"]}</h1><p>{identity["alternateName"]}</p>{portrait}{paragraphs}<p>{membership}</p>{identity_links}{research_links}</div></main>')
                head = sub(r'<title>[^<]*</title>', lambda _: '<title>قاسم عدرا | نبذة عني</title>' if lang == 'ar' else f'<title>{about_title} · Kasem Adra</title>', head)
            theme_label = {'en': 'Dark mode', 'ar': 'الوضع الداكن', 'fr': 'Mode sombre'}[lang]
            theme_button = f'<button class="theme-toggle" type="button" aria-label="{theme_label}" aria-pressed="false" hidden><span aria-hidden="true"></span></button>'
            body = body.replace('</nav></header>', f'</nav><div class="header-controls">{switcher}{theme_button}</div></header>')
            head = head.replace('<link rel="stylesheet"', '<script src="/theme.js"></script><link rel="stylesheet"', 1)
            alternates = ''.join(f'<link rel="alternate" hreflang="{other}" href="https://kasemadra.com{locale_path(other, path)}">' for other in labels)
            alternates += f'<link rel="alternate" hreflang="x-default" href="{origin}{locale_path("en", path)}">'
            if public_build:
                canonical = origin + locale_path(lang, path)
                alternates += f'<link rel="canonical" href="{canonical}">'
            output = Path(f'dist{locale_path(lang, path)}index.html')
            output.parent.mkdir(parents=True, exist_ok=True)
            if path == '/':
                title, description = {
                    'en': ('Kasem Adra | Independent AI Researcher', 'Kasem Adra is an independent AI researcher in France. Explore his work on local AI assistants, the ACO‑LLM protocol, and Arabic calligraphy.'),
                    'ar': ('قاسم عدرا | باحث مستقل في الذكاء الاصطناعي', 'قاسم عدرا، باحث مستقل في الذكاء الاصطناعي من بانياس ويعيش في فرنسا. تعرّف على مشاريعه في الذكاء الاصطناعي المحلي وبروتوكول ACO‑LLM وكتاباته عن الخط العربي.'),
                    'fr': ('Kasem Adra | Chercheur indépendant en intelligence artificielle', 'Kasem Adra est chercheur indépendant en IA en France. Découvrez ses projets sur les assistants IA locaux, le protocole ACO‑LLM et ses articles sur la calligraphie arabe.'),
                }[lang]
                head = sub(r'<title>[^<]*</title>', lambda _: f'<title>{escape(title)}</title>', head)
                head = sub(r'<meta name="description" content="[^"]*">', lambda _: f'<meta name="description" content="{escape(description, quote=True)}">', head)
            if path == results.PATH:
                head = sub(r'<title>[^<]*</title>', lambda _: f'<title>{escape(results.T[lang]["title"])}</title>', head)
                head = sub(r'<meta name="description" content="[^"]*">', lambda _: f'<meta name="description" content="{escape(results.description(lang), quote=True)}">', head)
            rendered = head.replace('</head>', f'{alternates}</head>') + '<body>' + body
            output.write_text(rendered, encoding='utf-8')
            if lang == 'en':
                Path(f'dist{path}index.html').write_text(rendered, encoding='utf-8')

localize_pages()

import knowledge
knowledge.build_site(Path('dist'), origin, public_build)

sitemap_path = Path('dist/sitemap.xml')
if public_build:
    root = Element('urlset', xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')
    for path in sorted(path for lang in ('en', 'ar', 'fr') for path in (Path('dist') / lang).rglob('index.html')):
        relative = path.parent.relative_to('dist')
        suffix = '/' if relative == Path('.') else f'/{relative.as_posix()}/'
        SubElement(SubElement(root, 'url'), 'loc').text = origin + suffix
    ElementTree(root).write(sitemap_path, encoding='utf-8', xml_declaration=True)
    Path('dist/robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {origin}/sitemap.xml\n')
else:
    sitemap_path.unlink(missing_ok=True)
    Path('dist/robots.txt').write_text('User-agent: *\nDisallow: /\n')

if public_build:
    knowledge.write_sitemap(Path('dist'), origin)

