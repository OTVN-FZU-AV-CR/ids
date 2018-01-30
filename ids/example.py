import ids
from pypyueye import PyuEyeQtApp, PyuEyeQtView
from PyQt4 import QtGui
import cv2
import numpy as np
import matplotlib.pyplot as plt
import ids

with ids.Camera(nummem=100, color=ids.COLOR_MONO_8) as cam:
    #==========================================================================
    # Settings
    #==========================================================================
    cam.color_mode = ids.COLOR_MONO_8    # Get images in RGB format
    # cam.exposure = 5                            # Set initial exposure to 5ms
    cam.auto_exposure = True
    cam.auto_exposure_brightness = True
    # cam.auto_speed = True
    # cam.auto_white_balance = False
    # cam.continuous_capture = True               # Start image capture
    cam.gain = 0
    cam.pixelclock = 10

    # #==============================================================================
    # # TMP
    # #==============================================================================
    # cam.continuous_capture = True
    # img, metadata = cam.next()
    # cd = CircleDetector(1)
    # cd.process(img)

    #======================================================================
    # Live video with circle detection
    #======================================================================
    # we need a QApplication, that runs our QT Gui Framework
    app = PyuEyeQtApp()
    # a basic qt window
    view = PyuEyeQtView()
    # Create a circle detector and associate it to the view
    cd = ids.CircleDetector(nmb_circ=1)
    view.user_callback = cd.process
    # Show the view
    view.show()
    # a thread that waits for new images and processes all connected views
    thread = ids.LiveThread(cam, view)
    thread.start()
    app.exit_connect(thread.stop)
    # Run and wait for the app to quit
    app.exec_()
    cam.close()
