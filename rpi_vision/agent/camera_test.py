import time
from picamera2 import Picamera2, Preview
import os

camera = Picamera2()
try:
    camera.start_preview()
    preview_config = camera.create_preview_configuration(
        main={"size": (320, 240)}
    )
    camera.configure(preview_config)
    camera.start()
    time.sleep(60)
    camera.stop_preview()
finally:
    camera.close()
