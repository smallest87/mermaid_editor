import sys
import logging
from PyQt6.QtWidgets import QApplication

# Import Domain Layer
from core.services import DiagramService

# Import Infrastructure Layer (Implementasi Konkret)
from infrastructure.repositories import JSONDiagramRepository
from infrastructure.exporters import MermaidExporter

# Import Presentation Layer
from ui.main_window import DiagramEditor


def bootstrap():
    """
    Fungsi Bootstrapper untuk merakit komponen aplikasi.
    Menggunakan Dependency Injection untuk menyuntikkan infrastruktur ke core.
    """
    # 1. Konfigurasi Logging (Opsional namun disarankan di industri)
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    logger = logging.getLogger(__name__)

    # 2. Inisialisasi Aplikasi Qt
    app = QApplication(sys.argv)
    app.setApplicationName("Professional Mermaid Editor")

    try:
        # 3. Komposisi Objek (Dependency Injection)
        # Jika besok ganti DB, cukup ganti JSONDiagramRepository di sini.
        repository = JSONDiagramRepository()
        exporter = MermaidExporter()

        # Suntikkan repository dan exporter ke dalam service
        service = DiagramService(repository=repository, exporter=exporter)

        # 4. Data Awal (Optional/Testing)
        service.add_node("START", "Mulai Kerja", pos_x=100, pos_y=100, shape="circle")
        service.add_node("END", "Selesai", pos_x=500, pos_y=100)

        # 5. Inisialisasi UI dengan Service yang sudah siap
        editor = DiagramEditor(service)
        editor.show()

        logger.info("Aplikasi berhasil diluncurkan.")
        sys.exit(app.exec())

    except Exception as e:
        logger.error(f"Gagal menjalankan aplikasi: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    bootstrap()
