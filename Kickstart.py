#!/usr/bin/env python3

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
# from IconWidget import *
from DragWidget import *
import sys


class Window(QWidget):

    child_windows = []

    def __init__(self, path, parent=None):
        super(Window, self).__init__()
        self.setWindowTitle(path)
        self.pattern = "images/pattern.png"
        self.path = path
        self.widget = QWidget()
        self.palette = QPalette()
        self.palette.setBrush(QPalette.Background,
                              QBrush(QPixmap(self.pattern)))
        self.widget.setPalette(self.palette)
        layout = QVBoxLayout(self)
        # layout.addWidget(DragWidget(path))
        self._drag_widget = DragWidget(path)
        self._drag_widget.new_window.connect(self.on_make_new_window)
        self._drag_widget.query.connect(self.on_query)
        layout.addWidget(self._drag_widget)
        self.widget.setLayout(layout)
        scroll = QScrollArea()
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.widget)
        self.setStyleSheet("""
            QScrollBar:vertical { border:none; width:6px }
            QScrollBar::handle:vertical { background: lightgray; }
            QScrollBar::add-line:vertical { background: none; }
            QScrollBar::sub-line:vertical { background: none; }
            QScrollBar:horizontal { border:none; height:6px }
            QScrollBar::handle:horizontal { background: lightgray; }
            QScrollBar::add-line:horizontal { background: none; }
            QScrollBar::sub-line:horizontal { background: none; }
            """)
        vlayout = QVBoxLayout(self)
        vlayout.setContentsMargins(0, 0, 0, 0)
        vlayout.setSpacing(0)
        vlayout.addWidget(scroll)
        self.setLayout(vlayout)
        self.show()

    def on_make_new_window(self, path):
        Window.child_windows.append(Window(path))

    def closeEvent(self, event):
        for item in Window.child_windows:
            if item.windowTitle() == self.windowTitle():
                Window.child_windows.remove(item)
                item.deleteLater()

    def on_query(self):
        # get info when doubleclicking on nothing in a window
        print("got query=", self.windowTitle(),
              "obj=", self, "type=", type(self),
              "len CW=", len(Window.child_windows))
        
        for item in Window.child_windows:
            print("loop child_window=", type(item), "title=", item.windowTitle())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window('./') 
    sys.exit(app.exec_())
