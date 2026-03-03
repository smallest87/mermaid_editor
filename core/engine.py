import json
from .models import DiagramState, Node, Edge


class MermaidEngine:
    """
    Mesin utama untuk mengelola logika data diagram (State)
    dan menerjemahkannya menjadi format JSON atau kode Mermaid.
    """

    def __init__(self):
        self.state = DiagramState()

    def add_node(self, node_id: str, text: str, shape: str = "rect"):
        """Menambahkan node fungsional ke dalam diagram."""
        self.state.nodes.append(Node(id=node_id, text=text, shape_type=shape))

    def connect_with_routing(
        self, source_id: str, target_id: str, waypoints: int = 0, label: str = None
    ):
        """
        Menghubungkan dua node. Jika waypoints > 0, akan menyuntikkan
        node pembantu (helper) sebagai titik belok transparan.
        """
        current_source = source_id
        for i in range(waypoints):
            h_id = f"WP_{source_id}_{target_id}_{i}"
            # Waypoint ditandai sebagai is_helper=True agar visual di kanvas berbeda
            self.state.nodes.append(Node(id=h_id, text=" ", is_helper=True))
            # Koneksi antar waypoint tidak menggunakan label
            self.state.edges.append(Edge(source=current_source, target=h_id))
            current_source = h_id

        # Koneksi terakhir ke target utama membawa label (jika ada)
        self.state.edges.append(
            Edge(source=current_source, target=target_id, label=label)
        )

    def generate_directive(self) -> str:
        """
        Menghasilkan konfigurasi gaya Mermaid (Directive).
        Sudah diperbaiki formatnya agar tidak menyebabkan Syntax Error di Live Editor.
        """
        config_data = {
            "theme": self.state.spec.theme,
            "themeVariables": {
                "fontFamily": self.state.spec.fontFamily,
                "fontSize": f"{self.state.spec.fontSize}px",
                "nodePadding": self.state.spec.nodePadding,
                "lineColor": self.state.spec.lineColor,
                "mainBkg": self.state.spec.primaryColor,
                "edgeLabelBackground": "#ffffff",  # Membuat label garis lebih bersih
                "tertiaryColor": "#f4f4f4",
            },
            "flowchart": {"curve": self.state.spec.curve},
        }

        # Format yang benar: %%{init: {json_content}}%%
        # Tanpa tanda kutip pada kata 'init'
        return f"%%{{init: {json.dumps(config_data)}}}%%"

    def get_mermaid_string(self) -> str:
        """Menyusun keseluruhan kode Mermaid dari directive, node, hingga edges."""
        lines = [self.generate_directive()]
        lines.append(f"graph {self.state.direction}")

        # Pemetaan tipe bentuk ke sintaks visual Mermaid
        shape_map = {
            "rect": "[{}]",
            "circle": "(({}))",
            "diamond": "{{{{{{{}}}}}}}",  # Diamond menggunakan bracket triple kurawal
        }

        # 1. Tulis Definisi Node
        for n in self.state.nodes:
            if n.is_helper:
                # Helper node (belokan) menggunakan bentuk minimalis
                lines.append(f"    {n.id}((( )))")
                lines.append(f"    class {n.id} helperNode")
            else:
                s_fmt = shape_map.get(n.shape_type, "[{}]").format(n.text)
                lines.append(f"    {n.id}{s_fmt}")

        # 2. Tulis Definisi Edge (Garis)
        for e in self.state.edges:
            if e.label:
                edge_str = f"-- {e.label} -->"
            else:
                edge_str = "-->"
            lines.append(f"    {e.source} {edge_str} {e.target}")

        # 3. Tambahkan ClassDef untuk menyembunyikan Helper Node di hasil akhir
        lines.append("    classDef helperNode fill:none,stroke:none,color:none")

        return "\n".join(lines)

    def save_state(self, path: str):
        """Menyimpan state diagram saat ini ke file JSON."""
        with open(path, "w") as f:
            f.write(self.state.model_dump_json(indent=4))

    def remove_node(self, node_id: str):
        # Hapus Node dari list
        self.state.nodes = [n for n in self.state.nodes if n.id != node_id]
        # Hapus semua Edge yang terhubung dengan node tersebut
        self.state.edges = [
            e for e in self.state.edges if e.source != node_id and e.target != node_id
        ]

    def remove_edge(self, source_id: str, target_id: str):
        """Menghapus hubungan spesifik antara dua node."""
        self.state.edges = [
            e
            for e in self.state.edges
            if not (e.source == source_id and e.target == target_id)
        ]
