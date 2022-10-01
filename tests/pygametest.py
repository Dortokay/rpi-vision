import pygame
import os
import time
from rpi_vision.agent.capture import PiCameraStream
import numpy as np

capture_manager = PiCameraStream(resolution=(320, 320), preview=False)

pygame.init()
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
pygame.mouse.set_visible(False)
screen.fill((255,0,0))
pygame.display.update()
font = pygame.font.Font(None, 48)
print(screen.get_size())
capture_manager.start()

while not capture_manager.stopped:
    if capture_manager.frame is None:
        continue
    frame = capture_manager.frame
    t = time.monotonic()
    # swap red & blue channels
    npframe = np.ascontiguousarray(np.flip(np.array(frame), 2))
    # make it an image
    img = pygame.image.frombuffer(npframe, capture_manager.camera.resolution, 'RGB')
    # draw it!
    screen.blit(img, (0, 0))
    # add some text
    temptext = ""
    try:
        temp = int(open("/sys/class/thermal/thermal_zone0/temp").read()) / 1000
        temptext = " %0.1f\N{DEGREE SIGN}C" % temp
    except OSError:
        pass
    text_surface = font.render("Hi!"+temptext, True, (255, 255, 255))
    text_position = (screen.get_width()//2, screen.get_height()-24)
    rect = text_surface.get_rect(center=text_position)
    screen.blit(text_surface, rect)
    pygame.display.update()


