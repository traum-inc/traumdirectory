#!/usr/bin/env python
import sys

if getattr(sys, 'frozen', False):
    # if frozen, cd to the bundle dir
    bundle_dir = sys._MEIPASS
    os.chdir(bundle_dir)

from PyQt5.QtWidgets import QApplication
from mainwindow import MainWindow
from utils import setup_logging
from template import TemplateManager

import logging
log = logging.getLogger('app')

if __name__ == '__main__':
    setup_logging(color=True)
    app = QApplication(sys.argv)

    template_manager = TemplateManager('templates')
    templates = list(template_manager.templates.values())

    # create my widgets
    main = MainWindow(templates)
    main.show()

    # start the app
    rc = app.exec_()
    sys.exit(rc)
