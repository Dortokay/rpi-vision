import logging
from picamera2 import Picamera2, Preview
from libcamera import Transform
from threading import Thread

class PiCameraStream(object):
    """
      Continuously capture video frames, and optionally render with an overlay

      Arguments
      resolution - tuple (x, y) size
      framerate - int
      vflip - reflect capture on x-axis
      hflip - reflect capture on y-axis

    """

    def __init__(self, *, resolution=(320, 240), vflip=False, hflip=False, preview=True):
        self.camera = Picamera2()
        # Disable Picamera2 Debugging
        logging.getLogger("picamera2").setLevel(logging.INFO)

        stream_transform = Transform(hflip=int(hflip), vflip=int(vflip))
        stream_config = self.camera.create_video_configuration(
            main={
                "size": resolution,
                "format": "RGB888"
            },
            transform=stream_transform
        )
        self.camera.configure(stream_config)

        self.frame = None
        self.stopped = False
        self._stream = "main"
        if preview:
            print('starting camera preview')
            self.camera.start_preview()

    def render_overlay(self):
        pass

    def start(self):
        """Begin handling frame stream in a separate thread"""
        Thread(target=self.flush, args=()).start()
        self.camera.start()
        return self

    def flush(self):
        # looping until self.stopped flag is flipped
        # for now, grab the first frame in buffer, then empty buffer
        while True:
            self.frame = self.camera.capture_array(self._stream)

            if self.stopped:
                self.camera.close()
                return

    def read(self):
        #stride = self.camera.stream_configuration(self._stream)["stride"]
        return self.frame[0:224, 48:272, :]  # crop the 240 x 320 frame

    def stop(self):
        self.stopped = True
        self.camera.stop()

    @property
    def resolution(self):
        return self.camera.stream_configuration(self._stream)["size"]
