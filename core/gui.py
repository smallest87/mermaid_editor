from PyQt6.QtWidgets import (
    QGraphicsRectItem,
    QGraphicsTextItem,
    QGraphicsItem,
    QGraphicsLineItem,
)
from PyQt6.QtGui import QPen, QBrush, QColor
from PyQt6.QtCore import Qt, QLineF


class TempEdgeItem(QGraphicsLineItem):
    """Garis pratinjau (biru putus-putus) saat menarik koneksi."""

    def __init__(self):
        super().__init__()
        self.setPen(QPen(QColor("#3498db"), 2, Qt.PenStyle.DashLine))
        self.setZValue(-1)


class EdgeItem(QGraphicsLineItem):
    """Garis permanen dengan label teks yang selalu di tengah."""

    def __init__(self, source_item, target_item, label_text=""):
        super().__init__()
        self.source_item = source_item
        self.target_item = target_item
        self.setPen(QPen(QColor("#2c3e50"), 2))
        self.setZValue(-1)

        # Inisialisasi Label
        self.label_item = QGraphicsTextItem(label_text, self)
        self.label_item.setDefaultTextColor(QColor("#2c3e50"))

        self.update_position()

    def update_position(self):
        """Update lintasan garis dan posisi label di titik tengah."""
        p1 = self.source_item.sceneBoundingRect().center()
        p2 = self.target_item.sceneBoundingRect().center()
        line = QLineF(p1, p2)
        self.setLine(line)

        # Hitung titik tengah untuk label
        mid_point = line.center()
        t_rect = self.label_item.boundingRect()
        self.label_item.setPos(
            mid_point.x() - t_rect.width() / 2, mid_point.y() - t_rect.height() / 2
        )


class NodeItem(QGraphicsRectItem):
    """Representasi visual Node/Waypoint dengan fitur Drag & Delete."""

    def __init__(self, node_data, engine):
        self.node_data = node_data
        self.engine = engine
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
            self.update_text_position()

        self.setPos(node_data.pos_x, node_data.pos_y)
        self.setFlags(
            QGraphicsItem.GraphicsItemFlag.ItemIsMovable
            | QGraphicsItem.GraphicsItemFlag.ItemIsSelectable
            | QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges
            | QGraphicsItem.GraphicsItemFlag.ItemIsFocusable
        )

    def add_edge(self, edge):
        self.edges.append(edge)

    def update_text_position(self):
        if not self.node_data.is_helper:
            rect = self.rect()
            t_rect = self.text_item.boundingRect()
            self.text_item.setPos(
                (rect.width() - t_rect.width()) / 2,
                (rect.height() - t_rect.height()) / 2,
            )

    def mousePressEvent(self, event):
        self.setFocus()
        super().mousePressEvent(event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Delete:
            self.engine.remove_node(self.node_data.id)
            scene = self.scene()
            for edge in self.edges[:]:
                if edge in scene.items():
                    scene.removeItem(edge)
            scene.removeItem(self)
        else:
            super().keyPressEvent(event)

    def itemChange(self, change, value):
        if change == QGraphicsItem.GraphicsItemChange.ItemPositionChange:
            self.node_data.pos_x = value.x()
            self.node_data.pos_y = value.y()
            for edge in self.edges:
                edge.update_position()
        return super().itemChange(change, value)
