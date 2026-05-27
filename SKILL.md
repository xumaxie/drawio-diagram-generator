---
name: drawio-diagram-generator
description: Generate a `.drawio` file that can be opened directly in draw.io from natural-language requirements. Use when the user wants a flowchart, UML, architecture diagram, sequence diagram, ER diagram, swimlane diagram, or a revision to existing draw.io XML. This skill first checks whether the request is specific enough, asks for missing details when needed, then writes a valid draw.io file with a clean layout and a strict output protocol.
license: MIT
---

# Draw.io Diagram Generator

## Overview

This skill turns a user's diagram request into a usable draw.io file. It is based on a backend workflow that proved useful in practice: analyze first, draw second, review last.

Use this skill when the user wants:

- a new draw.io file
- draw.io XML from a text description
- edits to an existing draw.io diagram
- a diagram derived from repository structure, code, API flow, or business process

Read [references/protocol.md](references/protocol.md) first, then use the workflow below. If you need a starter XML structure or layout rules, read [references/xml-template.md](references/xml-template.md). If you want reusable prompting language, read [references/prompt-snippets.md](references/prompt-snippets.md).

## Core Workflow

Follow this three-stage workflow every time:

1. Analyze the request.
2. Generate the diagram.
3. Review, write the file, and validate it.

Do not skip the analysis step just because the user mentioned draw.io. The backend's main insight is that diagram quality improves a lot when you decide whether to clarify before drawing.

## Stage 1: Analyze First

Decide whether the request is specific enough to draw immediately.

Treat the request as ready only if you can confidently infer most of the following:

- diagram type
- major nodes or participants
- relationships or flow direction
- grouping or boundaries
- any important labels

If the request is underspecified, do not invent a full diagram prematurely. Ask a focused follow-up that reduces ambiguity quickly. Prefer one compact clarification message that asks for the highest-leverage missing details.

When the environment or prompt requires a machine-readable protocol, use the `user` response shape from [references/protocol.md](references/protocol.md).

If the user provided repository context, local files, existing XML, or architecture text, use that material as source-of-truth before asking follow-up questions.

## Stage 2: Generate Draw.io XML

Once the request is clear enough, produce draw.io-compatible XML that will be written to a `.drawio` file.

Requirements:

- Output must represent a complete draw.io document or a valid `mxGraphModel` payload.
- Prefer a readable layout over packing too much information into one canvas.
- Keep line routing simple and reduce obvious edge crossings.
- Use stable IDs within the document.
- Make labels explicit instead of relying on visual inference.
- Separate containers, services, databases, actors, and decisions clearly.

Generation rules:

- Use top-to-bottom or left-to-right flow consistently unless the user requests otherwise.
- For architecture diagrams, cluster by layer, domain, or boundary.
- For flowcharts, reserve diamonds for decisions and rectangles for actions.
- For sequence diagrams, order participants logically and avoid unnecessary returns.
- For updates to existing XML, preserve the user's existing structure where possible instead of regenerating everything blindly.

Use the base patterns in [references/xml-template.md](references/xml-template.md) whenever you need a safe starting point.

## Stage 3: Review Before Final Output

Before returning the result, run this checklist:

- Is the XML well-formed?
- Is the root tag acceptable for draw.io?
- Are there obvious missing closing tags or broken escaping issues?
- Does the layout direction stay consistent?
- Are there likely edge crossings or overlapping blocks that can be reduced textually?
- Did you accidentally output Markdown fences, commentary, or mixed JSON/XML?

The default deliverable is a local `.drawio` file. After writing it, validate it with `scripts/validate_drawio_xml.py`.

## Output Modes

Choose the output mode that matches the task:

### Mode A: Conversational clarification

Use when information is missing. Ask for missing details directly, or if a structured protocol is needed, emit the `user` JSON contract from [references/protocol.md](references/protocol.md).

### Mode B: Direct XML

Use only when the user explicitly wants raw draw.io XML instead of a file. In this mode:

- output XML only
- do not wrap it in Markdown fences
- do not add explanations before or after the XML

### Mode C: Wrapped drawio payload

Use when the caller expects the backend-style front-end protocol instead of a file. Emit the `drawio` JSON contract from [references/protocol.md](references/protocol.md), with the XML in `content`.

## Working With Existing Draw.io XML

When the user provides existing XML:

1. Inspect it first.
2. Determine whether the request is a patch, extension, cleanup, or relayout.
3. Preserve valid existing nodes and IDs where practical.
4. Avoid discarding the entire diagram unless the XML is unusable or the user asked for a rewrite.

If the XML is malformed, explain the specific breakage briefly and either repair it or ask permission to regenerate.

## Defaults That Usually Work Well

Unless the user specifies otherwise:

- flowchart direction: top to bottom
- architecture diagram direction: left to right by layer
- keep labels concise
- avoid decorative styling unless asked
- prefer fewer crossings over perfect symmetry
- return one coherent diagram, not multiple competing variants

## What To Avoid

Avoid these failure modes from the backend prompt history:

- mixing JSON and XML in the same payload incorrectly
- wrapping XML inside Markdown when the caller expects raw XML
- returning explanatory prose when strict payloads are required
- generating a diagram before the request is understandable
- producing dense, tangled layouts with many crossed edges

## File Creation Pattern

When the user wants a diagram, default to this file workflow:

1. Choose a clear output filename ending in `.drawio`.
2. Generate the XML.
3. Save it as a local `.drawio` file.
4. Run `python3 scripts/validate_drawio_xml.py <path>`.
5. If validation passes, report the file path.

Only fall back to `.xml` when the user explicitly asks for XML instead of a draw.io file.
