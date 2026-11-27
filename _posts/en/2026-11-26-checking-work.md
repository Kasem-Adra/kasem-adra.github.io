---
title: "How to Verify an AI Assistant’s Work: A Practical Guide"
description: "A practical guide to separating tool execution from outcome verification, with examples of files, values, silent failures and the limits of structural checks."
lang: "en"
permalink: "/en/blog/checking-work/"
date_published: "2026-11-26"
date_modified: "2026-11-27"
---

## A completion message is not evidence

When an AI assistant says “done”, it is reporting what it believes happened. That statement is not independent evidence that the task was completed. A tool may return a success message even though a file or record did not change. A file may also be created successfully while containing the wrong information.

A reliable check separates three things: what the assistant said, what the tool did, and the final state that can be inspected. The first does not prove the second or the third.

## A practical example: creating a text file

Suppose you ask an assistant to create a text file containing these two lines:

    CHECK-5831
    The price is zero, not missing.

The check should not stop when the assistant reports that the file was created. Inspect the expected path, confirm that the file exists, read it as UTF-8, and compare its contents with the requested text. The comparison should also detect extra or missing lines and any punctuation differences when an exact match is required.

This test proves something specific: the file exists and its contents match the expected text. It does not automatically prove that every other operation performed by the assistant was correct.

## Existence, structure and semantic correctness

Verification has different levels. They should not be treated as interchangeable:

- **Existence:** Was the file or record created at the expected location?
- **Structure:** Can the output be read, and does it follow the required format or schema?
- **Semantic correctness:** Are the values and their meaning correct for the original task?

A CSV file can pass checks for columns and data types while containing incorrect numbers. A text file can contain a valid integer but still fail to represent the right answer.

An example in the ACO-LLM evaluation illustrates the distinction. The sum file contained 89 and the product file contained 1938. Both passed the structural check because they contained integers, but the independent evaluator recorded a failure because the correct product was 1908. A valid structure is not the same as correct content. [See the results paper](https://doi.org/10.5281/zenodo.24549236).

## Why zero must not be confused with missing data

In many data contexts, zero is a real value. A missing value means that the value is unavailable or was not recorded. If a system converts zero to an empty value, or treats a missing field as zero, a report may look valid while changing the meaning of the data.

A task contract should therefore state whether zero is allowed, what an empty field means, and how missing values are represented. The validator should check those rules rather than merely checking whether a field exists.

## Silent failures

A silent failure occurs when a tool reports success without carrying out the requested action. For example, a write operation may report success even though the file has not changed. If the assistant relies only on the tool's message, it may claim completion while the final state remains unchanged.

A practical response is to read the state after the write and compare it with the expected result. If the check fails, the system may allow a bounded repair attempt while recording the attempt and its outcome. Retries should not become an open-ended loop or repeat side-effecting operations without safeguards.

In the published evaluation, reference arm B succeeded in 0 of 384 episodes under the silent-failure condition, while arm D succeeded in 363 of 384. This finding is limited to the tested environment, simulated tools and model; it is not a guarantee of the same performance with every system or real service. [Read the evaluation](https://doi.org/10.5281/zenodo.24549236).

## Designing an independent check

Define an acceptable outcome in a testable way before execution. Then choose a validator that matches the task:

1. Keep the expected value or state in the task contract.
2. Inspect the final state at its source, not through the assistant's description.
3. Use deterministic comparison when the result can be calculated or matched exactly.
4. Separate structural validation from checks of semantic correctness.
5. Set explicit time and attempt limits for repairs.
6. Record the action, outcome and error while avoiding unnecessary storage of secrets or personal data.

The validator does not always need to be another language model. For many tasks, reading a file, comparing values or checking a data schema is clearer and easier to reproduce.

## What verification cannot prove

A structural check alone cannot prove semantic correctness. A successful local operation does not prove that every data path remained local: an assistant may connect to an external service through a tool or speech service. A retry mechanism also cannot guarantee that every failure will be repaired.

The ACO-LLM evaluation used one local model and simulated tools, so its findings must be interpreted within that scope. The [ACO-LLM protocol](https://doi.org/10.5281/zenodo.24488951) describes the study design; the [results preprint](https://doi.org/10.5281/zenodo.24549236) reports the executed evaluation and its limitations. The results paper has not been peer reviewed.

## A short verification checklist

Before accepting a completion claim, ask:

- Does the result exist at the expected location?
- Can it be read?
- Does it match the required format?
- Are the values correct, rather than merely valid data types?
- Was the state checked after the tool ran?
- Were repair attempts bounded and recorded?
- Are there side effects or external services that should be disclosed?

The principle is simple: do not make the assistant the only evidence of its own success. Inspect the state left by execution, and choose a level of verification appropriate to the result.
