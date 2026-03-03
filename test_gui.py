import sys
from PyQt6.QtWidgets import (
    QApplication,
    QGraphicsScene,
    QGraphicsView,
    QMainWindow,
    QToolBar,
    QInputDialog,
)
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt, QLineF
from core.engine import MermaidEngine
from core.gui import NodeItem, EdgeItem, TempEdgeItem


class CustomScene(QGraphicsScene):
    """Scene kustom untuk menangani penarikan garis antar node."""

    def __init__(self, engine, parent=None):
        super().__init__(parent)
        self.engine = engine
        self.mode = "SELECT"
        self.temp_edge = None
        self.source_node = None

    def mousePressEvent(self, event):
        item = self.itemAt(event.scenePos(), self.parent().view.transform())
        if self.mode == "CONNECT" and isinstance(item, NodeItem):
            self.source_node = item
            self.temp_edge = TempEdgeItem()
            self.addItem(self.temp_edge)
            pos = item.sceneBoundingRect().center()
            self.temp_edge.setLine(QLineF(pos, event.scenePos()))
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.mode == "CONNECT" and self.temp_edge:
            line = self.temp_edge.line()
            line.setP2(event.scenePos())
            self.temp_edge.setLine(line)
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.temp_edge:
            item = self.itemAt(event.scenePos(), self.parent().view.transform())
            if isinstance(item, NodeItem) and item != self.source_node:
                # Dialog Input Label
                label, ok = QInputDialog.getText(
                    self.parent(), "Edge Label", "Keterangan Garis:"
                )
                label_text = label if ok else ""

                # Simpan ke Engine & Visual
                self.engine.connect_with_routing(
                    self.source_node.node_data.id, item.node_data.id, label=label_text
                )
                new_edge = EdgeItem(self.source_node, item, label_text)
                self.addItem(new_edge)
                self.source_node.add_edge(new_edge)
                item.add_edge(new_edge)

            self.removeItem(self.temp_edge)
            self.temp_edge = None
            self.source_node = None
        super().mouseReleaseEvent(event)


class DiagramEditor(QMainWindow):
    def __init__(self, engine):
        super().__init__()
        self.engine = engine
        self.setWindowTitle("Python Mermaid Editor - Stage 7")
        self.resize(1100, 750)

        self.scene = CustomScene(self.engine, self)
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(self.view.renderHints().Antialiasing)  # Haluskan garis
        self.setCentralWidget(self.view)

        self.node_map = {}
        self.setup_toolbar()
        self.load_diagram()

    def setup_toolbar(self):
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        # Mode Toggles
        select_act = QAction("🖱️ Select", self)
        select_act.triggered.connect(lambda: self.set_mode("SELECT"))
        toolbar.addAction(select_act)

        connect_act = QAction("🔗 Connect", self)
        connect_act.triggered.connect(lambda: self.set_mode("CONNECT"))
        toolbar.addAction(connect_act)

        toolbar.addSeparator()

        # Add Node
        add_node_act = QAction("➕ Add Node", self)
        add_node_act.triggered.connect(self.add_new_node_dialog)
        toolbar.addAction(add_node_act)

    def add_new_node_dialog(self):
        text, ok = QInputDialog.getText(self, "New Node", "Enter label:")
        if ok and text:
            node_id = f"N_{len(self.engine.state.nodes) + 1}"
            self.engine.add_node(node_id, text)
            item = NodeItem(self.engine.state.nodes[-1], self.engine)
            self.scene.addItem(item)
            self.node_map[node_id] = item

    def set_mode(self, mode):
        self.scene.mode = mode
        self.statusBar().showMessage(f"Mode Aktif: {mode}")

    def load_diagram(self):
        self.node_map.clear()
        for node in self.engine.state.nodes:
            item = NodeItem(node, self.engine)
            self.scene.addItem(item)
            self.node_map[node.id] = item

        for edge in self.engine.state.edges:
            src = self.node_map.get(edge.source)
            tgt = self.node_map.get(edge.target)
            if src and tgt:
                e_item = EdgeItem(src, tgt, edge.label or "")
                self.scene.addItem(e_item)
                src.add_edge(e_item)
                tgt.add_edge(e_item)

    def closeEvent(self, event):
        self.engine.save_state("final_output.json")
        print("\n--- KODE MERMAID TERBARU ---")
        print(self.engine.get_mermaid_string())
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    engine = MermaidEngine()

    # Data dummy awal
    engine.add_node("A", "START", shape="circle")
    engine.add_node("B", "END", shape="rect")
    engine.state.nodes[0].pos_x, engine.state.nodes[0].pos_y = 100, 100
    engine.state.nodes[1].pos_x, engine.state.nodes[1].pos_y = 500, 100

    editor = DiagramEditor(engine)
    editor.show()
    sys.exit(app.exec())
