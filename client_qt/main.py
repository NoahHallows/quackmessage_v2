# Main python entry

import sys
from pathlib import Path
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from backend import Backend


class main:
    def __init__(self):
        self.app = QGuiApplication(sys.argv)
        self.engine = QQmlApplicationEngine()

        import_path = Path(__file__).parent / "."
        self.engine.addImportPath(str(import_path.resolve()))
        # Create the backend object
        self.backend = Backend()

        # 1. Provide the backend to QML
        self.engine.rootContext().setContextProperty("backend", self.backend)


        # 2. Load your main QML file (usually App.qml or Main.qml)
        qml_file = Path(__file__).parent / "qml/App.qml"
        self.engine.load(str(qml_file))

        if not self.engine.rootObjects():
            sys.exit(-1)
        sys.exit(self.app.exec())


if __name__ == "__main__":
    window = main()

