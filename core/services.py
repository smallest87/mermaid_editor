# core/services.py
from .entities import DiagramState, Node, Edge
from .interfaces import IDiagramRepository, IExporter


class DiagramService:
    def __init__(self, repository: IDiagramRepository, exporter: IExporter):
        self.state = DiagramState()
        self.repository = repository
        self.exporter = exporter

    def add_node(self, node_id: str, text: str, **kwargs) -> Node:
        # Menggunakan **kwargs agar flexible menerima pos_x, pos_y, dll.
        node = Node(id=node_id, text=text, **kwargs)
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

    def save(self, path: str):
        self.repository.save(self.state, path)

    def get_mermaid_code(self) -> str:
        return self.exporter.export(self.state)
