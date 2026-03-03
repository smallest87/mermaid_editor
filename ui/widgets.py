from PyQt6.QtWidgets import (
    QGraphicsRectItem,
    QGraphicsTextItem,
    QGraphicsItem,
    QGraphicsLineItem,
)
from PyQt6.QtGui import QPen, QBrush, QColor
from PyQt6.QtCore import Qt, QLineF


class TempEdgeItem(QGraphicsLineItem):
    def __init__(self):
        super().__init__()
        self.setPen(QPen(QColor("#3498db"), 2, Qt.PenStyle.DashLine))
        self.setZValue(-1)


class EdgeItem(QGraphicsLineItem):
    def __init__(self, source_item, target_item, label_text=""):
        super().__init__()
        self.source_item = source_item
        self.target_item = target_item
        self.setPen(QPen(QColor("#2c3e50"), 2))
        self.setZValue(-1)
        self.label_item = QGraphicsTextItem(label_text, self)
        self.update_position()

    def update_position(self):
        p1 = self.source_item.sceneBoundingRect().center()
        p2 = self.target_item.sceneBoundingRect().center()
        line = QLineF(p1, p2)
        self.setLine(line)
        mid = line.center()
        t_rect = self.label_item.boundingRect()
        self.label_item.setPos(
            mid.x() - t_rect.width() / 2, mid.y() - t_rect.height() / 2
        )


class NodeItem(QGraphicsRectItem):
    def __init__(self, node_data, service):
        self.node_data = node_data
        self.service = service
        self.edges = []

        if node_data.is_helper:
            super().__init__(0, 0, 10, 10)
            self.setBrush(QBrush(QColor("#3498db")))
            self.setPen(QPen(Qt.PenStyle.NoPen))
        else:
            super().__init__(0, 0, 120, 50)
            self.setBrush(QBrush(QColor("#ffffff")))
            self.setPen(QPen(QColor("#2c3e50"), 2))
            self.text_item = QGraphicsTextItem(node_data.text, self)

        self.setPos(node_data.pos_x, node_data.pos_y)
        self.setFlags(
            QGraphicsItem.GraphicsItemFlag.ItemIsMovable
            | QGraphicsItem.GraphicsItemFlag.ItemIsSelectable
            | QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges
            | QGraphicsItem.GraphicsItemFlag.ItemIsFocusable
        )

    def add_edge(self, edge):
        self.edges.append(edge)

    def mousePressEvent(self, event):
        self.setFocus()
        super().mousePressEvent(event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Delete:
            self.service.remove_node(self.node_data.id)
            for edge in self.edges[:]:
                if edge.scene():
                    edge.scene().removeItem(edge)
            self.scene().removeItem(self)
        super().keyPressEvent(event)

    def itemChange(self, change, value):
        if change == QGraphicsItem.GraphicsItemChange.ItemPositionChange:
            self.node_data.pos_x, self.node_data.pos_y = value.x(), value.y()
            for edge in self.edges:
                edge.update_position()
        return super().itemChange(change, value)
