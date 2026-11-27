---
title: "Peut-on faire confiance à un assistant IA local ?"
seo_title: "Fiabilité des assistants IA locaux et vérification des tâches | Kasem Adra"
description: "Analyse de la fiabilité des assistants IA locaux : défaillances silencieuses, vérification indépendante, résultats et limites de l’évaluation ACO-LLM."
subtitle: "De l’exécution locale des modèles de langage aux agents capables d’agir et de vérifier leurs résultats"
summary: "Un message de réussite ne prouve pas qu’un agent IA a accompli une tâche. Cet article explique les défaillances silencieuses des outils, l’orientation des tâches, la vérification et la correction limitée, puis présente l’évaluation ACO-LLM, ses résultats publiés et les limites de leur interprétation."
lang: "fr"
permalink: "/fr/blog/local-ai-agent-reliability/"
date_published: "2026-11-27"
date_modified: "2026-11-27"
published_label: "27 novembre 2026"
modified_label: "27 novembre 2026"
category: "Article technique et recherche"
author: "Kasem Adra"
author_display: "Kasem Adra"
image: "/assets/local-ai-agent-reliability-hero.webp"
image_alt: "Poste de travail informatique consacré à la recherche sur l’IA locale, avec un schéma illustratif montrant un modèle local, une action par outil, un contrôle d’état et une évaluation indépendante."
image_caption: "Image illustrative générée par IA. L’interface à l’écran est représentative et ne constitue pas une capture réelle de l’environnement d’évaluation."
editorial_note: "Cet article est une présentation analytique. Il ne remplace ni le protocole de recherche ni la prépublication originale des résultats."
article_section: "Intelligence artificielle ; modèles locaux ; agents IA ; ingénierie de la fiabilité"
keywords: ["IA locale", "fiabilité des assistants IA locaux", "fiabilité des agents IA", "défaillance silencieuse", "vérification indépendante", "ACO-LLM", "Gemma 4", "modèles de langage locaux"]
about: ["Intelligence artificielle locale", "agents d’intelligence artificielle", "vérification de l’exécution des tâches", "ingénierie de la fiabilité"]
citations: [{"name":"ACO-LLM research protocol, version 1.7","url":"https://doi.org/10.5281/zenodo.24488951"},{"name":"ACO-LLM held-out evaluation preprint, version 1","url":"https://doi.org/10.5281/zenodo.24549236"},{"name":"Google DeepMind Gemma 4 model overview","url":"https://deepmind.google/models/gemma/gemma-4/"},{"name":"Ollama gemma4:12b-it-qat model listing","url":"https://ollama.com/library/gemma4:12b-it-qat"},{"name":"NIST AI 600-1 Generative AI Profile","url":"https://doi.org/10.6028/NIST.AI.600-1"},{"name":"OWASP Top 10 for Agentic Applications for 2026","url":"https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/"},{"name":"ReAct: Synergizing Reasoning and Acting in Language Models","url":"https://arxiv.org/abs/2210.03629"},{"name":"Reflexion: Language Agents with Verbal Reinforcement Learning","url":"https://arxiv.org/abs/2303.11366"},{"name":"AgentBench: Evaluating LLMs as Agents","url":"https://arxiv.org/abs/2308.03688"},{"name":"Tau-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains","url":"https://arxiv.org/abs/2406.12045"},{"name":"AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents","url":"https://arxiv.org/abs/2406.13352"}]
---
## Vue d’ensemble

Il est désormais possible d’exécuter des modèles de langage performants sur des ordinateurs personnels et de les relier à des outils capables de lire et d’écrire des fichiers, de transformer des données et d’effectuer des opérations en plusieurs étapes. Toutefois, la capacité à envoyer une commande ou à appeler un outil ne signifie pas que la tâche demandée a été correctement accomplie. Un assistant peut afficher un message de réussite alors que la modification attendue n’a pas eu lieu, ou que le résultat est incomplet ou incorrect.

Cet article examine la fiabilité des assistants IA locaux sous l’angle de l’ingénierie des systèmes et de l’évaluation des agents. Il prend **Adaptive Cognitive Orchestration for Resource-Constrained Local Language Models (ACO-LLM)** comme étude de cas : quel problème cette approche examine-t-elle, comment l’évaluation a-t-elle été conçue, que montrent les résultats publiés et quelles limites faut-il respecter dans leur interprétation ?

## En bref

| Élément | Description |
|---|---|
| Sujet | Fiabilité des assistants IA locaux et des agents utilisant des outils |
| Auteur | Kasem Adra |
| Étude de cas | ACO-LLM |
| Modèle utilisé dans l’évaluation | Gemma 4 12B IT QAT, identifiant gemma4:12b-it-qat [4](https://ollama.com/library/gemma4:12b-it-qat) |
| Corpus de tâches | 96 tâches de base, chacune en versions arabe et anglaise |
| Taille de l’évaluation | 8 064 épisodes répartis sur six bras expérimentaux |
| Comparaison principale | Bras D par rapport au bras B |
| Estimation principale | +20,83 points de pourcentage de réussite, avec un poids égal par tâche |
| Statut de publication | Prépublication des résultats, non évaluée par les pairs |

## 1. Que signifie l’intelligence artificielle locale ?

L’**inférence locale** désigne l’exécution d’un modèle et le traitement de ses entrées sur l’appareil de l’utilisateur ou sur une infrastructure qu’il contrôle, plutôt que l’envoi de la requête d’inférence à un service externe hébergé. Les modèles à poids ouverts permettent aux développeurs de télécharger les poids et de les exécuter ou de les adapter, sous réserve de la licence applicable.

La famille **Gemma 4** de Google DeepMind est un exemple de modèles à poids ouverts conçus pour différents usages, notamment le raisonnement, le code, les flux de travail agentiques et l’appel de fonctions. Les ressources nécessaires dépendent de la taille du modèle, de la précision des poids, de la fenêtre de contexte et du matériel disponible. [3](https://deepmind.google/models/gemma/gemma-4/)

Il convient néanmoins de distinguer trois notions :

- **Exécution locale :** l’endroit où le modèle fonctionne et où ses ressources sont gérées.
- **Confidentialité :** la manière dont les données sont traitées, stockées ou transmises à d’autres services.
- **Fiabilité :** la capacité à accomplir correctement une tâche et à démontrer que le résultat est conforme.

L’exécution locale ne prouve pas que tous les composants du système fonctionnent hors ligne. Un agent peut encore utiliser un navigateur, un service de recherche ou une API externe. La confidentialité doit donc être évaluée sur l’ensemble du flux de données, et non déduite du seul lieu où s’effectue l’inférence.

## 2. Du modèle de langage à l’agent IA

Un modèle de langage classique génère du texte en réponse à une entrée. Un **agent d’intelligence artificielle** ajoute des mécanismes lui permettant de planifier, d’utiliser des outils et d’interagir avec un environnement externe. Son cycle d’exécution peut être résumé ainsi :

1. Comprendre la demande de l’utilisateur et les conditions de réussite.
2. Déterminer si un raisonnement direct ou une interaction avec l’environnement est nécessaire.
3. Sélectionner les outils et les autorisations appropriés.
4. Exécuter une action et observer la réponse.
5. Examiner l’état obtenu au regard des critères d’acceptation.
6. Corriger un échec récupérable dans des limites définies, ou signaler que la tâche n’a pas été accomplie.

Cette évolution modifie la manière d’évaluer le système. Une réponse peut être convaincante sur le plan linguistique alors que le fichier n’a jamais été créé, que les données n’ont pas été enregistrées ou qu’un autre chemin a été modifié. Le système doit donc distinguer **ce que le modèle affirme avoir fait** de **ce que l’environnement démontre après l’exécution**.

## 3. Défaillance silencieuse : lorsqu’un outil annonce une réussite sans effectuer l’action

Une **défaillance silencieuse (silent failure)** se produit lorsqu’un outil renvoie une réponse qui laisse penser que l’opération a réussi, alors que le changement d’état demandé n’a pas eu lieu. Par exemple, un outil d’écriture de fichier peut confirmer une écriture alors que le fichier reste inchangé ou que les données spécifiées sont absentes.

La séquence peut être représentée ainsi :

- L’utilisateur demande la création d’un fichier contenant des données précises.
- L’agent transmet une commande d’écriture à un outil.
- L’outil renvoie un accusé de réussite.
- Le fichier est absent ou ne contient pas les données demandées.
- L’agent annonce que la tâche est terminée en se fondant uniquement sur l’accusé de l’outil.

Le problème n’est pas seulement une erreur de formulation. Il s’agit d’une déduction invalide à partir des éléments disponibles. L’accusé de l’outil prouve qu’une réponse donnée a été renvoyée ; à lui seul, il ne prouve pas que l’état demandé existe désormais.

Le contrôle approprié dépend de la tâche. Pour l’écriture d’un fichier, il peut s’agir de confirmer son existence au bon emplacement, de lire son contenu et de le comparer aux données attendues. Pour une transformation de données, il peut être nécessaire de vérifier le schéma, le nombre d’enregistrements, les valeurs finales et l’absence de modification des fichiers non concernés.

## 4. La méthodologie ACO-LLM

**Adaptive Cognitive Orchestration for Resource-Constrained Local Language Models (ACO-LLM)** étudie si une orientation fondée sur le contrat de tâche, la vérification des résultats et une correction limitée peuvent améliorer l’accomplissement des tâches évalué indépendamment.

La méthode ne suppose pas que chaque demande nécessite une planification approfondie ou l’utilisation d’outils. Elle distingue les tâches pouvant être traitées par inférence directe de celles qui nécessitent une modification de l’environnement.

### 4.1 Contrat de tâche et orientation

Un **contrat de tâche** décrit le résultat attendu, la nécessité ou non d’interagir avec l’environnement, les outils autorisés, les conditions d’acceptation observables et les effets secondaires interdits.

L’orientation utilise ces informations pour sélectionner un parcours d’exécution. L’objectif est d’éviter un traitement inutile pour les tâches simples tout en appliquant des contrôles supplémentaires lorsque la tâche exige une action externe.

Une précision est essentielle pour interpréter l’orientation : dans cette expérience, le modèle ne devait pas déduire à partir d’une demande libre en langage naturel si un outil était nécessaire. Chaque scénario de test comportait un indicateur de routage public dans son contrat de tâche. L’étude évalue donc l’orientation à partir de métadonnées connues, et non la capacité d’un routeur général à choisir un parcours à partir de demandes utilisateur non contraintes. [1](https://doi.org/10.5281/zenodo.24488951)

### 4.2 Vérification du résultat

Une tâche n’est pas considérée comme réussie simplement parce que le modèle ou un outil annonce son achèvement. L’état obtenu doit être comparé à des critères d’acceptation définis, idéalement par un évaluateur indépendant de l’affirmation de réussite du modèle.

Il faut distinguer les **contrôles structurels à l’exécution**, par exemple confirmer l’existence d’un fichier ou son format, d’un **évaluateur de référence indépendant** qui vérifie les valeurs attendues et l’état final. Un résultat peut satisfaire un contrôle structurel sans être correct sur le fond.

### 4.3 Correction limitée

Lorsqu’un échec récupérable est détecté, le système peut tenter une correction dans des limites prédéfinies concernant le nombre de tentatives, la durée, les appels d’outils et la consommation de ressources. Le but est d’éviter des répétitions incontrôlées, notamment lorsque les actions sont coûteuses ou peuvent avoir des effets secondaires.

### 4.4 Bras expérimentaux

L’évaluation a été conçue pour comparer six bras présentant des politiques différentes d’orientation, de vérification et de correction :

| Bras | Politique d’exécution |
|---|---|
| A | Inférence directe sans entrer dans la boucle d’outils |
| B | Parcours fixe avec outils, reposant sur le retour ordinaire des outils |
| C | Orientation selon le contrat de tâche sans vérification obligatoire |
| D | Orientation selon le contrat de tâche, avec vérification obligatoire et correction limitée pour les tâches utilisant des outils |
| E | Bras D avec mémoire structurée des échecs, limitée à l’épisode |
| F | Parcours fixe avec outils, vérification obligatoire et correction limitée |

Ces comparaisons permettent d’examiner différentes composantes de la politique. La comparaison principale, **D par rapport à B**, estime l’effet de la politique combinée ; elle ne permet pas, à elle seule, d’isoler l’effet de l’orientation de ceux de la vérification et de la correction. D’autres contrastes prévus, notamment C par rapport à B, D par rapport à F, F par rapport à B et D par rapport à C, contribuent à interpréter les composantes. [1](https://doi.org/10.5281/zenodo.24488951)

## 5. Conception de l’évaluation expérimentale

La prépublication des résultats décrit un ensemble de test réservé (held-out) de 96 tâches de base, après exclusion des 24 tâches pilotes et de tous leurs résultats. Les 96 tâches réservées étaient réparties à parts égales entre trois strates, soit 32 tâches chacune : raisonnement déterministe, transformation de données dans un fichier unique et flux de travail à sorties multiples. Chaque tâche disposait d’une variante arabe et d’une variante anglaise :

- 32 tâches de raisonnement déterministe, évaluées uniquement dans la condition propre.
- 32 tâches de transformation de données dans un fichier unique et 32 flux de travail à sorties multiples, chacun évalué dans trois conditions : exécution propre, échec explicite contrôlé et no-op silencieux dans lequel l’outil accuse réception de l’action sans modifier l’état.

Chaque cas planifié a été répété trois fois dans les six bras expérimentaux, avec des épisodes appariés selon la tâche de base, la langue, la panne attribuée et la répétition. Cela représente 1 344 épisodes par bras et **8 064 épisodes au total**. L’évaluation a utilisé des outils simulés dans un environnement contrôlé ; elle ne constituait pas un test de services réels ou d’API de production. [2](https://doi.org/10.5281/zenodo.24549236)

La prépublication des résultats indique les paramètres d’exécution suivants :

| Paramètre | Valeur |
|---|---|
| Modèle | gemma4:12b-it-qat ; préfixe d’identifiant 38044be4f923 |
| Environnement d’exécution | Ollama 0.40.18 |
| Longueur du contexte | 2 048 jetons |
| Température | 0 |
| Limite de génération par réponse | 512 jetons |
| Budget du contrôleur par épisode | 4 096 unités de jetons du contrôleur |
| Appels d’outils et de vérification | 8 au maximum par épisode |
| Tentatives de correction | 2 au maximum |
| Délai maximal du processus | 180 secondes par épisode |

Il s’agit des paramètres d’exécution indiqués dans la prépublication des résultats ; ils ne doivent pas être confondus avec les paramètres prospectifs décrits dans le protocole. [2](https://doi.org/10.5281/zenodo.24549236)

## 6. Principaux résultats

### 6.1 Estimation principale

L’estimation principale indique que le bras D a augmenté le taux de réussite des tâches, selon l’évaluateur indépendant, de **20,83 points de pourcentage** par rapport au bras B. L’intervalle de confiance à 95 % s’étend de 18,23 à 23,44 points de pourcentage.

Cette estimation a été calculée à partir des différences appariées au sein de chacune des 96 tâches de base, chaque tâche recevant le même poids. Un bootstrap en grappes comprenant 10 000 rééchantillonnages des tâches de base au sein de leurs strates a servi à estimer l’intervalle de confiance. [2](https://doi.org/10.5281/zenodo.24549236)

### 6.2 Taux bruts de réussite

Le tableau suivant présente les épisodes réussis et les taux bruts de réussite pour les six bras :

| Bras | Épisodes réussis | Taux brut de réussite |
|---|---:|---:|
| A | 111 sur 1 344 | 8,26 % |
| B | 834 sur 1 344 | 62,05 % |
| C | 839 sur 1 344 | 62,43 % |
| D | 1 192 sur 1 344 | 88,69 % |
| E | 1 203 sur 1 344 | 89,51 % |
| F | 1 191 sur 1 344 | 88,62 % |

L’écart brut entre B et D était de **26,64 points de pourcentage**. Il ne correspond pas à l’estimation principale de 20,83 points, car le taux brut compte chaque épisode, tandis que l’estimation principale donne le même poids à chaque tâche de base. Les tâches avec outils ont été exécutées dans trois conditions et contribuent donc davantage d’épisodes au taux brut. [2](https://doi.org/10.5281/zenodo.24549236)

### 6.3 Condition de défaillance silencieuse

Pour les épisodes affectés à la condition de défaillance silencieuse, les résultats des six bras étaient les suivants :

| Bras | Épisodes réussis | Taux de réussite |
|---|---:|---:|
| A | 0 sur 384 | 0,00 % |
| B | 0 sur 384 | 0,00 % |
| C | 0 sur 384 | 0,00 % |
| D | 363 sur 384 | 94,53 % |
| E | 363 sur 384 | 94,53 % |
| F | 363 sur 384 | 94,53 % |

Ces résultats montrent une amélioration importante pour les bras comportant une vérification et une correction limitée dans la condition précise testée. Ils ne signifient pas que toutes les défaillances silencieuses ont été résolues : 21 des 384 épisodes sont restés en échec dans chacun des bras D, E et F. [2](https://doi.org/10.5281/zenodo.24549236)

### 6.4 Coût d’exécution

Les durées moyennes et les jetons générés dans les six bras étaient les suivants :

| Bras | Durée moyenne par épisode | Moyenne des jetons générés |
|---|---:|---:|
| A | 1,547 s | 43,69 |
| B | 2,096 s | 44,57 |
| C | 2,055 s | 44,59 |
| D | 2,279 s | 49,83 |
| E | 2,286 s | 49,83 |
| F | 2,287 s | 49,81 |

Par rapport à B, le bras D a consommé en moyenne 0,183 seconde supplémentaire par épisode (+8,73 %) et généré 5,26 jetons supplémentaires (+11,80 %). La vérification et la correction ne doivent donc pas être présentées comme gratuites. [2](https://doi.org/10.5281/zenodo.24549236)

### 6.5 Contrastes secondaires et interprétation des composantes

Le tableau suivant présente les contrastes secondaires prévus, y compris l’interaction globale entre l’orientation et le bloc vérification-correction :

| Contraste | Différence (points de pourcentage) | Intervalle de confiance à 95 % |
|---|---:|---:|
| C − B | +0,87 | −1,04 à +2,95 |
| D − F | +0,17 | −2,08 à +2,60 |
| F − B | +20,66 | +19,27 à +21,88 |
| D − C | +19,97 | +18,23 à +21,35 |
| E − D | +0,87 | +0,17 à +1,91 |
| (D − F) − (C − B) | −0,69 | −1,91 à +0,35 |

Sur les seules tâches de raisonnement déterministe, la différence médiane appariée de latence entre D et B était de −47 millisecondes (de −78 à −31). Dans l’analyse des pannes attribuées, la différence de réussite entre D et C était de +46,48 points de pourcentage (de +43,36 à +48,83), que l’exécution ait ou non atteint le déclencheur de panne.

Ces contrastes sont secondaires et exploratoires, et leurs intervalles ne sont pas ajustés pour les comparaisons multiples. Les intervalles de C−B et D−F incluent zéro : l’étude n’a donc pas établi d’effet positif distinct de l’orientation dans ces deux comparaisons, sans pour autant démontrer l’absence d’effet ou l’équivalence. En revanche, F−B et D−C sont positifs ; ils comparent tous deux l’ajout du bloc vérification-correction sous des politiques d’orientation différentes. Comme la vérification et la correction ont été testées ensemble, leurs effets respectifs ne peuvent pas être isolés. L’intervalle de l’interaction inclut également zéro et ne fournit pas de preuve claire d’une interaction. [2](https://doi.org/10.5281/zenodo.24549236)

## 7. Que signifie le terme « vérification » dans cette évaluation ?

Tous les contrôles n’apportent pas le même niveau de preuve. Un contrôle d’exécution que l’agent peut utiliser pendant le traitement est différent d’un évaluateur indépendant chargé de déterminer si le résultat final est correct.

Dans un exemple de l’évaluation, un résultat a passé un contrôle structurel parce qu’il contenait des nombres entiers, mais il ne correspondait pas à la valeur correcte vérifiée par l’évaluateur indépendant : le produit attendu était 1908, tandis que le résultat contenait 1938. Cet exemple montre pourquoi la validité structurelle n’est pas équivalente à l’exactitude du contenu. [2](https://doi.org/10.5281/zenodo.24549236)

Les critères d’acceptation doivent donc correspondre à la tâche. L’existence d’un fichier ne suffit pas lorsque son contenu doit également être contrôlé. Un schéma CSV valide ne prouve pas que toutes les valeurs sont correctes, et l’achèvement d’une étape intermédiaire ne prouve pas la réussite de l’ensemble du processus.

La qualité de l’évaluation dépend également de celle de l’évaluateur et de sa capacité à rejeter les sorties incorrectes et les effets secondaires interdits.

### 7.1 Limites du vérificateur structurel

Dans les bras dotés d’une porte de vérification, le vérificateur structurel a accepté 69 épisodes dans D, 60 dans E et 69 dans F alors que l’évaluateur indépendant les avait classés comme des échecs, soit 198 cas au total. Cela montre que vérifier la présence ou la structure d’un fichier ne revient pas à vérifier l’exactitude de son contenu. [2](https://doi.org/10.5281/zenodo.24549236)

### 7.2 Déclarations d’achèvement

La prépublication ne recense aucune déclaration de réussite structurée émise par le modèle via l’action structurée final_success prévue à cet effet. Le dénominateur du taux conditionnel de fausses déclarations était donc nul, et ce taux n’a pas pu être estimé. Les achèvements automatiques effectués par le moteur d’exécution lui ont été attribués, et non au modèle. L’expérience ne quantifie donc pas les fausses déclarations d’achèvement dans les réponses en langage naturel. [2](https://doi.org/10.5281/zenodo.24549236)

## 8. Limites des résultats et conclusions non établies

Les résultats étayent une conclusion circonscrite : dans le corpus de tâches, l’environnement et le modèle testés, la politique D a obtenu un taux de réussite évalué indépendamment supérieur à celui du bras de référence B. Ils ne démontrent pas que le même résultat sera obtenu dans tous les déploiements ou environnements de production.

Les principales limites sont les suivantes :

- **Un seul modèle :** l’évaluation a utilisé uniquement Gemma 4 12B IT QAT. Les résultats ne peuvent pas être généralisés automatiquement à d’autres modèles.
- **Outils simulés :** les outils simulés ne reproduisent pas tous les problèmes liés aux services réels, aux réseaux ou aux permissions.
- **Un corpus défini :** l’analyse réservée a utilisé 96 tâches de base après exclusion de 24 tâches pilotes ; cet ensemble ne représente pas nécessairement toutes les tâches de longue durée ou les flux de travail professionnels.
- **Métadonnées de routage publiques :** l’indicateur de routage était fourni dans le contrat de tâche ; l’expérience n’a pas testé l’inférence du parcours à partir du langage naturel.
- **Types de défaillances spécifiques :** l’évaluation comprenait des échecs explicites contrôlés et des no-op silencieux ; elle ne démontre pas une robustesse à toutes les attaques ou défaillances persistantes.
- **Limites de la vérification :** un contrôle structurel seul ne peut pas prouver l’exactitude sémantique ou la véracité de faits ouverts ; certaines sorties acceptées structurellement ont été rejetées par l’évaluateur indépendant.
- **Coût supplémentaire :** le bras D a consommé en moyenne davantage de temps et de jetons générés par épisode que le bras B.
- **Inventaire incomplet de l’environnement :** la prépublication indique qu’un inventaire complet du matériel et du système d’exploitation n’était pas disponible pour cette version.
- **Statut de publication :** les résultats sont présentés dans une prépublication qui n’a pas été évaluée par les pairs. L’intervalle de confiance décrit l’incertitude selon le plan de rééchantillonnage de ce benchmark ; il ne garantit pas la généralisation à d’autres environnements.

La prépublication indique qu’une archive complémentaire contient les journaux, le calendrier apparié, les sources du moteur d’exécution, le script d’analyse, les résultats lisibles par machine et un manifeste de gel. Toutefois, la page du registre Zenodo lié ne présentait que le PDF de la prépublication lors de sa vérification le 27 novembre 2026 ; elle n’exposait pas de lien de téléchargement distinct vers cette archive. Un lien direct est nécessaire pour que les lecteurs puissent examiner ces éléments de manière indépendante. [2](https://doi.org/10.5281/zenodo.24549236)

Le protocole de recherche et l’article de résultats sont deux documents distincts : le protocole décrit la conception et les règles d’analyse, tandis que la prépublication présente l’évaluation et ses résultats. [1](https://doi.org/10.5281/zenodo.24488951) [2](https://doi.org/10.5281/zenodo.24549236)

## 9. Considérations d’ingénierie et de sécurité pour des agents fiables

La fiabilité ne se limite pas au contrôle de l’exactitude des résultats. Un agent capable de lire ou de modifier des fichiers ou d’exécuter des commandes doit également respecter des limites de sécurité explicites.

Les pratiques fondamentales comprennent :

- **Moindre privilège :** accorder à l’agent uniquement les accès nécessaires à sa tâche et limiter les chemins et commandes autorisés.
- **Séparation de la planification et de l’exécution :** la décision du modèle ne doit pas suffire à autoriser une opération sensible ou irréversible.
- **Approbation humaine lorsque nécessaire :** demander une confirmation avant une suppression, une publication, une transmission de données ou une modification importante.
- **Journaux auditables :** enregistrer les commandes, les résultats, les erreurs et les tentatives de correction, tout en évitant de conserver inutilement des secrets ou des données personnelles.
- **Limites de temps et de ressources :** définir des délais d’exécution, des limites d’appels d’outils et des budgets de correction.
- **Considérer les contenus externes comme non fiables :** les fichiers, les pages web et les messages des outils peuvent contenir des instructions trompeuses et ne doivent pas être automatiquement considérés comme des commandes fiables.

Des cadres tels que le profil NIST de gestion des risques liés à l’IA générative et l’OWASP Top 10 pour les applications agentiques abordent des aspects connexes de gouvernance et de sécurité, notamment le mauvais usage des outils, les abus de privilèges et la manipulation du contexte. Ce sont des références complémentaires, et non la preuve que l’évaluation ACO-LLM a testé tous ces risques. [5](https://doi.org/10.6028/NIST.AI.600-1) [6](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)

## 10. Relations avec les travaux antérieurs

ACO-LLM s’inscrit dans un domaine de recherche plus large qui étudie le passage des modèles de langage de la génération de texte à l’interaction avec des outils et des environnements. Les travaux cités ci-dessous sont des exemples choisis en lien avec le sujet ; ils ne constituent pas une revue systématique de la littérature.

- **ReAct** a proposé une approche combinant raisonnement, actions et interaction avec l’environnement. [7](https://arxiv.org/abs/2210.03629)
- **Reflexion** a étudié l’utilisation du retour d’expérience et de la mémoire verbale pour améliorer les agents au fil des tentatives. [8](https://arxiv.org/abs/2303.11366)
- **AgentBench** a introduit un cadre d’évaluation des modèles de langage en tant qu’agents dans des environnements interactifs. [9](https://arxiv.org/abs/2308.03688)
- **τ-bench** s’est intéressé à l’interaction entre l’agent, l’outil et l’utilisateur, ainsi qu’à l’évaluation des résultats dans des domaines pratiques. [10](https://arxiv.org/abs/2406.12045)
- **AgentDojo** a fourni un environnement pour étudier l’injection de prompts et les attaques contre les agents utilisant des outils. [11](https://arxiv.org/abs/2406.13352)

ACO-LLM ne prétend pas que l’utilisation d’outils, la vérification externe ou l’orientation adaptative constituent individuellement des idées nouvelles. Sa question de recherche porte sur une intégration précise de l’orientation selon le contrat de tâche, de la vérification et de la correction limitée, sur un modèle local fixe, évaluée avec des tâches bilingues, des injections de défaillances contrôlées et une comptabilisation des ressources. [1](https://doi.org/10.5281/zenodo.24488951)

## 11. Questions fréquentes

### L’exécution locale d’un assistant IA garantit-elle la confidentialité ?

Non. L’inférence locale peut réduire la nécessité d’envoyer les entrées du modèle à un service externe, mais un agent peut encore utiliser des outils ou services en ligne. L’évaluation de la confidentialité nécessite d’examiner les flux de données, les permissions, le stockage et les journaux.

### L’amélioration de 20,83 points de pourcentage signifie-t-elle que le modèle est devenu plus intelligent ?

Non. Le résultat compare deux politiques d’exécution, D et B, en utilisant le même modèle local. Il indique une amélioration de la réussite des tâches dans les conditions d’évaluation, et non une augmentation de l’intelligence du modèle sous-jacent.

### Pourquoi la différence principale est-elle différente de la différence brute ?

L’estimation principale donne le même poids aux 96 tâches de base, tandis que le taux brut compte chaque épisode d’exécution. Les tâches avec outils comportent trois conditions et contribuent donc davantage d’épisodes au taux brut.

### L’évaluation a-t-elle prouvé qu’ACO-LLM fonctionne avec des outils réels ?

Non. L’évaluation a utilisé des outils simulés dans un environnement contrôlé. Une évaluation distincte avec des services réels est nécessaire avant de généraliser les résultats aux environnements de production.

### L’article de résultats a-t-il été évalué par les pairs ?

Non. Il s’agit d’une prépublication de résultats qui n’a pas été évaluée par les pairs. Ses méthodes et ses résultats sont accessibles sur Zenodo et doivent être interprétés en tenant compte de ce statut.

### ACO-LLM déduit-il automatiquement du texte libre de l’utilisateur qu’un outil est nécessaire ?

Non. Dans l’évaluation, l’indicateur de routage était fourni dans le contrat de tâche. L’expérience n’a pas testé la précision du routage sur des demandes en langage naturel non contraintes.

### L’expérience a-t-elle mesuré les fausses déclarations d’achèvement ?

Non. La prépublication ne recense aucune déclaration de réussite structurée émise par le modèle ; il n’existait donc aucun dénominateur permettant d’estimer un taux conditionnel de fausses déclarations. L’expérience n’établit pas le taux de fausses déclarations dans les réponses en langage naturel.

## Publications de recherche et pages associées

Pour consulter les documents de recherche à l’origine de cette analyse, voir :
- [Page du protocole ACO-LLM sur ce site](https://kasemadra.com/fr/publications/aco-llm/).
- [Page des résultats de l’évaluation ACO-LLM sur ce site](https://kasemadra.com/fr/publications/aco-llm-results/).
- [Protocole de recherche ACO-LLM sur Zenodo](https://doi.org/10.5281/zenodo.24488951).
- [Prépublication des résultats ACO-LLM sur Zenodo](https://doi.org/10.5281/zenodo.24549236).

## Conclusion

La fiabilité d’un assistant IA ne devrait pas être mesurée à l’assurance de ses réponses ni à sa facilité à annoncer l’achèvement d’une tâche. Le critère le plus important est la conformité de l’état final à la demande et la possibilité de fournir des éléments de preuve appropriés.

L’évaluation ACO-LLM indique que l’orientation selon les exigences de la tâche, la vérification et la correction limitée peuvent améliorer la réussite des tâches dans un environnement local contrôlé. Elle met également en évidence un coût supplémentaire en ressources et des limites liées au modèle unique, aux outils simulés et à la portée du corpus de test.

**La confiance envers un agent ne vient pas de sa déclaration « tâche terminée », mais de preuves vérifiables que l’exécution a satisfait aux exigences de la tâche.**

## Références

1. Adra, K. (2026). *Adaptive Cognitive Orchestration for Resource-Constrained Local Language Models (ACO-LLM): A Contract-Driven Research Protocol with Formal Guarantees and Reference Implementation* (Version 1.7). Zenodo. [DOI : 10.5281/zenodo.24488951](https://doi.org/10.5281/zenodo.24488951).
2. Adra, K. (2026). *Adaptive Cognitive Orchestration for Local Language Models: A Held-Out Evaluation of Structural Verification and Repair* [Prépublication, v1]. Zenodo, 26 novembre 2026. [DOI : 10.5281/zenodo.24549236](https://doi.org/10.5281/zenodo.24549236).
3. Google DeepMind. *Gemma 4.* Présentation officielle du modèle. [Page du modèle](https://deepmind.google/models/gemma/gemma-4/).
4. Ollama. *gemma4:12b-it-qat* [Fiche du modèle]. [Bibliothèque Ollama](https://ollama.com/library/gemma4:12b-it-qat).
5. Autio, C. et al. (2024). *Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile.* NIST AI 600-1. [DOI](https://doi.org/10.6028/NIST.AI.600-1).
6. OWASP GenAI Security Project. (2025). *OWASP Top 10 for Agentic Applications for 2026.* [Source](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/).
7. Yao, S. et al. (2022). *ReAct: Synergizing Reasoning and Acting in Language Models.* [arXiv:2210.03629](https://arxiv.org/abs/2210.03629).
8. Shinn, N. et al. (2023). *Reflexion: Language Agents with Verbal Reinforcement Learning.* [arXiv:2303.11366](https://arxiv.org/abs/2303.11366).
9. Liu, X. et al. (2023). *AgentBench: Evaluating LLMs as Agents.* [arXiv:2308.03688](https://arxiv.org/abs/2308.03688).
10. Yao, S. et al. (2024). *τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains.* [arXiv:2406.12045](https://arxiv.org/abs/2406.12045).
11. Debenedetti, E. et al. (2024). *AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents.* [arXiv:2406.13352](https://arxiv.org/abs/2406.13352).
