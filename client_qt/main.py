# Main python entry

import sys
from pathlib import Path
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from backend import Backend


class main:
    def __init__(self):
        app = QGuiApplication(sys.argv)
        engine = QQmlApplicationEngine()

        import_path = Path(__file__).parent / "."
        engine.addImportPath(str(import_path.resolve()))
        # Create the backend object
        self.backend = Backend()

        # 1. Provide the backend to QML
        engine.rootContext().setContextProperty("backend", self.backend)


        # 2. Load your main QML file (usually App.qml or Main.qml)
        qml_file = Path(__file__).parent / "Login.qml"
        engine.load(str(qml_file))

        if not engine.rootObjects():
            sys.exit(-1)
        sys.exit(app.exec())

    def changeToMainWindow(self):
        qml_file = Path(__file__).parent / "MainWindow.qml"
        engine.load(str(qml_file))

if __name__ == "__main__":
    window = main()

