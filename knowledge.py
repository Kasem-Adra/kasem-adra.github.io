from pathlib import Path
from html import escape
from json import dumps
import re
import xml.etree.ElementTree as ET

ORIGIN = "https://kasemadra.com"
PERSON_ID = ORIGIN + "/#person"
WEBSITE_ID = ORIGIN + "/#website"
LANGS = ("en", "ar", "fr")
LINKEDIN = "https://www.linkedin.com/in/kasem-adra/"
GITHUB = "https://github.com/Kasem-Adra"
ORCID = "https://orcid.org/0009-0004-7615-4978"
PROTOCOL_DOI = "https://doi.org/10.5281/zenodo.24488951"
RESULTS_DOI = "https://doi.org/10.5281/zenodo.24549236"
ARCHIVE_ROUTE = "/archive/"
BANIYAS_ROUTE = "/archive/baniyas-revolution-2010-2025/"

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
        "value": "0009-0004-7615-4978"
    },
    "sameAs": [GITHUB, ORCID, LINKEDIN],
    "knowsAbout": [
        "Local artificial intelligence assistants",
        "Large language model evaluation",
        "Task completion verification",
        "Tool use and error recovery in AI agents",
        "Arabic language technology",
        "Baniyas local history and archival documentation"
    ],
    "subjectOf": [
        {"@type": "ScholarlyArticle", "@id": PROTOCOL_DOI, "url": PROTOCOL_DOI},
        {"@type": "ScholarlyArticle", "@id": RESULTS_DOI, "url": RESULTS_DOI}
    ]
}

UI = {
    "en": {
        "home": "Home", "projects": "Projects", "research": "Research", "writing": "Writing",
        "about": "About", "archive": "Archive", "contact": "Contact",
        "archive_title": "Research and historical archive",
        "archive_desc": "A structured index of Kasem Adra’s research, projects, writing and documentary records, with dates, provenance and references.",
        "archive_intro": "This archive brings together research records, projects, writing and documentary material associated with Kasem Adra. Entries identify their authorship and distinguish personal testimony, local archival material and independently published sources.",
        "baniyas_title": "Baniyas: A Revolution and a National Memory (2010–2025)",
        "baniyas_desc": "A source-linked documentary chronology of Baniyas from the early local protests of 2010–2011 through the events of 2013, displacement, the return of 2024 and the community events of 2025.",
        "baniyas_intro": "This chronology documents key events in Baniyas and nearby communities from late 2010 to November 2025. It was prepared by Kasem Adra from local testimony and archival material, alongside human-rights, press and institutional reporting.",
        "infobox": "Archive record",
        "period": "Period", "place": "Place", "compiler": "Prepared and documented by", "source_edition": "Source edition", "contents": "Contents", "overview": "Overview",
        "coverage": "Coverage", "sources": "Sources and references", "method": "Method and source policy",
        "method_text": "This is an authored documentary chronology, not an independent investigation or a neutral third-party biography. It combines local testimony, the author’s photographic and video archive, and independently published human-rights, journalistic and institutional sources. Each entry identifies its evidentiary basis. Where reports give different victim counts, their figures are kept attributed to their respective sources rather than merged. Events supported only by local testimony are labelled as such.",
        "timeline": "Chronology", "related": "Related pages", "references": "References",
        "basis_independent": "Independent reporting / public record",
        "basis_local": "Local testimony / author archive",
        "basis_mixed": "Mixed: independent reporting and local testimony",
        "source_local": "Local primary testimony",
        "last_reviewed": "Editorial review",
        "review_date": "27 November 2026",
        "note": "Editorial note",
        "note_text": "This page is a structured summary of the author’s 37-page working chronology. It does not replace the original records or the full source documents. The source list preserves the distinctions and limitations stated in that chronology.",
        "research_archive": "Research archive",
        "protocol_title": "ACO-LLM research protocol",
        "results_title": "ACO-LLM evaluation results",
        "writing_archive": "Writing and research notes",
        "projects_archive": "Projects",
        "profile_archive": "Author profile",
        "open": "Open record",
        "about_archive": "About this archive",
        "about_archive_text": "The site uses one consistent author identity across its multilingual profile, research records and archive.",
        "lang_gateway": "Choose a language",
        "gateway_label": "Official multilingual profile and knowledge archive",
        "gateway_desc": "Research, projects, writing and historical documentation by Kasem Adra.",
        "language_en": "English", "language_ar": "العربية", "language_fr": "Français",
        "footer": "Official website of Kasem Adra",
        "source_unavailable": "Bibliographic details are incomplete in the cited working copy."
    },
    "ar": {
        "home": "الرئيسية", "projects": "المشاريع", "research": "الأبحاث", "writing": "الكتابات",
        "about": "عني", "archive": "الأرشيف", "contact": "تواصل",
        "archive_title": "الأرشيف البحثي والتاريخي",
        "archive_desc": "فهرس منظم لأبحاث قاسم عدرا ومشاريعه وكتاباته والمواد الوثائقية، مع التواريخ وبيانات المصدر والمراجع.",
        "archive_intro": "يجمع هذا الأرشيف السجلات البحثية والمشاريع والكتابات والمواد الوثائقية المرتبطة بقاسم عدرا. وتوضح كل مادة صاحبها ومصدرها، مع التمييز بين الشهادة الشخصية والتوثيق المحلي والمصادر المنشورة المستقلة.",
        "baniyas_title": "بانياس: حكاية ثورة وذاكرة وطن (2010–2025)",
        "baniyas_desc": "خط زمني وثائقي موثق بالمصادر لأحداث بانياس من إرهاصات الحراك في 2010–2011 إلى أحداث 2013 والتهجير والعودة في 2024 ومحطات 2025.",
        "baniyas_intro": "يوثق هذا الخط الزمني أبرز محطات بانياس وقراها من أواخر عام 2010 حتى تشرين الثاني 2025. أعدّه ووثّقه قاسم عدرا بالاستناد إلى الشهادات المحلية والأرشيف، إلى جانب التقارير الحقوقية والصحفية والمؤسسية المنشورة.",
        "infobox": "بطاقة الأرشيف",
        "period": "الفترة", "place": "المكان", "compiler": "الإعداد والتوثيق", "source_edition": "نسخة المصدر", "contents": "المحتويات", "overview": "نظرة عامة",
        "coverage": "نطاق التوثيق", "sources": "المصادر والمراجع", "method": "المنهجية وسياسة المصادر",
        "method_text": "هذا خط زمني وثائقي أعدّه مؤلفه، وليس تحقيقًا مستقلاً أو سيرة محايدة كتبها طرف ثالث. يجمع بين الشهادة المحلية والأرشيف الفوتوغرافي والمرئي للمؤلف والتقارير الحقوقية والصحفية والمؤسسية المنشورة. ويُبيّن كل مدخل أساسه التوثيقي. وعندما تختلف التقارير في أعداد الضحايا، تُحفظ الأرقام منسوبة إلى مصادرها ولا تُدمج في حصيلة واحدة. أما الوقائع التي لا يسندها سوى التوثيق المحلي فتُوسم بوضوح على هذا الأساس.",
        "timeline": "التسلسل الزمني", "related": "صفحات ذات صلة", "references": "المراجع",
        "basis_independent": "تقارير مستقلة / سجل منشور",
        "basis_local": "شهادة محلية / أرشيف المؤلف",
        "basis_mixed": "مصادر مختلطة: تقارير مستقلة وشهادة محلية",
        "source_local": "شهادة محلية أولية",
        "last_reviewed": "المراجعة التحريرية",
        "review_date": "27 تشرين الثاني 2026",
        "note": "ملاحظة تحريرية",
        "note_text": "هذه الصفحة خلاصة منظمة للنسخة العملية المؤلفة من 37 صفحة. وهي لا تحل محل السجلات الأصلية أو الوثائق الكاملة. وتحافظ قائمة المراجع على الفروق والقيود الواردة في التسلسل الزمني الأصلي.",
        "research_archive": "الأرشيف البحثي",
        "protocol_title": "بروتوكول ACO-LLM البحثي",
        "results_title": "نتائج تقييم ACO-LLM",
        "writing_archive": "الكتابات والملاحظات البحثية",
        "projects_archive": "المشاريع",
        "profile_archive": "صفحة المؤلف",
        "open": "فتح السجل",
        "about_archive": "حول هذا الأرشيف",
        "about_archive_text": "يعتمد الموقع هوية موحدة للمؤلف عبر الملف التعريفي متعدد اللغات والسجلات البحثية والأرشيف.",
        "lang_gateway": "اختر اللغة",
        "gateway_label": "الملف التعريفي والأرشيف المعرفي الرسمي",
        "gateway_desc": "أبحاث ومشاريع وكتابات وتوثيق تاريخي من إعداد قاسم عدرا.",
        "language_en": "English", "language_ar": "العربية", "language_fr": "Français",
        "footer": "الموقع الرسمي لقاسم عدرا",
        "source_unavailable": "بيانات النشر غير مكتملة في النسخة العملية المشار إليها."
    },
    "fr": {
        "home": "Accueil", "projects": "Projets", "research": "Recherche", "writing": "Écrits",
        "about": "À propos", "archive": "Archives", "contact": "Contact",
        "archive_title": "Archives de recherche et de documentation",
        "archive_desc": "Un index structuré des recherches, projets, écrits et documents de Kasem Adra, avec dates, provenance et références.",
        "archive_intro": "Ces archives réunissent les travaux de recherche, projets, écrits et documents associés à Kasem Adra. Chaque entrée précise son auteur et distingue les témoignages personnels, les archives locales et les sources indépendantes publiées.",
        "baniyas_title": "Baniyas : récit d’une révolution et mémoire nationale (2010–2025)",
        "baniyas_desc": "Une chronologie documentaire référencée de Baniyas, des premiers mouvements locaux de 2010–2011 aux événements de 2013, au déplacement, au retour de 2024 et aux événements communautaires de 2025.",
        "baniyas_intro": "Cette chronologie documente les principaux événements de Baniyas et des localités voisines de la fin de 2010 à novembre 2025. Elle a été préparée par Kasem Adra à partir de témoignages locaux et d’archives, ainsi que de rapports publiés par des organisations de défense des droits humains, des médias et des institutions.",
        "infobox": "Fiche d’archive",
        "period": "Période", "place": "Lieu", "compiler": "Préparation et documentation", "source_edition": "Version source", "contents": "Sommaire", "overview": "Présentation",
        "coverage": "Périmètre", "sources": "Sources et références", "method": "Méthode et politique des sources",
        "method_text": "Il s’agit d’une chronologie documentaire rédigée par son auteur, et non d’une enquête indépendante ni d’une biographie neutre produite par un tiers. Elle combine des témoignages locaux, les archives photographiques et vidéo de l’auteur, ainsi que des rapports publiés par des organisations de défense des droits humains, des médias et des institutions. Chaque entrée précise sa base documentaire. Lorsque les rapports divergent sur le nombre de victimes, les chiffres restent attribués à leurs sources respectives et ne sont pas fusionnés. Les événements reposant uniquement sur des témoignages locaux sont signalés comme tels.",
        "timeline": "Chronologie", "related": "Pages connexes", "references": "Références",
        "basis_independent": "Sources indépendantes / archives publiques",
        "basis_local": "Témoignage local / archives de l’auteur",
        "basis_mixed": "Sources mixtes : rapports indépendants et témoignages locaux",
        "source_local": "Témoignage primaire local",
        "last_reviewed": "Révision éditoriale",
        "review_date": "27 novembre 2026",
        "note": "Note éditoriale",
        "note_text": "Cette page est une synthèse structurée de la version de travail de 37 pages rédigée par l’auteur. Elle ne remplace ni les archives originales ni les documents complets. La bibliographie conserve les distinctions et limites indiquées dans la chronologie source.",
        "research_archive": "Archives de recherche",
        "protocol_title": "Protocole de recherche ACO-LLM",
        "results_title": "Résultats de l’évaluation ACO-LLM",
        "writing_archive": "Écrits et notes de recherche",
        "projects_archive": "Projets",
        "profile_archive": "Profil de l’auteur",
        "open": "Consulter la fiche",
        "about_archive": "À propos de ces archives",
        "about_archive_text": "Le site utilise une identité d’auteur cohérente dans son profil multilingue, ses publications de recherche et ses archives.",
        "lang_gateway": "Choisir une langue",
        "gateway_label": "Profil multilingue officiel et archives de connaissances",
        "gateway_desc": "Recherches, projets, écrits et documentation historique de Kasem Adra.",
        "language_en": "English", "language_ar": "العربية", "language_fr": "Français",
        "footer": "Site officiel de Kasem Adra",
        "source_unavailable": "Les informations bibliographiques sont incomplètes dans la copie de travail citée."
    }
}

SOURCES = [
    (1, "The Guardian / Associated Press, “Syria bans niqab from universities”, 20 July 2010.", "https://www.theguardian.com/world/2010/jul/20/syria-bans-niqab-from-universities"),
    (2, "Kasem Adra, “وردة الدم: حكاية ثورة بانياس” — local testimony and the principal local narrative source. Publication details are incomplete in the cited working copy.", None),
    (3, "Office of the UN High Commissioner for Human Rights, Report on the situation of human rights in the Syrian Arab Republic, A/HRC/18/53, 15 September 2011, para. 59.", "https://digitallibrary.un.org/record/710844/files/A_HRC_18_53-EN.pdf"),
    (4, "Fredrick Kunkle, The Washington Post, “Syria forces move into seaport…”, 11 April 2011.", "https://www.washingtonpost.com/world/violent-protest-continues-in-syria-spreads-to-university-in-capital/2011/04/11/AFV99MLD_story.html"),
    (5, "Zeina Karam, The Washington Post, “In new protest, Syrian women block main highway”, 13 April 2011.", "https://www.washingtonpost.com/world/in-new-protest-syrian-women-block-main-highway/2011/04/13/AFn4eJZD_story.html"),
    (6, "Damascus Bureau, “Syrian Revolution Digest, April 9, 2011”.", "https://www.damascusbureau.org/p-2077/"),
    (7, "Syrian Memory, “Baniyas raises flowers in Friday of anger”, 29 April 2011; the chronology also compares contemporary press estimates.", "https://syrianmemory.org/daily-events/event/5ec11beece8f760001028c5c"),
    (8, "Syrian Memory, “Syrian forces storm Baniyas and kill civilians”, 7 May 2011.", "https://syrianmemory.org/daily-events/event/5eb544b50e607900012d63b3"),
    (9, "Syrian Memory, “Baniyas: protests continue and Ahmad al-Biyasi confirms the Bayda incident”, 16 April 2011.", "https://syrianmemory.org/daily-events/event/60199ba46c363b000110068c"),
    (10, "Human Rights Watch, “No One’s Left: Summary Executions by Syrian Forces in al-Bayda and Baniyas”, 13 September 2013.", "https://www.hrw.org/report/2013/09/13/no-ones-left/summary-executions-syrian-forces-al-bayda-and-baniyas"),
    (11, "Independent International Commission of Inquiry on the Syrian Arab Republic, A/HRC/24/46, 16 August 2013, Annex II.", "https://documents.un.org/api/symbol/access?l=en&s=A%2FHRC%2F24%2F46&t=pdf"),
    (12, "Amnesty International, “Syria: Civilians in al-Baydah and Banias exposed to summary executions”, MDE 24/037/2013, 26 July 2013.", "https://www.amnesty.org/en/wp-content/uploads/2021/06/mde240372013en.pdf"),
    (13, "Al Jazeera Arabic, “مجازر بانياس: حين ذُبح الأطفال في أحضان…”, 3 May 2026; later reporting cited for the separate al-Bustan episode.", "https://www.aljazeera.net/encyclopedia/2026/5/3/مجازر-بانياس-حين-ذبح-الأطفال-في-أحضان"),
    (14, "United Nations Office at Geneva, press briefing, 11 March 2025.", "https://www.ungeneva.org/en/news-media/press-briefing/2025/03/un-geneva-press-briefing-1"),
    (15, "Independent International Commission of Inquiry on Syria, A/HRC/59/CRP.4, August 2025; OHCHR statement of 14 August 2025.", "https://www.ecoi.net/en/file/local/2132228/a-hrc-59-crp4-en.pdf"),
    (16, "Samer Abbas, Arab Reform Initiative, “Alawite disparities in relation to the state and the fallout of 6 March”, 7 May 2025.", "https://www.arab-reform.net/publication/alawite-disparities-in-relation-to-the-state-and-the-fallout-of-6-march/"),
    (17, "Syria 360, report quoting the administrative director of Baniyas National Hospital, 9 March 2025.", "https://syria-360.com/2025/03/09/مدير-مشفى-بانياس-فلول-الأسد-نفذوا-إعدامات-ميدانية-بحق-حراسة-المشفى/"),
    (18, "Hélène Sallon, Le Monde, “In Baniyas, Syria, a Sunni man who saved Alawites from a massacre speaks”, 17 March 2025.", "https://www.lemonde.fr/en/international/article/2025/03/17/in-baniyas-syria-the-story-of-a-sunni-who-saved-alawites-from-massacre-we-acted-out-of-simple-humanity_6739222_4.html"),
    (19, "Associated Press, “How it happened: Two seismic weeks that toppled Syria’s government”, December 2024.", "https://apnews.com/article/8c54a8b97803d4b10cde53b97227128e"),
    (20, "Syrian Arab News Agency, “Syrians mark ‘Deterring the Aggression’ with mass events across the country”, 28 November 2025.", "https://sana.sy/en/politics/2280429/"),
    (21, "Amnesty International, “Syria: death toll rises as city is placed under siege”, 9 May 2011.", "https://www.amnesty.org/en/latest/news/2011/05/syria-death-toll-rises-city-placed-under-siege/"),
    (22, "Alkarama, “List of 59 individuals killed during the demonstrations in Syria”, 10 May 2011.", "https://www.alkarama.org/sites/default/files/documents/20114414-4466_excel_table_53_syrian_demonstrators_killed_syr_sumx_100511_finale-2.pdf"),
    (23, "Los Angeles Times, “Activists report security forces kill three women in Baniyas”, 7 May 2011.", "https://www.latimes.com/archives/blogs/babylon-beyond/story/2011-05-07/syria-activists-report-security-forces-kill-three-women-in-baniyas"),
    (24, "Syrian Network for Human Rights, preliminary report on violations following attacks by armed groups linked to the Assad regime, 11 March 2025.", "https://snhr.org/arabic/wp-content/uploads/sites/2/2025/03/R250305A-2.pdf"),
    (25, "Amnesty International, “Syria: Coastal massacres of Alawite civilians must be investigated as war crimes”, 3 April 2025.", "https://www.amnesty.org/en/latest/news/2025/04/syria-coastal-massacres-of-alawite-civilians-must-be-investigated-as-war-crimes/"),
    (26, "Al Jazeera English, “Deaths reported as Syrian forces storm city”, 7 May 2011.", "https://www.aljazeera.com/amp/news/2011/5/7/deaths-reported-as-syrian-forces-storm-city")
]

EVENTS = [
    {
        "date": {"ar":"أواخر 2010","en":"Late 2010","fr":"Fin 2010"},
        "title": {"ar":"ثانوية عماد عرنوق والاعتراض على الإهانة","en":"Imad Arnous Secondary School and an early protest against humiliation","fr":"Le lycée Imad Arnous et une première contestation de l’humiliation"},
        "text": {
            "ar":"تسجل الشهادة المحلية واقعة عند بوابة ثانوية عماد عرنوق في سياق القرارات المتعلقة بالنقاب ونقل بعض المعلمات إلى وظائف إدارية. وتوثق التغطية المستقلة السياق الأوسع للسياسة؛ أما الحادثة المحددة عند بوابة المدرسة فتبقى منسوبة إلى شهادة قاسم عدرا.",
            "en":"The local testimony records an incident at the gate of Imad Arnous Secondary School amid policies concerning the niqab and the reassignment of some teachers. Independent reporting documents the wider policy context; the specific school-gate incident remains attributed to Kasem Adra’s testimony.",
            "fr":"Le témoignage local rapporte un incident à l’entrée du lycée Imad Arnous dans le contexte des décisions concernant le niqab et la réaffectation de certaines enseignantes. La presse indépendante documente le contexte général de ces mesures ; l’incident précis à l’entrée de l’établissement reste attribué au témoignage de Kasem Adra."
        }, "sources":[1,2], "basis":"mixed"
    },
    {
        "date":{"ar":"11 آذار 2011","en":"11 March 2011","fr":"11 mars 2011"},
        "title":{"ar":"خطبة جامع الرحمن","en":"The sermon at al-Rahman Mosque","fr":"Le sermon de la mosquée al-Rahman"},
        "text":{
            "ar":"تصف الرواية المحلية خطبة الجمعة في جامع الرحمن، التي انتقلت من موضوع ديني إلى عرض مطالب إصلاحية محلية تتعلق بالحياة المدرسية والخدمات العامة. وتُعرض تفاصيل الحوار والمطالب هنا بوصفها شهادة محلية.",
            "en":"The local account describes a Friday sermon at al-Rahman Mosque that moved from a religious subject to local reform demands concerning schools and public services. The detailed dialogue and demands are presented as local testimony.",
            "fr":"Le récit local décrit un sermon du vendredi à la mosquée al-Rahman, passé d’un sujet religieux à des revendications locales concernant l’école et les services publics. Les détails du dialogue et des demandes sont présentés comme un témoignage local."
        }, "sources":[2], "basis":"local"
    },
    {
        "date":{"ar":"14 آذار 2011","en":"14 March 2011","fr":"14 mars 2011"},
        "title":{"ar":"ليلة الكتابة على الجدران","en":"The night of the wall writings","fr":"La nuit des inscriptions sur les murs"},
        "text":{
            "ar":"ينسب الأرشيف المحلي إلى هذه الليلة كتابات احتجاجية على جدران مدارس ومواقع في المدينة، من بينها عبارة «إجاك الدور يا دكتور». وتفاصيل المشاركين والأماكن واردة في شهادة المؤلف، وليست جميعها مثبتة في تقارير مستقلة.",
            "en":"The local archive attributes protest inscriptions on school walls and other locations in the city to this night, including the phrase “Your turn has come, Doctor.” Details about participants and locations come from the author’s testimony and are not all independently corroborated.",
            "fr":"Les archives locales attribuent à cette nuit des inscriptions de protestation sur les murs d’écoles et d’autres lieux de la ville, dont la phrase « Ton tour est arrivé, Docteur ». Les détails concernant les participants et les lieux proviennent du témoignage de l’auteur et ne sont pas tous corroborés indépendamment."
        }, "sources":[2], "basis":"local"
    },
    {
        "date":{"ar":"18 آذار 2011","en":"18 March 2011","fr":"18 mars 2011"},
        "title":{"ar":"جمعة الكرامة وبداية المظاهرات الحاشدة","en":"Friday of Dignity and the first large demonstrations","fr":"Le vendredi de la dignité et les premières grandes manifestations"},
        "text":{
            "ar":"تسجل الشهادة المحلية خروج مظاهرة من محيط جامع الرحمن باتجاه مركز المدينة، ورفع مطالب الحرية والإصلاح والوحدة الوطنية. ويتناول تقرير الأمم المتحدة أحداث بانياس في 18 آذار وما تلاها، موفراً مرجعاً مستقلاً للسياق العام.",
            "en":"The local testimony records a demonstration moving from the area around al-Rahman Mosque towards the city centre, with calls for freedom, reform and national unity. The UN report discusses the Baniyas events of 18 March and the days that followed, providing an independent source for the wider context.",
            "fr":"Le témoignage local rapporte une manifestation partie des abords de la mosquée al-Rahman vers le centre-ville, avec des revendications de liberté, de réforme et d’unité nationale. Le rapport de l’ONU traite des événements de Baniyas du 18 mars et des jours suivants, fournissant une source indépendante pour le contexte général."
        }, "sources":[2,3], "basis":"mixed"
    },
    {
        "date":{"ar":"25 آذار – 1 نيسان 2011","en":"25 March–1 April 2011","fr":"25 mars–1er avril 2011"},
        "title":{"ar":"من المطالب الإصلاحية إلى إسقاط النظام","en":"From reform demands to calls for the regime’s removal","fr":"Des revendications de réforme aux appels au départ du régime"},
        "text":{
            "ar":"يوثق تقرير المفوضية السامية لحقوق الإنسان وقوع عنف قرب جامع أبي بكر الصديق في بانياس يوم 25 آذار، ويورد سقوط ثلاثة قتلى على الأقل. أما تفاصيل مظاهرة 1 نيسان والهتافات التي رفعت سقف المطالب فتُعرض وفق الشهادة المحلية.",
            "en":"The Office of the UN High Commissioner for Human Rights documented violence near Abu Bakr al-Siddiq Mosque in Baniyas on 25 March and reported at least three deaths. Details of the 1 April demonstration and its calls for a higher political demand are presented according to local testimony.",
            "fr":"Le Haut-Commissariat des Nations unies aux droits de l’homme a documenté des violences près de la mosquée Abou Bakr al-Siddiq à Baniyas le 25 mars et fait état d’au moins trois morts. Les détails de la manifestation du 1er avril et de ses revendications politiques sont rapportés selon le témoignage local."
        }, "sources":[2,3], "basis":"mixed"
    },
    {
        "date":{"ar":"8–9 نيسان 2011","en":"8–9 April 2011","fr":"8–9 avril 2011"},
        "title":{"ar":"سبت الأكفان","en":"The Shrouds Saturday demonstration","fr":"La manifestation des linceuls"},
        "text":{
            "ar":"تصف الرواية المحلية ارتداء أكفان بيضاء في مظاهرة 8 نيسان ثم خروج حشد كبير في اليوم التالي. ويتيح أرشيف Damascus Bureau مرجعاً مرئياً معاصراً لمقاطع من مظاهرة 9 نيسان.",
            "en":"The local account describes protesters wearing white shrouds at a demonstration on 8 April, followed by a large gathering the next day. The Damascus Bureau archive provides a contemporary visual record of footage from the 9 April demonstration.",
            "fr":"Le récit local décrit des manifestants portant des linceuls blancs lors d’une manifestation le 8 avril, suivie d’un grand rassemblement le lendemain. Les archives de Damascus Bureau offrent une trace visuelle contemporaine de séquences de la manifestation du 9 avril."
        }, "sources":[2,6], "basis":"mixed"
    },
    {
        "date":{"ar":"10 نيسان 2011","en":"10 April 2011","fr":"10 avril 2011"},
        "title":{"ar":"الأحد الدامي وجسر رأس النبع","en":"Bloody Sunday and Ras al-Nabaa Bridge","fr":"Le dimanche sanglant et le pont de Ras al-Nabaa"},
        "text":{
            "ar":"تتناول الشهادة المحلية إطلاق النار والضحايا عند جسر رأس النبع ومحيطه. وتورد التغطية الصحفية المعاصرة روايات متباينة عن تسلسل الأحداث والحصيلة؛ لذلك لا تُقدَّم هنا حصيلة موحدة تتجاوز ما يثبته كل مصدر.",
            "en":"Local testimony describes gunfire and casualties at and around Ras al-Nabaa Bridge. Contemporary press reports contain differing accounts of the sequence of events and the toll; this chronology therefore does not present a single consolidated count beyond what each source supports.",
            "fr":"Le témoignage local décrit des tirs et des victimes au pont de Ras al-Nabaa et dans ses environs. Les articles de presse contemporains présentent des récits différents de la séquence des événements et du bilan ; cette chronologie ne propose donc pas de chiffre unique au-delà de ce que chaque source étaye."
        }, "sources":[2,4], "basis":"mixed"
    },
    {
        "date":{"ar":"11–13 نيسان 2011","en":"11–13 April 2011","fr":"11–13 avril 2011"},
        "title":{"ar":"احتجاج النساء وقطع الطريق الساحلي","en":"Women’s protest and the coastal highway sit-in","fr":"La mobilisation des femmes et le blocage de la route côtière"},
        "text":{
            "ar":"تذكر التقارير الحقوقية والصحفية حملة الاعتقالات في البيضا، ثم خروج نساء وأطفال حاملين الأعلام البيضاء وأغصان الزيتون للمطالبة بالإفراج عن المعتقلين وقطع الطريق الساحلي. ويُستند في وصف الاعتصام إلى تغطية واشنطن بوست المعاصرة.",
            "en":"Human-rights and press reports describe an arrest campaign in al-Bayda, followed by women and children carrying white flags and olive branches to demand the release of detainees and block the coastal highway. The account of the sit-in draws on contemporary Washington Post coverage.",
            "fr":"Des rapports de défense des droits humains et des articles de presse décrivent une campagne d’arrestations à al-Bayda, suivie d’une mobilisation de femmes et d’enfants portant des drapeaux blancs et des branches d’olivier pour demander la libération des détenus et bloquer la route côtière. Le récit du sit-in s’appuie sur un article contemporain du Washington Post."
        }, "sources":[5,10], "basis":"independent"
    },
    {
        "date":{"ar":"14–26 نيسان 2011","en":"14–26 April 2011","fr":"14–26 avril 2011"},
        "title":{"ar":"توثيق البيضا ومعركة إثبات الحقيقة","en":"Documentation of al-Bayda and the struggle to establish the facts","fr":"La documentation d’al-Bayda et l’établissement des faits"},
        "text":{
            "ar":"تسجل الذاكرة السورية ظهور أحمد بياسي أمام الكاميرا لتأكيد مكان تصوير مقطع الاعتداء في البيضا. ويُقرأ هذا السجل إلى جانب تقرير هيومن رايتس ووتش اللاحق، مع التمييز بين التسجيل المعاصر والتحقيق الحقوقي اللاحق.",
            "en":"Syrian Memory records Ahmad al-Biyasi appearing on camera to confirm that footage of an assault was filmed in al-Bayda. This record is read alongside the later Human Rights Watch investigation, distinguishing the contemporary recording from subsequent human-rights reporting.",
            "fr":"La mémoire syrienne rapporte qu’Ahmad al-Biyasi est apparu devant la caméra pour confirmer que des images d’une agression avaient été filmées à al-Bayda. Cette archive est mise en regard de l’enquête ultérieure de Human Rights Watch, en distinguant l’enregistrement contemporain du rapport publié par la suite."
        }, "sources":[9,10], "basis":"independent"
    },
    {
        "date":{"ar":"29 نيسان 2011","en":"29 April 2011","fr":"29 avril 2011"},
        "title":{"ar":"جمعة غضب الورد","en":"Friday of the Roses","fr":"Le vendredi de la colère des roses"},
        "text":{
            "ar":"يوثق سجل الذاكرة السورية مظاهرة حمل فيها المشاركون الورود وأغصان الزيتون. ويورد الأرشيف المحلي تقديراً أكبر لعدد المشاركين من بعض التغطيات المعاصرة؛ لذلك تبقى الأعداد منسوبة إلى مصادرها ولا تُعرض كإحصاء محسوم.",
            "en":"A Syrian Memory record documents a demonstration in which participants carried flowers and olive branches. The local archive gives a higher estimate of attendance than some contemporary reports; the figures are therefore attributed to their sources rather than presented as a settled count.",
            "fr":"Une fiche de Syrian Memory documente une manifestation au cours de laquelle les participants portaient des fleurs et des branches d’olivier. Les archives locales donnent une estimation de participation supérieure à certains articles contemporains ; les chiffres restent donc attribués à leurs sources et ne sont pas présentés comme un bilan établi."
        }, "sources":[2,7], "basis":"mixed"
    },
    {
        "date":{"ar":"30 نيسان 2011","en":"30 April 2011","fr":"30 avril 2011"},
        "title":{"ar":"ليلة الشموع","en":"The Night of Candles","fr":"La nuit des bougies"},
        "text":{
            "ar":"تصف الشهادة المحلية مظاهرة ليلية بالشموع في ساحة مدرسة ابن خلدون، تضامناً مع درعا وحمص. ويذكر المصدر المحلي أن الشموع رُتبت لتشكيل كلمات وشعارات؛ أما وصفها بأنها الأولى من نوعها في سوريا فلا يُقدَّم هنا كأسبقية مثبتة مستقلاً.",
            "en":"Local testimony describes a candlelit night demonstration at Ibn Khaldun School square in solidarity with Daraa and Homs. The local source says the candles were arranged to form words and slogans; the claim that this was the first event of its kind in Syria is not presented here as independently established.",
            "fr":"Le témoignage local décrit une manifestation nocturne aux bougies sur la place de l’école Ibn Khaldoun, en solidarité avec Deraa et Homs. La source locale indique que les bougies formaient des mots et des slogans ; l’affirmation selon laquelle il s’agissait d’une première en Syrie n’est pas présentée ici comme établie indépendamment."
        }, "sources":[2], "basis":"local"
    },
    {
        "date":{"ar":"3 أيار 2011","en":"3 May 2011","fr":"3 mai 2011"},
        "title":{"ar":"مظاهرة الخبز والكرامة","en":"The Bread and Dignity demonstration","fr":"La manifestation du pain et de la dignité"},
        "text":{
            "ar":"يسجل الأرشيف المحلي مظاهرة في ساحة السنتر رُفعت فيها أرغفة الخبز في سياق التضامن مع درعا والاعتراض على الحصار ونقص المواد الأساسية. وتبقى تفاصيل المبادرة والهتافات منسوبة إلى الشهادة المحلية.",
            "en":"The local archive records a demonstration in the central square where participants raised loaves of bread in solidarity with Daraa and in protest against the siege and shortages of basic goods. Details of the initiative and chants remain attributed to local testimony.",
            "fr":"Les archives locales rapportent une manifestation sur la place centrale où les participants ont brandi des pains en solidarité avec Deraa et pour protester contre le siège et les pénuries de produits essentiels. Les détails de l’initiative et des slogans restent attribués au témoignage local."
        }, "sources":[2], "basis":"local"
    },
    {
        "date":{"ar":"6–7 أيار 2011","en":"6–7 May 2011","fr":"6–7 mai 2011"},
        "title":{"ar":"جمعة التحدي والاقتحام العسكري","en":"Friday of Defiance and the military incursion","fr":"Le vendredi du défi et l’incursion militaire"},
        "text":{
            "ar":"تجمع الرواية المحلية بين مظاهرة 6 أيار والاقتحام الواسع لبانياس وقراها في 7 أيار. وتوفر سجلات الذاكرة السورية والتغطية الصحفية المعاصرة مراجع مستقلة لأحداث الاقتحام والضحايا، مع ضرورة إبقاء الأسماء والأعداد وفق كل سجل.",
            "en":"The local account connects the 6 May demonstration with the large-scale incursion into Baniyas and nearby villages on 7 May. Syrian Memory records and contemporary press coverage provide independent references for the incursion and reported casualties; names and counts should remain specific to each record.",
            "fr":"Le récit local relie la manifestation du 6 mai à l’incursion de grande ampleur dans Baniyas et les villages voisins le 7 mai. Les archives de Syrian Memory et la presse contemporaine fournissent des références indépendantes sur l’incursion et les victimes signalées ; les noms et les chiffres doivent rester propres à chaque source."
        }, "sources":[2,7,8,21,22,23,26], "basis":"mixed"
    },
    {
        "date":{"ar":"20 أيار 2011","en":"20 May 2011","fr":"20 mai 2011"},
        "title":{"ar":"جمعة آزادي","en":"Azadi Friday","fr":"Le vendredi Azadi"},
        "text":{
            "ar":"تسجل الرواية المحلية خروج مظاهرة جديدة بعد الاقتحام، تحت شعار «آزادي» الذي يعني الحرية باللغة الكردية. وتبقى تفاصيل المسار والمشاركين منسوبة إلى التوثيق المحلي.",
            "en":"The local account records another demonstration after the incursion, under the slogan “Azadi”, meaning freedom in Kurdish. Details of the route and participants are attributed to the local archive.",
            "fr":"Le récit local rapporte une nouvelle manifestation après l’incursion, sous le slogan « Azadi », qui signifie liberté en kurde. Les détails du parcours et des participants sont attribués aux archives locales."
        }, "sources":[2], "basis":"local"
    },
    {
        "date":{"ar":"2011–2013","en":"2011–2013","fr":"2011–2013"},
        "title":{"ar":"المظاهرات الطيارة والانشقاقات الأولى","en":"Rapid demonstrations and early defections","fr":"Manifestations éclairs et premières défections"},
        "text":{
            "ar":"تصف الشهادة المحلية استمرار أشكال احتجاج صغيرة وسريعة بعد تعذر تنظيم المظاهرات الكبرى، كما تورد روايات عن انشقاقات مبكرة. وتُعرض هذه التفاصيل باعتبارها مادة من أرشيف المؤلف وشهادته، لا بوصفها قاعدة بيانات مستقلة مكتملة.",
            "en":"Local testimony describes small, rapid protest actions after large demonstrations became difficult to organize, and recounts early defections. These details are presented as material from the author’s archive and testimony, not as a complete independent database.",
            "fr":"Le témoignage local décrit de petites actions de protestation rapides après que l’organisation de grandes manifestations est devenue difficile, et rapporte des récits de premières défections. Ces éléments sont présentés comme provenant des archives et du témoignage de l’auteur, et non comme une base de données indépendante exhaustive."
        }, "sources":[2], "basis":"local"
    },
    {
        "date":{"ar":"2–3 أيار 2013","en":"2–3 May 2013","fr":"2–3 mai 2013"},
        "title":{"ar":"مجازر البيضا ورأس النبع والبساتين","en":"The massacres in al-Bayda, Ras al-Nabaa and al-Bustan","fr":"Les massacres d’al-Bayda, Ras al-Nabaa et al-Bustan"},
        "text":{
            "ar":"توثق تقارير هيومن رايتس ووتش ولجنة التحقيق الدولية المستقلة ومنظمة العفو الدولية الإعدامات والانتهاكات في البيضا وبانياس. وقد أحصت هيومن رايتس ووتش 167 ضحية في البيضا و81 في رأس النبع ضمن قوائمها، مع التنبيه إلى احتمال أن تكون الحصيلة الفعلية أعلى. وتتناول تغطية لاحقة البساتين كواقعة منفصلة؛ لذلك لا تُدمج المواقع أو الأرقام في حصيلة واحدة.",
            "en":"Reports by Human Rights Watch, the UN Commission of Inquiry and Amnesty International document executions and abuses in al-Bayda and Baniyas. Human Rights Watch listed 167 victims in al-Bayda and 81 in Ras al-Nabaa, while noting that the actual toll may be higher. Later reporting treats al-Bustan as a separate episode; locations and figures are therefore not merged into one total.",
            "fr":"Les rapports de Human Rights Watch, de la Commission d’enquête de l’ONU et d’Amnesty International documentent des exécutions et des violations à al-Bayda et Baniyas. Human Rights Watch a recensé 167 victimes à al-Bayda et 81 à Ras al-Nabaa dans ses listes, tout en signalant que le bilan réel pourrait être supérieur. Des publications ultérieures traitent al-Bustan comme un épisode distinct ; les lieux et les chiffres ne sont donc pas fusionnés en un seul total."
        }, "sources":[10,11,12,13], "basis":"independent"
    },
    {
        "date":{"ar":"2013–2024","en":"2013–2024","fr":"2013–2024"},
        "title":{"ar":"الشتات واستمرار حضور أبناء بانياس","en":"Displacement and the continued presence of Baniyas communities","fr":"L’exil et la continuité des communautés de Baniyas"},
        "text":{
            "ar":"تسجل الرواية المحلية امتداد حياة أبناء المدينة خارج بانياس خلال سنوات النزوح، وتورد أنماطاً من النشاط المجتمعي والطبي والإعلامي. وأي تفاصيل تتعلق بتشكيلات أو أدوار ميدانية تبقى منسوبة إلى رواية المؤلف ما لم يسندها مصدر مستقل محدد.",
            "en":"The local account records the lives of people from Baniyas outside the city during the years of displacement and describes forms of community, medical and media activity. Details concerning formations or field roles remain attributed to the author’s account unless supported by a specific independent source.",
            "fr":"Le récit local retrace la vie des habitants de Baniyas hors de la ville pendant les années de déplacement et décrit des formes d’activité communautaire, médicale et médiatique. Les détails concernant des formations ou des rôles sur le terrain restent attribués au récit de l’auteur, sauf lorsqu’une source indépendante précise les étaye."
        }, "sources":[2], "basis":"local"
    },
    {
        "date":{"ar":"2011–2024","en":"2011–2024","fr":"2011–2024"},
        "title":{"ar":"التهجير والمخيمات وذاكرة العودة","en":"Displacement, camps and the memory of return","fr":"Déplacement, camps et mémoire du retour"},
        "text":{
            "ar":"يوثق الأرشيف المحلي سنوات النزوح وما رافقها من إقامة في المخيمات وحفظ مفاتيح المنازل والارتباط بفكرة العودة. وتُعرض الصور والتفاصيل الميدانية باعتبارها مواد من أرشيف المؤلف أو من تصوير أشخاص تُذكر أسماؤهم في النسخة الأصلية.",
            "en":"The local archive documents years of displacement, life in camps, the keeping of house keys and the continuing idea of return. Photographs and field details are treated as material from the author’s archive or from photographers credited by name in the original document.",
            "fr":"Les archives locales documentent les années de déplacement, la vie dans les camps, la conservation des clés des maisons et l’idée persistante du retour. Les photographies et les détails de terrain sont considérés comme des éléments des archives de l’auteur ou de photographes crédités dans le document original."
        }, "sources":[2], "basis":"local"
    },
    {
        "date":{"ar":"8 كانون الأول 2024","en":"8 December 2024","fr":"8 décembre 2024"},
        "title":{"ar":"سقوط النظام وبداية العودة","en":"The fall of the Assad government and the beginning of return","fr":"La chute du gouvernement Assad et le début du retour"},
        "text":{
            "ar":"يوثق تسلسل Associated Press سقوط حكومة الأسد في 8 كانون الأول 2024 بعد أسابيع من العمليات العسكرية التي بدأت في 27 تشرين الثاني. ويضيف الأرشيف المحلي مشاهد توجه الأهالي نحو بانياس والعودة إليها؛ وتبقى الصور المحلية منسوبة إلى أرشيف المؤلف.",
            "en":"The Associated Press chronology records the fall of the Assad government on 8 December 2024 after the military operation that began on 27 November. The local archive adds scenes of residents travelling towards and returning to Baniyas; local photographs remain attributed to the author’s archive.",
            "fr":"La chronologie d’Associated Press rapporte la chute du gouvernement Assad le 8 décembre 2024, après l’opération militaire commencée le 27 novembre. Les archives locales ajoutent des scènes d’habitants se dirigeant vers Baniyas et y retournant ; les photographies locales restent attribuées aux archives de l’auteur."
        }, "sources":[2,19], "basis":"mixed"
    },
    {
        "date":{"ar":"آذار – تشرين الثاني 2025","en":"March–November 2025","fr":"Mars–novembre 2025"},
        "title":{"ar":"اختبار الوحدة الوطنية ومبادرات حماية المدنيين","en":"The test of national unity and civilian-protection initiatives","fr":"L’épreuve de l’unité nationale et les initiatives de protection des civils"},
        "text":{
            "ar":"تتناول التقارير الأممية والحقوقية والصحفية أحداث الساحل في آذار 2025، والانتهاكات التي طالت المدنيين والمرافق الصحية، كما يوثق تقرير لوموند شهادة عن حماية عائلات من جيرانها في بانياس. ويذكر سجل سانا فعاليات 28 تشرين الثاني في الذكرى الأولى لبدء معركة ردع العدوان. ويجب قراءة كل رقم أو شهادة ضمن نطاق المصدر الذي أوردها.",
            "en":"UN, human-rights and press reports cover the March 2025 coastal events and violations affecting civilians and medical facilities. A Le Monde report documents testimony about neighbours protecting families in Baniyas. A SANA report records events on 28 November marking the first anniversary of the start of Operation Deterring Aggression. Each figure or testimony should be read within the scope of the source that reported it.",
            "fr":"Des rapports de l’ONU, d’organisations de défense des droits humains et de médias couvrent les événements côtiers de mars 2025 ainsi que les violations visant des civils et des établissements de santé. Un article du Monde rapporte un témoignage sur la protection de familles par leurs voisins à Baniyas. Un article de SANA documente les événements du 28 novembre marquant le premier anniversaire du début de l’opération « Dissuasion de l’agression ». Chaque chiffre ou témoignage doit être lu dans le périmètre de la source qui le rapporte."
        }, "sources":[14,15,16,17,18,20,24,25], "basis":"independent"
    }
]

def citations(ids):
    return " ".join(f'<sup class="citation"><a href="#ref-{n}" aria-label="Reference {n}">[{n}]</a></sup>' for n in ids)

def source_list(lang):
    items = []
    for number, label, url in SOURCES:
        if url:
            text = f'<a href="{escape(url, quote=True)}" rel="noopener noreferrer">{escape(label)}</a>'
        else:
            text = f'<span>{escape(label)}</span> <em>({escape(UI[lang]["source_unavailable"])})</em>'
        items.append(f'<li id="ref-{number}"><span class="ref-number">[{number}]</span> {text}</li>')
    return '<ol class="references">' + "".join(items) + '</ol>'

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
    og_image = "" if route == BANIYAS_ROUTE else f'<meta property="og:image" content="{ORIGIN}/assets/kasem-adra-portrait.jpg>'
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
<footer><span>{escape(u["footer"])}</span><div class="profiles"><a href="{GITHUB}">GitHub</a><a href="{ORCID}">ORCID</a><a href="{LINKEDIN}">LinkedIn</a></div></footer>
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
        (u["baniyas_title"], u["baniyas_desc"], f"/{lang}{BANIYAS_ROUTE}"),
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

def baniyas_html(lang):
    u = UI[lang]
    event_html = []
    for index, event in enumerate(EVENTS, 1):
        basis_key = {"local":"basis_local", "mixed":"basis_mixed", "independent":"basis_independent"}[event["basis"]]
        event_html.append(
            f'<article class="timeline-entry" id="event-{index}">'
            f'<div class="timeline-date">{escape(event["date"][lang])}</div>'
            f'<div><h3>{escape(event["title"][lang])}</h3>'
            f'<p>{escape(event["text"][lang])} {citations(event["sources"])}</p>'
            f'<p class="source-basis">{escape(u[basis_key])}</p></div></article>'
        )
    infobox = f'''<aside class="archive-infobox" aria-label="{escape(u["infobox"])}">
<h2>{escape(u["infobox"])}</h2>
<dl>
<dt>{escape(u["period"])}</dt><dd>2010–2025</dd>
<dt>{escape(u["place"])}</dt><dd>{'Baniyas, Tartus Governorate, Syria' if lang == 'en' else 'بانياس، محافظة طرطوس، سوريا' if lang == 'ar' else 'Baniyas, gouvernorat de Tartous, Syrie'}</dd>
<dt>{escape(u["compiler"])}</dt><dd><a href="/{lang}/about/">Kasem Adra / قاسم عدرا</a></dd>
<dt>{escape(u["source_edition"])}</dt><dd>{ "v27-audited · 37-page source chronology" if lang == "en" else "v27-audited · تسلسل زمني من 37 صفحة" if lang == "ar" else "v27-audited · chronologie source de 37 pages" }</dd>
<dt>{escape(u["coverage"])}</dt><dd>{'20 chronological sections; local testimony and 25 external references' if lang == 'en' else '20 محطة زمنية؛ شهادات محلية و25 مرجعًا خارجيًا' if lang == 'ar' else '20 étapes chronologiques ; témoignages locaux et 25 références externes'}</dd>
</dl></aside>'''
    main = f'''<p class="label">{escape(u["archive"])}</p>
<h1>{escape(u["baniyas_title"])}</h1>
<p class="archive-lead">{escape(u["baniyas_intro"])}</p>
{infobox}
<nav class="toc" aria-label="{escape(u["contents"])}"><h2>{escape(u["contents"])}</h2><ol>
<li><a href="#overview">{escape(u["overview"])}</a></li>
<li><a href="#method">{escape(u["method"])}</a></li>
<li><a href="#timeline">{escape(u["timeline"])}</a></li>
<li><a href="#references">{escape(u["references"])}</a></li>
<li><a href="#related">{escape(u["related"])}</a></li>
</ol></nav>
<section id="overview"><h2>{escape(u["overview"])}</h2><p>{escape(u["note_text"])}</p></section>
<section id="method"><h2>{escape(u["method"])}</h2><p>{escape(u["method_text"])}</p></section>
<section id="timeline"><h2>{escape(u["timeline"])}</h2><div class="timeline">{''.join(event_html)}</div></section>
<section id="references"><h2>{escape(u["references"])}</h2>
{source_list(lang)}
</section>
<section id="related"><h2>{escape(u["related"])}</h2>
<ul>
<li><a href="/{lang}/about/">Kasem Adra / قاسم عدرا — {escape(u["profile_archive"])}</a></li>
<li><a href="/{lang}/publications/aco-llm/">ACO-LLM</a></li>
<li><a href="/{lang}/publications/aco-llm-results/">ACO-LLM evaluation results</a></li>
<li><a href="/{lang}/archive/">{escape(u["archive_title"])}</a></li>
</ul></section>
<section><h2>{escape(u["last_reviewed"])}</h2><p>{escape(u["review_date"])}</p><p><strong>{escape(u["note"])}:</strong> {escape(u["note_text"])}</p></section>'''
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
    graph = [PERSON, webpage]
    if route == "/about/":
        webpage["@type"] = "ProfilePage"
        webpage["mainEntity"] = {"@id": PERSON_ID}
    elif route == ARCHIVE_ROUTE:
        webpage["@type"] = "CollectionPage"
        webpage["hasPart"] = [
            {"@id": ORIGIN + f"/{lang}" + BANIYAS_ROUTE + "#article"},
            {"@id": ORIGIN + f"/{lang}/publications/aco-llm/#article"},
            {"@id": ORIGIN + f"/{lang}/publications/aco-llm-results/#article"}
        ]
    elif route == BANIYAS_ROUTE:
        article = {
            "@type": "Article",
            "@id": canonical + "#article",
            "headline": UI[lang]["baniyas_title"],
            "description": description,
            "url": canonical,
            "author": {"@id": PERSON_ID},
            "datePublished": "2026-11-27",
            "dateModified": "2026-11-27",
            "inLanguage": lang,
            "articleSection": "Historical archive",
            "about": {"@id": ORIGIN + "/#place-baniyas"},
            "citation": ["Kasem Adra, وردة الدم: حكاية ثورة بانياس (local testimony; bibliographic details incomplete in the cited copy)."] + [url for _, _, url in SOURCES if url],
            "keywords": ["Baniyas", "Banias", "Banyas", "Syrian revolution", "Syria 2011", "Baniyas 2013", "historical archive", "oral history"],
            "genre": "Historical documentary chronology",
            "version": "v27-audited",
            "isAccessibleForFree": True,
            "isPartOf": {"@id": ORIGIN + f"/{lang}{ARCHIVE_ROUTE}#collection"},
            "mainEntityOfPage": {"@id": canonical + "#webpage"}
        }
        graph.append({
            "@type":"City",
            "@id":ORIGIN + "/#place-baniyas",
            "name":"Baniyas",
            "alternateName":["Banias","Banyas"],
            "containedInPlace":{"@type":"AdministrativeArea","name":"Tartus Governorate","containedInPlace":{"@type":"Country","name":"Syria"}}
        })
        graph.append(article)
        webpage["mainEntity"] = {"@id": canonical + "#article"}
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
            "checking-work": {"en":"How do we verify an assistant’s work?","ar":"كيف نتحقّق من عمل المساعد؟","fr":"Comment vérifier le travail d’un assistant ?"},
            "arabic-calligraphy": {"en":"When Letters Become a Drawing","ar":"حين تصبح الحروف رسمة","fr":"Quand les lettres deviennent un dessin"}
        }
        post = {
            "@type":"BlogPosting",
            "@id":canonical+"#article",
            "headline":post_titles.get(slug,{}).get(lang,title),
            "author":{"@id":PERSON_ID},
            "datePublished":"2026-11-26",
            "dateModified":"2026-11-26",
            "inLanguage":lang,
            "url":canonical,
            "mainEntityOfPage":{"@id":canonical+"#webpage"},
            "isPartOf":{"@id":ORIGIN+f"/{lang}/blog/#collection"}
        }
        if slug == "arabic-calligraphy":
            post["image"] = ORIGIN + "/assets/kasem-calligraphy-transparent.png"
        graph.append(post)
        webpage["mainEntity"] = {"@id":canonical+"#article"}
    elif route in ("/blog/","/projects/"):
        webpage["@type"] = "CollectionPage"
    elif route == "/projects/local-assistant/":
        graph.append({
            "@type":"CreativeWork",
            "@id":canonical+"#project",
            "name":"A local AI assistant for Arabic",
            "author":{"@id":PERSON_ID},
            "inLanguage":["ar","en"],
            "about":["Local AI assistants","Arabic language technology","On-device AI"]
        })
        webpage["mainEntity"]={"@id":canonical+"#project"}
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
            "hasPart":[{"@id":ORIGIN+f"/{lang}"+BANIYAS_ROUTE+"#article"},{"@id":PROTOCOL_DOI},{"@id":RESULTS_DOI}]
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
                "baniyas-revolution-2010-2025":UI[lang]["baniyas_title"],
                "projects":UI[lang]["projects"],"local-assistant":"A local AI assistant",
                "publications":UI[lang]["research"],"aco-llm":UI[lang]["protocol_title"],
                "aco-llm-results":UI[lang]["results_title"],"blog":UI[lang]["writing"],
                "checking-work":"How do we verify an assistant’s work?",
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
            "en":("Local Arabic AI Assistant | Kasem Adra","A local, on-device AI assistant project by Kasem Adra for Arabic text, speech and tool-assisted tasks."),
            "ar":("مساعد ذكاء اصطناعي محلي بالعربية | قاسم عدرا","مشروع مساعد ذكاء اصطناعي يعمل محليًا ويدعم النص والصوت العربيين وتنفيذ المهام بالأدوات."),
            "fr":("Assistant IA local en arabe | Kasem Adra","Projet d’assistant IA exécuté localement, prenant en charge le texte, la voix et les outils en arabe.")
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
            "en":("How to Verify an AI Assistant’s Work | Kasem Adra","A practical explanation of checking task outcomes independently of an AI assistant’s own completion claim."),
            "ar":("كيف نتحقق من عمل مساعد الذكاء الاصطناعي؟ | قاسم عدرا","شرح عملي للتحقق من نتائج المهمة بصورة مستقلة عن ادعاء المساعد الذكي أنه أتم العمل."),
            "fr":("Comment vérifier le travail d’un assistant IA ? | Kasem Adra","Explication pratique de la vérification des résultats indépendamment de l’affirmation de réussite de l’assistant.")
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
                    "bio":"Biography","contents":"Contents","facts":"Profile at a glance","name":"Name","occupation":"Occupation","occupation_value":"Independent AI researcher","origin":"Origin","origin_value":"Baniyas, Syria","location":"Based in","location_value":"France","education":"Education","research":"Research and publications","projects":"Projects","archive":"Historical documentation","interests":"Other interests","identifiers":"Public identifiers","protocol_link":"ACO-LLM research protocol","results_link":"ACO-LLM evaluation results","projects_link":"View selected projects","archive_link":"Baniyas documentary archive, 2010–2025","preprint":"preprint",
                    "bio_text":"Kasem Adra (قاسم عدرا) is an independent AI researcher based in France and originally from Baniyas, Syria. He studies computer science and artificial intelligence. His work focuses on local AI assistants and methods for verifying task completion and recovering from errors. He published the ACO-LLM research protocol and a separate evaluation preprint. His academic background includes an MBA and a master’s degree in Digital Marketing and Analytics.",
                    "education_text":"MBA (Master of Business Administration); Master in Digital Marketing and Analytics; current studies in computer science and artificial intelligence.",
                    "research_text":"His independent research examines how local language models and AI agents can select tools, verify their outputs and recover from observable failures. The ACO-LLM protocol and its held-out evaluation are separate research records; the results paper is a preprint and has not been peer reviewed.",
                    "projects_text":"Selected work includes a local AI assistant designed to support Arabic text and speech, alongside data-science projects involving launch data and financial datasets.",
                    "archive_text":"He maintains a documentary chronology of Baniyas from 2010 to 2025. The archive distinguishes local testimony and author-held materials from independently published human-rights, press and institutional sources.",
                    "interests_text":"He also explores Arabic calligraphy and visual design, including the calligraphic signature used on this website."
                },
                "ar": {
                    "bio":"السيرة","contents":"المحتويات","facts":"بطاقة تعريفية","name":"الاسم","occupation":"الصفة","occupation_value":"باحث مستقل في الذكاء الاصطناعي","origin":"الأصل","origin_value":"بانياس، سوريا","location":"الإقامة","location_value":"فرنسا","education":"التعليم","research":"الأبحاث والمنشورات","projects":"المشاريع","archive":"التوثيق التاريخي","interests":"اهتمامات أخرى","identifiers":"المعرّفات العامة","protocol_link":"بروتوكول ACO-LLM البحثي","results_link":"نتائج تقييم ACO-LLM","projects_link":"عرض المشاريع المختارة","archive_link":"أرشيف بانياس الوثائقي، 2010–2025","preprint":"ورقة أولية",
                    "bio_text":"قاسم عدرا باحث مستقل في الذكاء الاصطناعي يقيم في فرنسا وينحدر من مدينة بانياس السورية. يدرس علوم الحاسوب والذكاء الاصطناعي. يركز عمله على المساعدات الذكية المحلية وطرق التحقق من إنجاز المهام والتعافي من الأخطاء. نشر بروتوكول ACO-LLM البحثي، ثم ورقة أولية مستقلة لنتائج التقييم. وتشمل خلفيته الأكاديمية ماجستير إدارة الأعمال (MBA) وماجستير التسويق الرقمي وتحليل البيانات.",
                    "education_text":"ماجستير إدارة الأعمال (MBA)، وماجستير التسويق الرقمي وتحليل البيانات، مع متابعة دراسة علوم الحاسوب والذكاء الاصطناعي.",
                    "research_text":"تتناول أبحاثه المستقلة كيفية اختيار النماذج اللغوية المحلية والوكلاء الأذكياء للأدوات، والتحقق من مخرجاتها، والتعافي من الإخفاقات القابلة للرصد. بروتوكول ACO-LLM وورقة نتائج تقييمه سجلان بحثيان منفصلان؛ وورقة النتائج أولية وغير محكّمة.",
                    "projects_text":"تشمل أعماله مساعد ذكاء اصطناعي محليًا يدعم النص والصوت العربيين، إلى جانب مشاريع في علم البيانات تتناول بيانات إطلاق الصواريخ والبيانات المالية.",
                    "archive_text":"يعدّ تسلسلاً زمنيًا وثائقيًا لأحداث بانياس بين عامي 2010 و2025. ويميّز الأرشيف بين الشهادة المحلية والمواد التي يحتفظ بها المؤلف وبين التقارير الحقوقية والصحفية والمؤسسية المنشورة بصورة مستقلة.",
                    "interests_text":"يهتم أيضًا بالرسم والخط العربي والتصميم البصري، ومن ذلك التوقيع الحروفي المستخدم في هذا الموقع."
                },
                "fr": {
                    "bio":"Biographie","contents":"Sommaire","facts":"Profil en bref","name":"Nom","occupation":"Fonction","occupation_value":"Chercheur indépendant en IA","origin":"Origine","origin_value":"Baniyas, Syrie","location":"Résidence","location_value":"France","education":"Formation","research":"Recherche et publications","projects":"Projets","archive":"Documentation historique","interests":"Autres intérêts","identifiers":"Identifiants publics","protocol_link":"Protocole de recherche ACO-LLM","results_link":"Résultats de l’évaluation ACO-LLM","projects_link":"Voir les projets sélectionnés","archive_link":"Archives documentaires de Baniyas, 2010–2025","preprint":"prépublication",
                    "bio_text":"Kasem Adra (قاسم عدرا) est un chercheur indépendant en intelligence artificielle basé en France et originaire de Baniyas, en Syrie. Il étudie l’informatique et l’intelligence artificielle. Ses travaux portent sur les assistants IA locaux et les méthodes permettant de vérifier l’achèvement des tâches et de corriger les erreurs. Il a publié le protocole de recherche ACO-LLM, puis une prépublication distincte présentant les résultats de l’évaluation. Sa formation comprend un MBA et un master en marketing numérique et analyse de données.",
                    "education_text":"MBA (Master of Business Administration), master en marketing numérique et analyse de données ; études en cours en informatique et intelligence artificielle.",
                    "research_text":"Ses recherches indépendantes portent sur la manière dont les modèles de langage locaux et les agents IA sélectionnent des outils, vérifient leurs résultats et récupèrent après des défaillances observables. Le protocole ACO-LLM et sa prépublication de résultats constituent deux références distinctes ; cette dernière n’a pas été évaluée par les pairs.",
                    "projects_text":"Ses projets comprennent un assistant IA local prenant en charge le texte et la voix en arabe, ainsi que des travaux en science des données portant sur les données de lancement spatial et les données financières.",
                    "archive_text":"Il prépare une chronologie documentaire de Baniyas couvrant la période 2010–2025. Les archives distinguent les témoignages locaux et les documents conservés par l’auteur des rapports indépendants publiés par des organisations de défense des droits humains, des médias et des institutions.",
                    "interests_text":"Il s’intéresse également au dessin, à la calligraphie arabe et au design visuel, notamment à la signature calligraphique de ce site."
                }
            }[lang]
            if 'id="profile-facts"' not in doc:
                infobox = f'<aside class="profile-infobox" id="profile-facts"><h2>{profile_titles["facts"]}</h2><dl><dt>{profile_titles["name"]}</dt><dd>Kasem Adra · قاسم عدرا</dd><dt>{profile_titles["occupation"]}</dt><dd>{profile_titles["occupation_value"]}</dd><dt>{profile_titles["origin"]}</dt><dd>{profile_titles["origin_value"]}</dd><dt>{profile_titles["location"]}</dt><dd>{profile_titles["location_value"]}</dd><dt>{profile_titles["education"]}</dt><dd>{profile_titles["education_text"]}</dd><dt>ORCID</dt><dd><a href="{ORCID}">0009-0004-7615-4978</a></dd></dl></aside>'
                toc = f'<nav class="profile-toc"><h2>{profile_titles["contents"]}</h2><ol><li><a href="#biography">{profile_titles["bio"]}</a></li><li><a href="#research-profile">{profile_titles["research"]}</a></li><li><a href="#projects-profile">{profile_titles["projects"]}</a></li><li><a href="#archive-profile">{profile_titles["archive"]}</a></li><li><a href="#identifiers">{profile_titles["identifiers"]}</a></li></ol></nav>'
                doc = doc.replace("</h1>", "</h1>" + infobox + toc + f'<h2 id="biography">{profile_titles["bio"]}</h2>', 1)
                pattern = r'(<img class="portrait"[^>]*>).*?(<p>(?:Member|عضو|Membre)[^<]*</p>)'
                replacement = lambda m: m.group(1) + f'<p class="profile-biography">{profile_titles["bio_text"]}</p>' + m.group(2)
                doc, replaced = re.subn(pattern, replacement, doc, count=1, flags=re.S)
                if replaced != 1:
                    raise RuntimeError("Could not locate the localized biography on " + str(file))
                extras = f'<section id="research-profile"><h2>{profile_titles["research"]}</h2><p>{profile_titles["research_text"]}</p><ul><li><a href="/{lang}/publications/aco-llm/">{profile_titles["protocol_link"]}</a> · <a href="{PROTOCOL_DOI}">DOI</a></li><li><a href="/{lang}/publications/aco-llm-results/">{profile_titles["results_link"]}</a> · <a href="{RESULTS_DOI}">DOI · {profile_titles["preprint"]}</a></li></ul></section><section id="projects-profile"><h2>{profile_titles["projects"]}</h2><p>{profile_titles["projects_text"]}</p><p><a href="/{lang}/projects/">{profile_titles["projects_link"]}</a></p></section><section id="archive-profile"><h2>{profile_titles["archive"]}</h2><p>{profile_titles["archive_text"]}</p><p><a href="/{lang}/archive/baniyas-revolution-2010-2025/">{profile_titles["archive_link"]}</a></p></section><section id="other-interests"><h2>{profile_titles["interests"]}</h2><p>{profile_titles["interests_text"]}</p></section>'
                if "research-profile" not in doc:
                    doc = doc.replace("</div></main>", extras + "</div></main>", 1)
            profile_section = {
                "en": '<section class="profile-identifiers" id="identifiers"><h2>Public identity and research records</h2><p>Public identifiers and author-controlled records help distinguish this profile from people with similar names. They do not replace independent coverage or peer review.</p><ul><li><a href="' + ORCID + '">ORCID iD: 0009-0004-7615-4978</a></li><li><a href="' + LINKEDIN + '">LinkedIn profile</a></li><li><a href="' + GITHUB + '">GitHub profile</a></li><li><a href="' + PROTOCOL_DOI + '">ACO-LLM research protocol (DOI)</a></li><li><a href="' + RESULTS_DOI + '">ACO-LLM evaluation results (preprint DOI)</a></li><li><a href="/en/archive/">Research and historical archive</a></li></ul></section>',
                "ar": '<section class="profile-identifiers"><h2>الهوية العامة والسجلات البحثية</h2><p>تساعد المعرّفات والسجلات التي يديرها المؤلف على تمييز هذا الملف عن الأشخاص المتشابهة أسماؤهم، لكنها لا تحل محل التغطية المستقلة أو التحكيم العلمي.</p><ul><li><a href="' + ORCID + '">معرّف ORCID: 0009-0004-7615-4978</a></li><li><a href="' + LINKEDIN + '">الملف المهني على LinkedIn</a></li><li><a href="' + GITHUB + '">ملف GitHub</a></li><li><a href="' + PROTOCOL_DOI + '">بروتوكول ACO-LLM البحثي (DOI)</a></li><li><a href="' + RESULTS_DOI + '">نتائج تقييم ACO-LLM (DOI الورقة الأولية)</a></li><li><a href="/ar/archive/">الأرشيف البحثي والتاريخي</a></li></ul></section>',
                "fr": '<section class="profile-identifiers"><h2>Identité publique et références de recherche</h2><p>Les identifiants publics et les références contrôlées par l’auteur aident à distinguer ce profil des personnes portant un nom similaire. Ils ne remplacent ni la couverture indépendante ni l’évaluation par les pairs.</p><ul><li><a href="' + ORCID + '">Identifiant ORCID : 0009-0004-7615-4978</a></li><li><a href="' + LINKEDIN + '">Profil LinkedIn</a></li><li><a href="' + GITHUB + '">Profil GitHub</a></li><li><a href="' + PROTOCOL_DOI + '">Protocole de recherche ACO-LLM (DOI)</a></li><li><a href="' + RESULTS_DOI + '">Résultats de l’évaluation ACO-LLM (DOI de la prépublication)</a></li><li><a href="/fr/archive/">Archives de recherche et historiques</a></li></ul></section>'
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
        social = [
            ("og:site_name","Kasem Adra"),("og:title",title),("og:description",desc),
            ("og:type","profile" if route=="/about/" else "article" if route.startswith("/blog/") or route.startswith("/archive/") or route.startswith("/publications/") else "website"),
            ("og:url",ORIGIN+f"/{lang}"+route),("og:locale",{"ar":"ar_SY","fr":"fr_FR","en":"en_US"}[lang]),
            ("twitter:card","summary_large_image")
        ]
        for prop,value in social:
            attr = "name" if prop.startswith("twitter:") else "property"
            pattern = rf'<meta {attr}="{re.escape(prop)}" content="[^"]*">'
            tag = f'<meta {attr}="{prop}" content="{escape(value,quote=True)}">'
            doc = meta_replace(doc,pattern,tag)
            if not re.search(pattern,doc,flags=re.I):
                doc = doc.replace("</head>",tag+"</head>",1)
        file.write_text(doc,encoding="utf-8")

def write_root_gateway(dist, public_build):
    title = "Kasem Adra | Official multilingual profile and archive"
    desc = "Official multilingual website of Kasem Adra: independent AI research, ACO-LLM publications, projects, writing and historical documentation."
    person = dict(PERSON)
    website = {
        "@type":"WebSite","@id":WEBSITE_ID,"url":ORIGIN+"/","name":"Kasem Adra",
        "alternateName":["قاسم عدرا","Qassem Adra"],
        "description":desc,"inLanguage":["en","ar","fr"],
        "publisher":{"@id":PERSON_ID}
    }
    graph = {"@context":"https://schema.org","@graph":[person,website,{
        "@type":"WebPage","@id":ORIGIN+"/#webpage","url":ORIGIN+"/","name":title,
        "description":desc,"inLanguage":"en","isPartOf":{"@id":WEBSITE_ID},
        "about":{"@id":PERSON_ID},"mainEntity":{"@id":PERSON_ID}
    }]}
    choices = [
        ("English","en","Independent AI researcher · Research, projects and archive"),
        ("العربية","ar","باحث مستقل في الذكاء الاصطناعي · الأبحاث والمشاريع والأرشيف"),
        ("Français","fr","Chercheur indépendant en IA · Recherche, projets et archives")
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
<meta property="og:url" content="{ORIGIN}/"><meta property="og:image" content="{ORIGIN}/assets/kasem-adra-portrait.jpg">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">{dumps(graph,ensure_ascii=False,separators=(",",":"))}</script>
<link rel="stylesheet" href="/style.css"></head>
<body><div class="shell"><header><a class="wordmark" href="/">Kasem Adra</a><span>قاسم عدرا</span></header>
<main class="gateway"><figure><img src="/assets/kasem-adra-portrait.jpg" alt="Portrait of Kasem Adra" width="782" height="1024"></figure>
<div><p class="label">{escape(UI["en"]["gateway_label"])}</p><h1>Kasem Adra</h1><p class="gateway-desc">{escape(UI["en"]["gateway_desc"])}</p><h2>{escape(UI["en"]["lang_gateway"])}</h2><div class="language-choices">{buttons}</div></div>
</main><footer><span>Kasem Adra · قاسم عدرا</span><div class="profiles"><a href="{GITHUB}">GitHub</a><a href="{ORCID}">ORCID</a><a href="{LINKEDIN}">LinkedIn</a></div></footer></div></body></html>'''
    (dist/"index.html").write_text(doc,encoding="utf-8")

def build_site(dist, origin, public_build):
    # Generate the two new archive layers before the sitemap is built.
    for lang in LANGS:
        u = UI[lang]
        shell_page(dist,lang,ARCHIVE_ROUTE,u["archive_title"],u["archive_desc"],archive_index_html(lang),public_build)
        shell_page(dist,lang,BANIYAS_ROUTE,u["baniyas_title"],u["baniyas_desc"],baniyas_html(lang),public_build)
    # Preserve root-level legacy routes as English aliases; their canonicals point to /en/.
    for route in (ARCHIVE_ROUTE,BANIYAS_ROUTE):
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

