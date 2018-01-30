# -*- coding: utf-8 -*-
#!/usr/env python3

# Copyright (C) 2017 Gaby Launay

# Author: Gaby Launay  <gaby.launay@tutanota.com>

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""  """

__author__ = "Gaby Launay"
__copyright__ = "Gaby Launay 2017"
__credits__ = ""
__license__ = "GPL3"
__version__ = ""
__email__ = "gaby.launay@tutanota.com"
__status__ = "Development"


# from PyQt5 import QtCore
# from PyQt5 import QtGui
from PyQt4 import QtCore
from PyQt4 import QtGui
import cv2
import numpy as np


class IdsQtView(QtGui.QWidget):

    update_signal = QtCore.pyqtSignal(QtGui.QImage, name="update_signal")

    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.__image = None
        self.image = None
        self.graphics_view = QtGui.QGraphicsView(self)
        self.v_layout = QtGui.QVBoxLayout(self)
        self.h_layout = QtGui.QHBoxLayout()
        self.scene = QtGui.QGraphicsScene()
        self.graphics_view.setScene(self.scene)
        self.v_layout.addWidget(self.graphics_view)
        self.scene.drawBackground = self.draw_background
        self.scene.setSceneRect(self.scene.itemsBoundingRect())
        self.update_signal.connect(self.update_image)
        self.processors = []
        self.resize(640, 512)
        self.v_layout.addLayout(self.h_layout)
        self.setLayout(self.v_layout)

    # def on_update_canny_1_slider(self, value):
    #     pass  # print(value)

    # def on_update_canny_2_slider(self, value):
    #     pass  # print(value)

    def draw_background(self, painter, rect):
        if self.image is not None:
            image = self.image.scaled(rect.width(), rect.height(),
                                      QtCore.Qt.KeepAspectRatio)
            painter.drawImage(rect.x(), rect.y(), image)

    def update_image(self, image):
        self.scene.update()

    def user_callback(self, image_data):
        return image_data

    @property
    def image(self):
        return self.__image

    @image.setter
    def image(self, image):
        if isinstance(image, np.ndarray):
            self.__image = self._np2qtimage(image)
        else:
            self.__image = image

    def handle(self, image_data):
        self.image = self.user_callback(image_data)
        self.update_signal.emit(self.image)

    def _np2qtimage(self, image):
        # print("")
        # print(image.shape)
        # print(image)
        image = cv2.cvtColor(image, cv2.COLOR_BAYER_GR2BGR)
        return QtGui.QImage(image,
                            image.shape[1],
                            image.shape[0],
                            QtGui.QImage.Format_RGB888)

    def shutdown(self):
        self.close()

    def add_processor(self, callback):
        self.processors.append(callback)


class IdsQtApp:
    def __init__(self, args=[]):
        self.qt_app = QtGui.QApplication(args)

    def exec_(self):
        self.qt_app.exec_()

    def exit_connect(self, method):
        self.qt_app.aboutToQuit.connect(method)
