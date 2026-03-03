# core/interfaces.py
from abc import ABC, abstractmethod
from .entities import DiagramState


class IDiagramRepository(ABC):
    """Kontrak untuk penyimpanan data."""

    @abstractmethod
    def save(self, state: DiagramState, path: str):
        pass

    @abstractmethod
    def load(self, path: str) -> DiagramState:
        pass


class IExporter(ABC):
    """Kontrak untuk generator output (Mermaid, PNG, dll)."""

    @abstractmethod
    def export(self, state: DiagramState) -> str:
        pass
