import os
import re
import logging

from PyQt5.QtWidgets import (
        QMainWindow, QAction, QFileDialog, QComboBox, QLabel, QLineEdit,
        QWidget, QSizePolicy, QFormLayout, QVBoxLayout, QMessageBox,
        qApp,
        )
from PyQt5.QtGui import (
        QIcon,
        )
from PyQt5.QtCore import (
        Qt, QSize, QTimer, QPersistentModelIndex,
        )

import config


log = logging.getLogger('app')
app_title = 'Traum Directory'

icon_cache = {}
def get_icon(name):
    if name not in icon_cache:
        filename = f'icons/{name}.png'
        icon_cache[name] = QIcon(filename)
    return icon_cache[name]

re_valid = re.compile(r'^[^<>:"/\|?*]+$')

class MainWindow(QMainWindow):
    def __init__(self, templates):
        QMainWindow.__init__(self)
        self._templates = templates
        self._selected_template = None
        self._template_lines = {}

        self._init_ui()
        self._init_template_ui()

    def _status(self, message):
        self.statusBar().showMessage(message)

    def _init_ui(self):
        self.setMinimumSize(QSize(640, 480))
        self.setWindowTitle(app_title)
        qApp.setApplicationDisplayName(app_title)
        #self.setAcceptDrops(True)
        self._status('Ready')

        def make_action(text, icon, tip=None, key=None, handler=None):
            action = QAction(get_icon(icon), text, self)
            if key:
                action.setShortcut(key)
            if tip:
                action.setStatusTip(tip)
            if handler:
                action.triggered.connect(handler)
            return action

        action_encode = make_action(
            text='&Generate',
            icon='gears',
            tip='Genrate structure',
            key='Ctrl+G',
            handler=self._generate)

        action_quit = make_action(
            text='&Exit',
            icon='exit',
            tip='Exit application',
            key='Ctrl+Q',
            handler=qApp.quit)

        menubar = self.menuBar()

        menu = menubar.addMenu('&File')
        menu.addAction(action_quit)

        toolbar = self.addToolBar('toolbar')
        for action in [action_encode]:
            toolbar.addAction(action)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        toolbar.addWidget(spacer)

        combo = QComboBox()
        for template in self._templates:
            combo.addItem(template.name, userData=template)
        toolbar.addWidget(QLabel('Template:'))
        toolbar.addWidget(combo)
        combo.activated.connect(self._on_combo_template_activated)

        toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

    def _on_combo_template_activated(self, idx):
        self._select_template_by_idx(idx)

    def _select_template_by_idx(self, idx):
        template = self._templates[idx]
        if self._selected_template is template:
            return
        self._selected_template = template
        self._template_lines = {}
        log.info(f'selected template {template.name}')

        # create ui
        form = QFormLayout()
        for varname in template.varnames:
            line = QLineEdit()
            form.addRow(varname, line)
            self._template_lines[varname] = line

        widget = QWidget()
        widget.setLayout(form)
        self.setCentralWidget(widget)

    def _init_template_ui(self):
        if self._templates:
            self._select_template_by_idx(0)

    def _generate(self):
        env = {}

        for varname, line in self._template_lines.items():
            text = line.text()
            text = text.strip()

            if not text:
                QMessageBox.warning(self, 'Bad value', f'Variable "{varname}" cannot be empty.')
                return

            if not re_valid.match(text):
                QMessageBox.warning(self, 'Bad value', f'Variable "{varname}" contains invalid characters.')
                return

            env[varname] = text

        self._status('Generating structure from template...')
        dirpath = QFileDialog.getExistingDirectory(self, 'Select output directory')
        if not dirpath:
            return

        log.info(f'generate: {dirpath}')

        try:
            template = self._selected_template
            template.exec(dirpath, **env)
            QMessageBox.information(self, 'Success', f'Generated template "{template.name}" in:\n{dirpath}')
        except Exception as ex:
            QMessageBox.critical(self, 'Generation failed', repr(ex))

        self._status('Success')
