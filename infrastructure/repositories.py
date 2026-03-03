# infrastructure/repositories.py
from core.interfaces import IDiagramRepository
from core.entities import DiagramState


class JSONDiagramRepository(IDiagramRepository):
    """Implementasi IDiagramRepository menggunakan format file JSON."""

    def save(self, state: DiagramState, path: str):
        with open(path, "w") as f:
            f.write(state.model_dump_json(indent=4))

    def load(self, path: str) -> DiagramState:
        with open(path, "r") as f:
            return DiagramState.model_validate_json(f.read())
