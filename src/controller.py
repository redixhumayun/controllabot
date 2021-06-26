import pygame
import sys
from multiprocessing import Process

from motor_state_enum import MotorStateEnum

pygame.init()

joystick = pygame.joystick.Joystick(0)
joystick.init()

class Controller(Process):
  def __init__(self, queue, main_queue):
    Process.__init__(self)
    pygame.init()
    self.joystick = pygame.joystick.Joystick(0)
    self.joystick.init()
    self.queue = queue
    self.main_queue = main_queue

  def run(self):
    while True:
      events = pygame.event.get()
      if self.queue.empty() == False and self.queue.get_nowait() == None:
        break
      for event in events:
        if event.type == pygame.JOYAXISMOTION:
          pass
        if event.type == pygame.JOYBUTTONDOWN:
          print(event.dict)
          if event.button == 6:
            self.main_queue.put(MotorStateEnum.REVERSE)
          if event.button == 7:
            self.main_queue.put(MotorStateEnum.START)
        if (event.type == pygame.JOYBUTTONUP):
          if event.button == 6:
            self.main_queue.put(MotorStateEnum.STOP)
          if event.button == 7:
            self.main_queue.put(MotorStateEnum.STOP)
          pass

    # clean up
    self.joystick.quit()

# try:
#   while True:
#     events = pygame.event.get()
#     for event in events:
#       if event.type == pygame.JOYAXISMOTION:
#         print("JOYAXISMOTION")
#         print(event.dict)
#       elif event.type == pygame.JOYBALLMOTION:
#         print("JOYBALLMOTION")
#         print(event.dict)
#       elif event.type == pygame.JOYBUTTONDOWN:
#         print("JOYBUTTONDOWN")
#         print(event.dict, 'pressed')
#       elif event.type == pygame.JOYBUTTONUP:
#         print("JOYBUTTONUP")
#         print(event.dict, 'released')
#       elif event.type == pygame.JOYHATMOTION:
#         print("JOYHATMOTION")
#         print(event.dict, event.joy, event.hat, event.value)
# except KeyboardInterrupt:
#   joystick.quit()
#   sys.exit(0)