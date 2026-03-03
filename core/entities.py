from pydantic import BaseModel, Field
from typing import List, Optional


class VisualSpec(BaseModel):
    theme: str = "base"
    fontFamily: str = "Arial"
    fontSize: int = 14
    nodePadding: int = 15
    lineColor: str = "#333333"
    primaryColor: str = "#ffffff"
    curve: str = "basis"


class Node(BaseModel):
    id: str
    text: str
    shape_type: str = "rect"
    is_helper: bool = False
    pos_x: float = 0.0
    pos_y: float = 0.0


class Edge(BaseModel):
    source: str
    target: str
    label: Optional[str] = None


class DiagramState(BaseModel):
    direction: str = "TD"
    nodes: List[Node] = []
    edges: List[Edge] = []
    spec: VisualSpec = Field(default_factory=VisualSpec)
