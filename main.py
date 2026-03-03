import sys
from PyQt6.QtWidgets import QApplication
from core.services import DiagramService
from ui.main_window import DiagramEditor


def main():
    app = QApplication(sys.argv)
    service = DiagramService()

    # Pre-populate data (opsional)
    service.add_node("A", "START", pos_x=50, pos_y=50)
    service.add_node("B", "END", pos_x=300, pos_y=50)

    window = DiagramEditor(service)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
