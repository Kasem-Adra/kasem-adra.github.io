import json, pathlib
J = json.loads(pathlib.Path(__file__).with_name('results.json').read_text(encoding='utf-8')); B, D, M = J['B'], J['D'], J['main']
def num(x, lang, dec=2, sign=False):
    s = format(x, f"{'+' if sign else ''},.{dec}f")
    fr = lang == 'fr'
    return s.replace(',', '§').replace('.', ',' if fr else '.').replace('§', '\u202f' if fr else ',')
def ltr(s): return f'<bdi dir="ltr">{s}</bdi>'
def vals(L):
    n = lambda x, d=2, s=False: num(x, L, d, s)
    p = lambda x, s=False: n(x, 2, s) + ('\u202f%' if L == 'fr' else '%')
    r = lambda a, t: 100 * a / t
    cell = lambda a, t: f"{n(a,0)} / {n(t,0)} ({p(r(a,t))})"
    ds, dt = D['sec'] - B['sec'], D['tok'] - B['tok']
    return dict(
        rec=J['record'], pdf=J['pdf'], bt=J['base_tasks'], en_=n(J['episodes_per_arm'],0), et=n(J['episodes_total'],0),
        model=ltr(f"<code>{J['model']}</code>"), dpp=ltr(n(M['delta_pp'],2,True)), lo=ltr(n(M['ci_low'])), hi=ltr(n(M['ci_high'])),
        nres=n(M['resamples'],0), sb=n(B['silent_ok'],0), sd=n(D['silent_ok'],0), sn=n(B['silent_n'],0),
        sdp=p(r(D['silent_ok'],D['silent_n'])), fail=n(D['silent_n']-D['silent_ok'],0),
        c1=(cell(B['ok'],B['n']), cell(D['ok'],D['n']), ltr(n(r(D['ok'],D['n'])-r(B['ok'],B['n']),2,True))),
        c2=(cell(B['silent_ok'],B['silent_n']), cell(D['silent_ok'],D['silent_n']), ltr(n(r(D['silent_ok'],D['silent_n'])-r(B['silent_ok'],B['silent_n']),2,True))),
        c3=(n(B['sec'],3), n(D['sec'],3), ltr(f"{n(ds,3,True)} ({p(100*ds/B['sec'],True)})")),
        c4=(n(B['tok']), n(D['tok']), ltr(f"{n(dt,2,True)} ({p(100*dt/B['tok'],True)})")),
        dsec=ltr(n(ds,3,True)), dsecp=ltr(p(100*ds/B['sec'],True)), dtok=ltr(n(dt,2,True)), dtokp=ltr(p(100*dt/B['tok'],True)), gap=ltr(n(r(D['ok'],D['n'])-r(B['ok'],B['n']),2,True)))
T = {
'en': dict(dir='ltr', title='ACO‑LLM evaluation results · Kasem Adra',
 desc='ACO‑LLM evaluation: {delta} percentage points in task success over a fixed-path reference arm, with simulated tools and one local model. Preprint.',
 h1='ACO‑LLM: evaluation results', badge='RESULTS PREPRINT · NOT PEER REVIEWED',
 lead='Summary of the evaluation designed in the <a href="../aco-llm/">protocol</a>. The authoritative source is the <a href="{rec}">results preprint on Zenodo</a> (<a href="{pdf}">PDF</a>).',
 summary_title='In plain terms',
 summary='This evaluation tested whether explicit checks and bounded repair could improve task completion. In this benchmark, arm D exceeded arm B by {dpp} percentage points according to an independent evaluator. The test used one local model and simulated tools; it does not establish the same gain for other models or real services.',
 hmain='Main estimate',
 main='Arm D, which combined task-contract routing, structural verification, and bounded repair, raised task success, as judged by the independent evaluator, by <b>{dpp} percentage points</b> over the fixed-path reference arm with tool support (arm B). 95% confidence interval: {lo} to {hi}.',
 method='Method: paired differences were averaged within each of the {bt} base tasks, and the base tasks were weighted equally. The interval comes from {nres} resamples of base tasks within their strata.',
 hraw='Raw rates and cost', pp='pp', s='s',
 rawnote='Raw rates count every episode, so tool tasks (run in three conditions) weigh more than reasoning tasks; the main estimate weights every base task equally. Raw gap: {gap} pp.',
 th=('Metric','B','D','Difference'), rows=('Success, independent evaluator','Success under silent failures','Mean time per episode (s)','Mean generated tokens per episode'),
 hsil='Silent failures',
 sil='In a silent failure the tool reports success without carrying out the action, for example by confirming a write without changing the file. Arm B relied on the tool\'s ordinary feedback and succeeded in {sb} of {sn} such episodes. Arm D succeeded in {sd} of {sn} ({sdp}); {fail} episodes still failed.',
 hdes='Design',
 des='{bt} base tasks, each in an Arabic and an English version: 32 reasoning tasks (clean condition only) and 64 tool tasks (three conditions, one of them the silent failure). Each case ran three times: 32×2×3 + 64×2×3×3 = {en_} episodes per arm, {et} across the six arms. Model: {model}, a single local model, with simulated tools.',
 arms='<b>B</b>: fixed-path reference arm with tool support, relying on the tool\'s ordinary feedback. <b>D</b>: task-contract routing with verification and bounded repair. The other four arms are described in the preprint.',
 hlim='Limits',
 lim=('Tools were simulated, not real services.','One local model ({model}) and {bt} base tasks.','D used more resources than B: {dsec} s ({dsecp}) and {dtok} tokens ({dtokp}) more per episode.','The preprint has not been peer reviewed.'),
 home='In a held-out evaluation of {bt} base tasks, each with an Arabic and an English version, ACO‑LLM raised task success, as judged by an independent evaluator, by {dpp} percentage points over the fixed-path reference arm with tool support. The evaluation used simulated tools and one local model ({model}). <a href="{rec}">Read the results preprint</a>',
 proto='This protocol describes the design of the evaluation. The evaluation was carried out and its results were published in a separate paper.'),
'ar': dict(dir='rtl', title='نتائج تقييم ACO‑LLM · قاسم عدرا',
 desc='تقييم ACO‑LLM: رفع معدل نجاح المهام بمقدار {delta} نقطة مئوية مقارنة بذراع مرجعية ذات مسار ثابت، باستخدام أدوات محاكاة ونموذج محلي واحد. ورقة أولية.',
 h1='ACO‑LLM: نتائج التقييم', badge='ورقة نتائج أولية · غير محكّمة',
 lead='ملخّص للتقييم الذي صُمّم في <a href="../aco-llm/">البروتوكول</a>. المصدر المعتمد هو <a href="{rec}">ورقة النتائج الأولية على Zenodo</a> (<a href="{pdf}">PDF</a>).',
 summary_title='بعبارة مبسطة',
 summary='اختبر التقييم ما إذا كانت إضافة فحوص صريحة وإصلاح محدود تحسّن إنجاز المهام. في هذا المعيار التجريبي، تفوقت الذراع D على الذراع B بمقدار {dpp} نقطة مئوية وفق مقيّم مستقل. استخدم الاختبار نموذجاً محلياً واحداً وأدوات محاكاة؛ ولا يثبت تحقق التحسن نفسه مع نماذج أخرى أو خدمات حقيقية.',
 hmain='التقدير الرئيسي',
 main='رفعت الذراع D، التي جمعت التوجيه المستند إلى عقد المهمة والتحقق البنيوي والإصلاح المحدود، معدل نجاح المهام، وفق المقيّم المستقل، بمقدار <b>{dpp} نقطة مئوية</b> مقارنة بالذراع المرجعية ذات المسار الثابت الداعم للأدوات (الذراع B). فاصل الثقة 95%: من {lo} إلى {hi}.',
 method='الطريقة: حُسب متوسط الفروق المقترنة داخل كل مهمة من المهام الأساسية الـ{bt}، ثم أُعطيت المهام أوزانًا متساوية. وحُسب الفاصل بإعادة معاينة {nres} مجموعة من المهام الأساسية داخل طبقاتها.',
 hraw='المعدلات الخام والتكلفة', pp='نقطة', s='ث',
 rawnote='تحسب المعدلات الخام كل حلقة، فتزن مهام الأدوات (وتُشغَّل في ثلاث حالات) أكثر من مهام الاستدلال، بينما يعطي التقدير الرئيسي كل مهمة أساسية وزنًا متساويًا. الفرق الخام: {gap} نقطة.',
 th=('المقياس','B','D','الفرق'), rows=('النجاح وفق المقيّم المستقل','النجاح عند الأعطال الصامتة','متوسط زمن الحلقة (ثانية)','متوسط الرموز المولّدة لكل حلقة'),
 hsil='الأعطال الصامتة',
 sil='في العطل الصامت تبلغ الأداة عن النجاح من دون تنفيذ الإجراء، كأن تؤكد الكتابة دون تغيير حالة الملف. اعتمد B على التغذية الراجعة المعتادة من الأداة فنجح في {sb} حلقة من {sn}. ونجح D في {sd} من {sn} ({sdp})، وبقيت {fail} حلقة فاشلة.',
 hdes='التصميم',
 des='{bt} مهمة أساسية، لكل منها نسخة عربية وأخرى إنجليزية: 32 مهمة استدلال (في الحالة النظيفة فقط) و64 مهمة أدوات (ثلاث حالات، إحداها العطل الصامت). شُغّلت كل حالة ثلاث مرات: 32×2×3 + 64×2×3×3 = {en_} حلقة لكل ذراع، و{et} حلقة عبر الأذرع الستة. النموذج: {model}، وهو نموذج محلي واحد، مع أدوات محاكاة.',
 arms='<b>B</b>: الذراع المرجعية ذات المسار الثابت الداعم للأدوات، وتعتمد على التغذية الراجعة المعتادة من الأداة. <b>D</b>: توجيه بعقد المهمة مع تحقق وإصلاح محدود. وتوصف الأذرع الأربعة الأخرى في الورقة.',
 hlim='حدود الدراسة',
 lim=('الأدوات محاكاة وليست خدمات حقيقية.','نموذج محلي واحد ({model}) و{bt} مهمة أساسية.','استهلك D موارد أكثر من B: {dsec} ثانية ({dsecp}) و{dtok} رمزًا ({dtokp}) في كل حلقة.','لم تخضع الورقة الأولية للتحكيم.'),
 home='في تقييم شمل {bt} مهمة أساسية، لكل منها نسخة عربية وأخرى إنجليزية، رفع ACO‑LLM معدل النجاح وفق مقيّم مستقل بمقدار {dpp} نقطة مئوية مقارنة بالذراع المرجعية ذات المسار الثابت الداعم للأدوات. استخدم التقييم أدوات محاكاة ونموذجًا محليًا واحدًا ({model}). <a href="{rec}">اقرأ ورقة النتائج الأولية</a>',
 proto='يصف البروتوكول تصميم التقييم. نُفّذ التقييم ونُشرت نتائجه في ورقة مستقلة.'),
'fr': dict(dir='ltr', title='Résultats de l’évaluation ACO‑LLM · Kasem Adra',
 desc='Évaluation d’ACO‑LLM : {delta} points de pourcentage de réussite par rapport à un bras de référence utilisant un routage fixe avec accès aux outils, avec des outils simulés et un seul modèle local. Prépublication.',
 h1='ACO‑LLM : résultats de l’évaluation', badge='PRÉPUBLICATION DES RÉSULTATS · NON ÉVALUÉE PAR LES PAIRS',
 lead='Résumé de l’évaluation conçue dans le <a href="../aco-llm/">protocole</a>. La source de référence est la <a href="{rec}">prépublication des résultats sur Zenodo</a> (<a href="{pdf}">PDF</a>).',
 summary_title='En termes simples',
 summary='Cette évaluation a testé si des contrôles explicites et une correction limitée pouvaient améliorer l’exécution des tâches. Dans ce benchmark, le bras D a dépassé le bras B de {dpp} points de pourcentage selon un évaluateur indépendant. Le test a utilisé un seul modèle local et des outils simulés ; il ne démontre pas le même gain avec d’autres modèles ou des services réels.',
 hmain='Estimation principale',
 main='Le bras D, qui associait routage fondé sur le contrat de tâche, vérification structurelle et correction limitée, a augmenté le taux de réussite des tâches, selon l’évaluateur indépendant, de <b>{dpp} points de pourcentage</b> par rapport au bras de référence utilisant un routage fixe avec accès aux outils (bras B). Intervalle de confiance à 95 % : de {lo} à {hi}.',
 method='Méthode : les différences appariées ont été moyennées pour chacune des {bt} tâches de base, puis les tâches de base ont reçu un poids égal. L’intervalle provient de {nres} rééchantillonnages des tâches de base au sein de leurs strates.',
 hraw='Taux bruts et coût', pp='pts', s='s',
 rawnote='Les taux bruts comptent chaque épisode : les tâches avec outils (exécutées dans trois conditions) pèsent donc plus que les tâches de raisonnement, alors que l’estimation principale donne le même poids à chaque tâche de base. Écart brut : {gap} pts.',
 th=('Mesure','B','D','Écart'), rows=('Réussite, évaluateur indépendant','Réussite en cas de panne silencieuse','Durée moyenne par épisode (s)','Jetons générés par épisode (moyenne)'),
 hsil='Pannes silencieuses',
 sil='Dans une panne silencieuse, l’outil signale un succès sans exécuter l’action, par exemple en confirmant une écriture sans modifier le fichier. Le bras B s’appuie sur le retour habituel de l’outil et n’a réussi aucun des {sn} épisodes. Le bras D en a réussi {sd} sur {sn} ({sdp}) ; {fail} épisodes ont tout de même échoué.',
 hdes='Conception',
 des='{bt} tâches de base, chacune en version arabe et anglaise : 32 tâches de raisonnement (condition propre uniquement) et 64 tâches avec outils (trois conditions, dont la panne silencieuse). Chaque cas a été exécuté trois fois : 32×2×3 + 64×2×3×3 = {en_} épisodes par bras, {et} pour les six bras. Modèle : {model}, un seul modèle local, avec des outils simulés.',
 arms='<b>B</b> : bras de référence utilisant un routage fixe avec accès aux outils, qui s’appuie sur le retour habituel de l’outil. <b>D</b> : aiguillage par contrat de tâche avec vérification et réparation limitée. Les quatre autres bras sont décrits dans la prépublication.',
 hlim='Limites',
 lim=('Les outils étaient simulés, pas de vrais services.','Un seul modèle local ({model}) et {bt} tâches de base.','D a consommé plus que B : {dsec} s ({dsecp}) et {dtok} jetons ({dtokp}) de plus par épisode.','La prépublication n’a pas été évaluée par les pairs.'),
 home='Dans une évaluation de {bt} tâches de base, chacune en version arabe et anglaise, ACO‑LLM a augmenté le taux de réussite, selon un évaluateur indépendant, de {dpp} points de pourcentage par rapport au bras de référence utilisant un routage fixe avec accès aux outils. L’évaluation a utilisé des outils simulés et un seul modèle local ({model}). <a href="{rec}">Lire la prépublication des résultats</a>',
 proto='Ce protocole décrit la conception de l’évaluation. L’évaluation a été réalisée et ses résultats ont été publiés dans un article distinct.'),
}

DOI = '10.5281/zenodo.24549236'
TITLE = 'Adaptive Cognitive Orchestration for Local Language Models: A Held-Out Evaluation of Structural Verification and Repair'
PATH = '/publications/aco-llm-results/'


def homepage_summary(lang):
    values = vals(lang)
    values['rec'] = '/' + lang + PATH
    return '<p>' + T[lang]['home'].format(**values) + '</p>'


def description(lang):
    return T[lang]['desc'].format(delta=num(M['delta_pp'], lang, sign=True))


VERIFICATION_EXAMPLE = {
    'ar': ('مثال من مهمة عربية', 'بعد تصحيح إخفاق في كتابة الناتج، احتوى ملف المجموع على 89 وملف حاصل الضرب على 1938. اجتاز الملفان الفحص البنيوي لأنهما احتويا على أعداد، لكن المقيّم المستقل سجّل إخفاقًا لأن حاصل الضرب الصحيح هو 1908. يقيس فرق النجاح المقارنة بين الذراعين كاملتين.'),
    'en': ('Example from an Arabic task', 'After a silent write failure was repaired, the sum file contained 89 and the product file contained 1938. Both files passed the structural check because they contained integers. The independent evaluator recorded a failure because the correct product was 1908. The success-rate difference compares the two arms as a whole.'),
    'fr': ('Exemple tiré d’une tâche en arabe', 'Après la correction d’un échec silencieux d’écriture, le fichier de la somme contenait 89 et celui du produit 1938. Les deux fichiers ont passé la vérification structurelle car ils contenaient des entiers. L’évaluateur indépendant a relevé un échec car le produit correct était 1908. L’écart de réussite compare les deux bras dans leur ensemble.'),
}

def render(lang):
    t = T[lang]
    values = vals(lang)
    fmt = lambda key: t[key].format(**values)
    labels = {
        'en': ('Citation', 'Results', 'Open the results page'),
        'ar': ('الاقتباس', 'النتائج', 'افتح صفحة النتائج'),
        'fr': ('Citation', 'Résultats', 'Consulter la page des résultats'),
    }
    headers = ''.join(f'<th scope="col">{label}</th>' for label in t['th'])
    rows = ''
    for label, key in zip(t['rows'], ('c1', 'c2', 'c3', 'c4')):
        b, d, delta = values[key]
        unit = ' ' + t['pp'] if key in ('c1', 'c2') else ''
        rows += f'<tr><th scope="row">{label}</th><td>{b}</td><td>{d}</td><td>{delta}{unit}</td></tr>'
    limits = ''.join(f'<li>{item.format(**values)}</li>' for item in t['lim'])
    return (
        f'<div class="subpage"><h1>{t["h1"]}</h1><p class="label">{t["badge"]}</p><p>{fmt("lead")}</p>'
        f'<h2>{t["summary_title"]}</h2><p>{fmt("summary")}</p>'
        f'<h2>{t["hmain"]}</h2><p>{fmt("main")}</p><p>{fmt("method")}</p>'
        f'<h2>{VERIFICATION_EXAMPLE[lang][0]}</h2><p>{VERIFICATION_EXAMPLE[lang][1]}</p>'
        f'<h2>{t["hraw"]}</h2><div class="results-table" tabindex="0" role="region" aria-label="{t["hraw"]}">'
        f'<table><thead><tr>{headers}</tr></thead><tbody>{rows}</tbody></table></div><p>{fmt("rawnote")}</p>'
        f'<h2>{t["hsil"]}</h2><p>{fmt("sil")}</p><h2>{t["hdes"]}</h2><p>{fmt("des")}</p><p>{fmt("arms")}</p>'
        f'<h2>{t["hlim"]}</h2><ul>{limits}</ul><h2>{labels[lang][0]}</h2>'
        f'<p lang="en" dir="ltr">Adra, K. (2026). <cite>{TITLE}</cite> [Preprint]. Zenodo. '
        f'<a href="https://doi.org/{DOI}">{DOI}</a></p></div>'
    )
