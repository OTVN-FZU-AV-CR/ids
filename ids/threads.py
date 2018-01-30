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


class UselessThread(GatherThread):
    def __init__(self, cam, views=None, copy=True):
        """
        Thread used for debugging only.
        """
        super().__init__(cam=cam, copy=copy)
        self.views = views

    def process(self, image_data):
        print(self.cam.get_exposure())
        import numpy as np
        new_exp = np.random.rand()*20
        self.cam.set_exposure(new_exp)
        print(f"nex exposure {new_exp}")
        print(self.cam.get_exposure())


class SaveThread(GatherThread):
    def __init__(self, cam, path, copy=True):
        """
        Thread used for saving images.
        """
        super().__init__(cam=cam, copy=copy)
        self.path = path

    def process(self, image_data):
        cv2.imwrite(self.path, image_data.as_1d_image())
        self.stop()


class RecordThread(GatherThread):
    def __init__(self, cam, path, nmb_frame=10, copy=True):
        """
        Thread used to record videos.
        """
        super().__init__(cam=cam, copy=copy)
        self.nmb_frame = nmb_frame
        self.ind_frame = 0
        self.path = path
        aoi = self.cam.get_aoi()
        # TODO: add real fps
        # Create videowriter instance
        fourcc = cv2.VideoWriter_fourcc("M", "J", "P", "G")
        self.vw = cv2.VideoWriter(self.path,
                                  # cv2.CAP_FFMPEG,
                                  fourcc=fourcc,
                                  fps=10,
                                  frameSize=(aoi.width, aoi.height),
                                  isColor=0)

    def process(self, imdata):
        self.vw.write(imdata)
        self.ind_frame += 1
        # stop
        if self.ind_frame >= self.nmb_frame:
            self.stop()

    def stop(self):
        self.vw.release()
        super().stop()
