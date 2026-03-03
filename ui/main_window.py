from PyQt6.QtWidgets import QMainWindow, QGraphicsView, QToolBar, QInputDialog
from PyQt6.QtGui import QAction
from .scene import DiagramScene
from .widgets import NodeItem, EdgeItem
from infrastructure.persistence import JSONRepository
from infrastructure.converters import MermaidConverter


class DiagramEditor(QMainWindow):
    def __init__(self, service):
        super().__init__()
        self.service = service
        self.setWindowTitle("Professional Mermaid Editor")
        self.resize(1000, 700)

        self.scene = DiagramScene(service, self)
        self.view = QGraphicsView(self.scene)
        self.setCentralWidget(self.view)
        self.node_map = {}

        self._setup_toolbar()
        self._load_initial_view()

    def _setup_toolbar(self):
        tb = self.addToolBar("Main")

        sel_act = QAction("🖱️ Select", self)
        sel_act.triggered.connect(lambda: self._set_mode("SELECT"))
        tb.addAction(sel_act)

        con_act = QAction("🔗 Connect", self)
        con_act.triggered.connect(lambda: self._set_mode("CONNECT"))
        tb.addAction(con_act)

        add_act = QAction("➕ Add", self)
        add_act.triggered.connect(self._add_node_dialog)
        tb.addAction(add_act)

    def _set_mode(self, mode):
        self.scene.mode = mode
        self.statusBar().showMessage(f"Mode: {mode}")

    def _add_node_dialog(self):
        txt, ok = QInputDialog.getText(self, "New", "Label:")
        if ok and txt:
            node = self.service.add_node(f"N{len(self.service.state.nodes)}", txt)
            item = NodeItem(node, self.service)
            self.scene.addItem(item)
            self.node_map[node.id] = item

    def _load_initial_view(self):
        for n in self.service.state.nodes:
            item = NodeItem(n, self.service)
            self.scene.addItem(item)
            self.node_map[n.id] = item
        # Logic untuk edges bisa ditambahkan di sini jika load dari file

    def closeEvent(self, event):
        JSONRepository.save(self.service.state, "output.json")
        print(MermaidConverter.to_mermaid(self.service.state))
        event.accept()
