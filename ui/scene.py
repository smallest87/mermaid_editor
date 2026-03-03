from PyQt6.QtWidgets import QGraphicsScene, QInputDialog
from PyQt6.QtCore import QLineF
from .widgets import NodeItem, EdgeItem, TempEdgeItem


class DiagramScene(QGraphicsScene):
    def __init__(self, service, parent=None):
        super().__init__(parent)
        self.service = service
        self.mode = "SELECT"
        self.temp_edge = None
        self.source_node = None

    def mousePressEvent(self, event):
        item = self.itemAt(event.scenePos(), self.parent().view.transform())
        if self.mode == "CONNECT" and isinstance(item, NodeItem):
            self.source_node = item
            self.temp_edge = TempEdgeItem()
            self.addItem(self.temp_edge)
            self.temp_edge.setLine(
                QLineF(item.sceneBoundingRect().center(), event.scenePos())
            )
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.temp_edge:
            line = self.temp_edge.line()
            line.setP2(event.scenePos())
            self.temp_edge.setLine(line)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.temp_edge:
            item = self.itemAt(event.scenePos(), self.parent().view.transform())
            if isinstance(item, NodeItem) and item != self.source_node:
                label, ok = QInputDialog.getText(self.parent(), "Label", "Keterangan:")
                txt = label if ok else ""
                self.service.add_connection(
                    self.source_node.node_data.id, item.node_data.id, txt
                )
                edge = EdgeItem(self.source_node, item, txt)
                self.addItem(edge)
                self.source_node.add_edge(edge)
                item.add_edge(edge)
            self.removeItem(self.temp_edge)
            self.temp_edge = self.source_node = None
        super().mouseReleaseEvent(event)
