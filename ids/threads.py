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

from threading import Thread


class GatherThread(Thread):
    def __init__(self, cam):
        """
        Thread used for gather images.
        """
        super().__init__()
        self.cam = cam
        self.cam.continuous_capture = True
        self.running = True

    def run(self):
        while self.running:
            img, data = self.cam.next()
            self.process(img)

    def process(self, image_data):
        pass

    def stop(self):
        self.cam.continuous_capture = False
        self.running = False


class LiveThread(GatherThread):
    def __init__(self, cam, views=None):
        """
        Thread used for live display.
        """
        super().__init__(cam=cam)
        self.views = views

    def process(self, image_data):
        if self.views:
            if type(self.views) is not list:
                self.views = [self.views]
            for view in self.views:
                view.handle(image_data)
