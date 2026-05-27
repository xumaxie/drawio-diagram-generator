# Draw.io Output Protocol

This reference captures the most useful protocol rules from the backend agent design.

For this skill, the default end product is still a local `.drawio` file. The payloads below are for integrations, chat UIs, or middleware that need a structured intermediate response.

## The Two Result Types

The backend separates responses into two channels:

- `user`: ask the user for missing information
- `drawio`: send final diagram XML to the draw.io panel

Use these exact shapes when a structured response is needed.

### Clarification payload

```json
{"type":"user","content":"请补充具体的节点、关系和布局要求。"}
```

Use this when:

- the request is too vague
- the diagram type is unclear
- important nodes or relationships are missing
- the user refers to external material that has not been inspected yet

The `content` should ask only for the highest-value missing details.

### Final diagram payload

```json
{"type":"drawio","content":"<mxfile>...</mxfile>"}
```

Use this when:

- the request is clear enough
- the XML has already been reviewed
- the caller expects a front-end payload instead of raw XML

## Strictness Rules

These rules came up repeatedly in the backend prompts and should be preserved:

1. Do not confuse JSON and XML.
2. If the mode is raw XML, output XML only.
3. If the mode is wrapped payload, the final outer structure must be JSON.
4. Do not add Markdown fences unless the caller explicitly wants them.
5. Do not prepend explanations or conclusions to strict payloads.

## Existing Diagram Context

The front end may include the current canvas XML as conversational context before the user's request, using a wrapper like this:

````text
[Context: Current Draw.io XML]
```xml
<mxfile>...</mxfile>
```

...user request...
````

When this context is present:

- treat the XML as the current source diagram
- prefer editing or extending it over regenerating from scratch
- preserve valid structure and identifiers where practical
- only replace the whole diagram when the request clearly calls for it or the XML is unusable

## Decision Rule

Use this simple policy:

- If missing information blocks a trustworthy diagram, return `user`.
- If the request is clear and the result is ready to render, return `drawio` or raw XML depending on the task contract.

## Reviewer Mindset

The backend's reviewer stage is worth keeping:

- pass through `user` payloads unchanged
- inspect XML for structural validity
- improve obvious layout issues textually
- only then normalize into final output format
