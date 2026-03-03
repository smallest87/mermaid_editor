import json


class MermaidConverter:
    @staticmethod
    def to_mermaid(state) -> str:
        config = {
            "theme": state.spec.theme,
            "themeVariables": {
                "fontFamily": state.spec.fontFamily,
                "edgeLabelBackground": "#ffffff",
            },
            "flowchart": {"curve": state.spec.curve},
        }
        directive = f"%%{{init: {json.dumps(config)}}}%%"
        lines = [directive, f"graph {state.direction}"]

        for n in state.nodes:
            if n.is_helper:
                lines.append(f"    {n.id}((( )))")
                lines.append(f"    class {n.id} helperNode")
            else:
                lines.append(f"    {n.id}[{n.text}]")

        for e in state.edges:
            edge_str = f"-- {e.label} -->" if e.label else "-->"
            lines.append(f"    {e.source} {edge_str} {e.target}")

        lines.append("    classDef helperNode fill:none,stroke:none,color:none")
        return "\n".join(lines)
