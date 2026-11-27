---
title: "Comment vérifier le travail d’un assistant IA ? Guide pratique"
description: "Un guide pratique pour distinguer l’exécution d’un outil de la vérification du résultat, avec des exemples de fichiers, de valeurs, de pannes silencieuses et des limites des contrôles structurels."
lang: "fr"
permalink: "/fr/blog/checking-work/"
date_published: "2026-11-26"
date_modified: "2026-11-27"
---

## Un message de réussite n’est pas une preuve

Lorsqu’un assistant IA répond « terminé », il indique ce qu’il pense avoir accompli. Cette déclaration ne constitue pas une preuve indépendante que la tâche a réellement été exécutée. Un outil peut renvoyer un message de réussite alors qu’un fichier ou un enregistrement n’a pas changé. Un fichier peut également être créé correctement sur le plan technique tout en contenant des informations erronées.

Une vérification fiable distingue donc trois éléments : ce que l’assistant a déclaré, ce que l’outil a exécuté et l’état final qui peut être inspecté. Le premier ne prouve ni le deuxième ni le troisième.

## Exemple pratique : créer un fichier texte

Supposons que vous demandiez à un assistant de créer un fichier texte contenant les deux lignes suivantes :

    CHECK-5831
    The price is zero, not missing.

La vérification ne doit pas s’arrêter au message indiquant que le fichier a été créé. Il faut examiner le chemin attendu, confirmer que le fichier existe, le relire en UTF-8 et comparer son contenu au texte demandé. La comparaison doit également détecter les lignes supplémentaires ou manquantes et les différences de ponctuation lorsqu’une correspondance exacte est requise.

Ce contrôle prouve un point précis : le fichier existe et son contenu correspond au texte attendu. Il ne prouve pas automatiquement que toutes les autres opérations de l’assistant sont correctes.

## Existence, structure et exactitude sémantique

La vérification comporte plusieurs niveaux qu’il ne faut pas confondre :

- **Existence :** le fichier ou l’enregistrement a-t-il été créé à l’emplacement prévu ?
- **Structure :** le résultat est-il lisible et respecte-t-il le format ou le schéma demandé ?
- **Exactitude sémantique :** les valeurs et leur signification sont-elles correctes au regard de la tâche initiale ?

Un fichier CSV peut réussir les contrôles de colonnes et de types tout en contenant des nombres erronés. Un fichier texte peut contenir un entier valide sans pour autant représenter la bonne réponse.

Un exemple de l’évaluation ACO-LLM illustre cette différence. Le fichier de somme contenait 89 et le fichier du produit 1938. Les deux ont passé le contrôle structurel parce qu’ils contenaient des entiers, mais l’évaluateur indépendant a enregistré un échec : le produit correct était 1908. Une structure valide ne signifie pas que le contenu est exact. [Voir l’article de résultats](https://doi.org/10.5281/zenodo.24549236).

## Pourquoi ne pas confondre zéro et donnée manquante ?

Dans de nombreux contextes, zéro est une valeur réelle. Une donnée manquante signifie que la valeur n’est pas disponible ou n’a pas été enregistrée. Si un système transforme zéro en champ vide, ou traite un champ manquant comme zéro, un rapport peut sembler valide tout en modifiant le sens des données.

Le contrat de tâche doit donc préciser si zéro est autorisé, ce que signifie un champ vide et comment représenter une valeur manquante. Le validateur doit contrôler ces règles au lieu de vérifier uniquement la présence du champ.

## Les défaillances silencieuses

Une défaillance silencieuse se produit lorsqu’un outil signale une réussite sans avoir effectué l’action demandée. Par exemple, une opération d’écriture peut annoncer son succès alors que le fichier n’a pas été modifié. Si l’assistant se fie uniquement au message de l’outil, il peut annoncer la fin de la tâche alors que l’état final est inchangé.

Une réponse pratique consiste à relire l’état après l’écriture et à le comparer au résultat attendu. Si le contrôle échoue, le système peut autoriser une tentative de correction limitée, tout en enregistrant cette tentative et son résultat. Les nouvelles tentatives ne doivent pas devenir une boucle sans fin ni répéter des opérations à effets de bord sans garde-fous.

Dans l’évaluation publiée, le bras de référence B a réussi 0 épisode sur 384 dans la condition de défaillance silencieuse, tandis que le bras D en a réussi 363 sur 384. Ce résultat est limité à l’environnement testé, aux outils simulés et au modèle utilisé ; il ne garantit pas des performances identiques avec tous les systèmes ou services réels. [Consulter l’évaluation](https://doi.org/10.5281/zenodo.24549236).

## Concevoir un contrôle indépendant

Définissez un résultat acceptable de manière vérifiable avant l’exécution. Choisissez ensuite un validateur adapté à la tâche :

1. Conservez la valeur ou l’état attendu dans le contrat de tâche.
2. Inspectez l’état final à sa source, et non à travers la description de l’assistant.
3. Utilisez une comparaison déterministe lorsque le résultat peut être calculé ou comparé exactement.
4. Distinguez la validation structurelle du contrôle de l’exactitude sémantique.
5. Fixez des limites explicites de durée et de nombre de tentatives de correction.
6. Enregistrez l’action, le résultat et l’erreur, sans conserver inutilement des secrets ou des données personnelles.

Le validateur n’a pas toujours besoin d’être un autre modèle de langage. Pour de nombreuses tâches, relire un fichier, comparer des valeurs ou contrôler un schéma de données est plus clair et plus reproductible.

## Ce que la vérification ne prouve pas

Un contrôle structurel ne suffit pas à démontrer l’exactitude sémantique. Une opération locale réussie ne prouve pas que tous les flux de données sont restés locaux : un assistant peut se connecter à un service externe par l’intermédiaire d’un outil ou d’un service vocal. Un mécanisme de nouvelle tentative ne garantit pas non plus la correction de toutes les défaillances.

L’évaluation ACO-LLM a utilisé un seul modèle local et des outils simulés. Ses résultats doivent donc être interprétés dans ce périmètre. Le [protocole ACO-LLM](https://doi.org/10.5281/zenodo.24488951) décrit le plan de l’étude ; la [prépublication des résultats](https://doi.org/10.5281/zenodo.24549236) présente l’évaluation réalisée et ses limites. L’article de résultats n’a pas été évalué par les pairs.

## Liste de vérification

Avant d’accepter une déclaration d’achèvement, demandez-vous :

- Le résultat existe-t-il à l’emplacement attendu ?
- Peut-on le lire ?
- Respecte-t-il le format demandé ?
- Les valeurs sont-elles exactes, et pas seulement conformes à un type de données ?
- L’état a-t-il été contrôlé après l’exécution de l’outil ?
- Les tentatives de correction ont-elles été limitées et enregistrées ?
- Existe-t-il des effets secondaires ou des services externes à signaler ?

Le principe est simple : ne faites pas de l’assistant la seule preuve de sa propre réussite. Inspectez l’état laissé par l’exécution et choisissez un niveau de vérification adapté au résultat.
