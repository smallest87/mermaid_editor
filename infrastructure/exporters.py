# infrastructure/exporters.py
import json
from core.interfaces import IExporter
from core.entities import DiagramState


class MermaidExporter(IExporter):
    """Implementasi IExporter khusus untuk format Mermaid.js."""

    def export(self, state: DiagramState) -> str:
        config = {
            "theme": state.spec.theme,
            "themeVariables": {
                "fontFamily": state.spec.fontFamily,
                "edgeLabelBackground": "#ffffff",
            },
            "flowchart": {"curve": state.spec.curve},
        }

        # Directive untuk styling di Mermaid Live Editor
        directive = f"%%{{init: {json.dumps(config)}}}%%"
        lines = [directive, f"graph {state.direction}"]

        # Render Nodes
        for n in state.nodes:
            if n.is_helper:
                lines.append(f"    {n.id}((( )))")
                lines.append(f"    class {n.id} helperNode")
            else:
                lines.append(f"    {n.id}[{n.text}]")

        # Render Edges
        for e in state.edges:
            edge_str = f"-- {e.label} -->" if e.label else "-->"
            lines.append(f"    {e.source} {edge_str} {e.target}")

        lines.append("    classDef helperNode fill:none,stroke:none,color:none")
        return "\n".join(lines)
