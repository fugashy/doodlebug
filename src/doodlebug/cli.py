import sys

from icecream import ic
ic.configureOutput(
        prefix="doodlebug | ",
        includeContext=False)
from PyQt5.QtWidgets import QApplication

from .view import GUI


def main():
    app = QApplication(sys.argv)
    window = GUI()
    window.show()
    sys.exit(app.exec_())
