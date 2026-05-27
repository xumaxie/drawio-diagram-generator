# Draw.io XML Template And Layout Rules

## Safe Minimal Skeleton

Use this as a safe baseline when you need to create a new file from scratch.

```xml
<mxfile host="app.diagrams.net">
  <diagram name="Page-1">
    <mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1600" pageHeight="1200" math="0" shadow="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

## Tiny Working Example

Use this when you need a concrete, low-risk starting point with two nodes and one edge.

```xml
<mxfile host="app.diagrams.net">
  <diagram name="Page-1">
    <mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1600" pageHeight="1200" math="0" shadow="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <mxCell id="actor-1" value="User" style="rounded=1;whiteSpace=wrap;html=1;" vertex="1" parent="1">
          <mxGeometry x="120" y="120" width="120" height="60" as="geometry"/>
        </mxCell>
        <mxCell id="process-1" value="Submit Request" style="rounded=0;whiteSpace=wrap;html=1;" vertex="1" parent="1">
          <mxGeometry x="340" y="120" width="160" height="60" as="geometry"/>
        </mxCell>
        <mxCell id="edge-1" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" parent="1" source="actor-1" target="process-1">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

## Practical Shape Heuristics

### Flowcharts

- process: rectangle
- decision: diamond
- start or end: rounded rectangle or ellipse
- data store: cylinder when useful

### Architecture diagrams

- actors or users: simple labeled boxes
- services: rounded rectangles
- databases: cylinders
- external systems: distinct border or grouping container
- network or trust boundaries: containers or swimlanes

### Sequence diagrams

- participants aligned horizontally
- messages ordered vertically
- keep labels short

## Layout Heuristics

These are the most reusable quality rules from the backend prompt:

1. Pick one primary direction and stick to it.
2. Group related nodes closely.
3. Keep enough spacing so labels remain readable.
4. Prefer orthogonal routing when it reduces crossings.
5. Avoid long diagonal edges unless necessary.
6. Put decisions on the main path, not off in a corner.
7. Do not over-model minor details if they hurt readability.

## Update Strategy

When editing existing XML:

- preserve valid root structure
- reuse cells when possible
- add new nodes in the same coordinate system
- adjust geometry to reduce overlap before adding more edges

## ID Convention

Simple IDs help with revisions:

- nodes: `actor-1`, `service-2`, `db-1`, `decision-1`
- edges: `edge-1`, `edge-2`
- groups: `lane-1`, `boundary-1`

## Final Sanity Check

Before returning XML, confirm:

- every opened tag closes
- every cell parent exists
- the diagram has root cells `0` and `1`
- there is a usable `diagram` and `mxGraphModel` wrapper unless the caller only wants a raw model fragment
