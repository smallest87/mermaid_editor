# core/services.py
from .entities import DiagramState, Node, Edge


class DiagramService:
    def __init__(self, state: DiagramState = None):
        self.state = state or DiagramState()

    def add_node(
        self,
        node_id: str,
        text: str,
        shape: str = "rect",
        is_helper: bool = False,
        pos_x: float = 0.0,
        pos_y: float = 0.0,
    ) -> Node:
        """
        PERBAIKAN: Menambahkan parameter pos_x dan pos_y agar
        bisa menerima koordinat awal dari main.py atau UI.
        """
        node = Node(
            id=node_id,
            text=text,
            shape_type=shape,
            is_helper=is_helper,
            pos_x=pos_x,
            pos_y=pos_y,
        )
        self.state.nodes.append(node)
        return node

    def remove_node(self, node_id: str):
        self.state.nodes = [n for n in self.state.nodes if n.id != node_id]
        self.state.edges = [
            e for e in self.state.edges if e.source != node_id and e.target != node_id
        ]

    def add_connection(self, source_id: str, target_id: str, label: str = None) -> Edge:
        edge = Edge(source=source_id, target=target_id, label=label)
        self.state.edges.append(edge)
        return edge
