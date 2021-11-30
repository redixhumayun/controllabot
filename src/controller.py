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
    should_exit_loop = False
    while should_exit_loop is False:
      if self.queue.qsize() > 0 and self.queue.get() is None:
        should_exit_loop = True
        
      events = pygame.event.get()

      for event in events:
        if event.type == pygame.JOYAXISMOTION:
          if event.axis == 0 and event.value != 0:
            value = event.value
            turn_dict = { 'value': event.value, 'state': MotorStateEnum.TURN }
            self.main_queue.put(turn_dict)
          elif event.axis == 1 and event.value != 0:
            pass
        if event.type == pygame.JOYBUTTONDOWN:
          # L2 pressed
          if event.button == 6:
            self.main_queue.put(MotorStateEnum.REVERSE)
          # R2 pressed
          if event.button == 7:
            self.main_queue.put(MotorStateEnum.START)
        if (event.type == pygame.JOYBUTTONUP):
          # L2 released
          if event.button == 6:
            self.main_queue.put(MotorStateEnum.STOP)
          # R2 released
          if event.button == 7:
            self.main_queue.put(MotorStateEnum.STOP)

    # clean up
    self.joystick.quit()