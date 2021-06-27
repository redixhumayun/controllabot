import pygame
import sys
from multiprocessing import Queue, Process

from controller import Controller
from motor import Motor
from motor_state_enum import MotorStateEnum

if __name__ == "__main__":
  processes:list = []

  controller_queue = Queue()
  motor_queue = Queue()
  main_queue = Queue()

  controller_process = Controller(controller_queue, main_queue)
  processes.append(controller_process)

  motor_process = Motor(motor_queue, main_queue)
  processes.append(motor_process)

  for process in processes:
    process.start()

  try:
    while True:
      main_queue_value = main_queue.get()
      if main_queue_value == MotorStateEnum.START:
        motor_queue.put(MotorStateEnum.START)
      elif main_queue_value == MotorStateEnum.STOP:
        motor_queue.put(MotorStateEnum.STOP)
      elif main_queue_value == MotorStateEnum.REVERSE:
        motor_queue.put(MotorStateEnum.REVERSE)
      else:
        motor_queue.put(main_queue_value)
  except KeyboardInterrupt:
    print("Quitting the main loop")
    controller_queue.put(None)
    motor_queue.put(None)
    for process in processes:
      process.join()