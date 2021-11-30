import RPi.GPIO as GPIO
import sys
from multiprocessing import Process, Queue
from motor_state_enum import MotorStateEnum
import time

class Motor(Process):
  def __init__(self, queue, main_queue):
    Process.__init__(self)

    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)

    PWM_frequency = 1500
    self.duty_cycle_1 = 35
    self.duty_cycle_2 = 38
    self.duty_cycle_3 = 35
    self.duty_cycle_4 = 36.5
    
    # Set up motor 1
    self.in1 = 8
    self.in2 = 7
    self.enA = 12
    GPIO.setup(self.in1, GPIO.OUT)
    GPIO.setup(self.in2, GPIO.OUT)
    GPIO.setup(self.enA, GPIO.OUT)
    self.pA = GPIO.PWM(self.enA, PWM_frequency)
    self.pA.start(self.duty_cycle_1)

    # Set up motor 2
    self.in3 = 6
    self.in4 = 5
    self.enB = 13
    GPIO.setup(self.in3, GPIO.OUT)
    GPIO.setup(self.in4, GPIO.OUT)
    GPIO.setup(self.enB, GPIO.OUT)
    self.pB = GPIO.PWM(self.enB, PWM_frequency)
    self.pB.start(self.duty_cycle_2)

    # Set up motor 3
    self.in5 = 24
    self.in6 = 23
    self.enC = 25
    GPIO.setup(self.in5, GPIO.OUT)
    GPIO.setup(self.in6, GPIO.OUT)
    GPIO.setup(self.enC, GPIO.OUT)
    self.pC = GPIO.PWM(self.enC, PWM_frequency)
    self.pC.start(self.duty_cycle_3)

    # Set up motor 4
    self.in7 = 27
    self.in8 = 17
    self.enD = 22
    GPIO.setup(self.in7, GPIO.OUT)
    GPIO.setup(self.in8, GPIO.OUT)
    GPIO.setup(self.enD, GPIO.OUT)
    self.pD = GPIO.PWM(self.enD, PWM_frequency)
    self.pD.start(self.duty_cycle_4)

    # Set the queue for IPC communication
    self.queue = queue
    self.main_queue = main_queue

  def run(self):
    should_exit_loop = False
    while should_exit_loop is False:
      value = self.queue.get()
      if value == MotorStateEnum.START:
        self.start_motors()
      elif value == MotorStateEnum.STOP:
        self.stop_motors()
      elif value == MotorStateEnum.REVERSE:
        self.reverse_motors()
      elif isinstance(value, dict):
        # Motor needs to turn
        self.turn_motors(value['value'])
      elif value is None:
        should_exit_loop = True

    self.stop_motors()
    GPIO.cleanup()

  def start_motors(self):

    GPIO.output(self.in1, GPIO.HIGH)
    GPIO.output(self.in2, GPIO.LOW)

    GPIO.output(self.in3, GPIO.HIGH)
    GPIO.output(self.in4, GPIO.LOW)

    GPIO.output(self.in5, GPIO.HIGH)
    GPIO.output(self.in6, GPIO.LOW)

    GPIO.output(self.in7, GPIO.HIGH)
    GPIO.output(self.in8, GPIO.LOW)

  def stop_motors(self):
    GPIO.output(self.in1, GPIO.LOW)
    GPIO.output(self.in2, GPIO.LOW)

    GPIO.output(self.in3, GPIO.LOW)
    GPIO.output(self.in4, GPIO.LOW)

    GPIO.output(self.in5, GPIO.LOW)
    GPIO.output(self.in6, GPIO.LOW)

    GPIO.output(self.in7, GPIO.LOW)
    GPIO.output(self.in8, GPIO.LOW)

  def reverse_motors(self):
    GPIO.output(self.in1, GPIO.LOW)
    GPIO.output(self.in2, GPIO.HIGH)

    GPIO.output(self.in3, GPIO.LOW)
    GPIO.output(self.in4, GPIO.HIGH)

    GPIO.output(self.in5, GPIO.LOW)
    GPIO.output(self.in6, GPIO.HIGH)

    GPIO.output(self.in7, GPIO.LOW)
    GPIO.output(self.in8, GPIO.HIGH)
  
  def turn_motors(self, scaling_value):
    try:
      print(scaling_value)
      if scaling_value > 0:
        scaling_output_1 = scaling_value * self.duty_cycle_1
        scaling_output_3 = scaling_value * self.duty_cycle_3
        if scaling_value > 0.2:
          print('Running motors 1 & 3')
          print(scaling_output_1)
          print(scaling_output_3)

          self.pA.ChangeDutyCycle(scaling_output_1)
          GPIO.output(self.in1, GPIO.HIGH)
          GPIO.output(self.in2, GPIO.LOW)

          self.pC.ChangeDutyCycle(scaling_output_3)
          GPIO.output(self.in5, GPIO.HIGH)
          GPIO.output(self.in6, GPIO.LOW)
        elif scaling_value <= 0.2:
          print('Stopping motors 1 & 3')
          print(scaling_output_1)
          print(scaling_output_3)

          self.pA.ChangeDutyCycle(scaling_output_1)
          GPIO.output(self.in1, GPIO.LOW)
          GPIO.output(self.in2, GPIO.LOW)

          self.pC.ChangeDutyCycle(scaling_output_3)
          GPIO.output(self.in5, GPIO.LOW)
          GPIO.output(self.in6, GPIO.LOW)
      elif scaling_value < 0:
        scaling_output_2 = scaling_value * self.duty_cycle_2
        scaling_output_4 = scaling_value * self.duty_cycle_4
        if scaling_value < -0.2:
          print('Running motors 2 & 4')
          print(scaling_output_2)
          print(scaling_output_4)

          self.pB.ChangeDutyCycle(abs(scaling_output_2))
          GPIO.output(self.in3, GPIO.HIGH)
          GPIO.output(self.in4, GPIO.LOW)

          self.pD.ChangeDutyCycle(abs(scaling_output_4))
          GPIO.output(self.in7, GPIO.HIGH)
          GPIO.output(self.in8, GPIO.LOW)

        elif scaling_value > -0.2:
          print('Stopping motors 2 & 4')
          print(scaling_output_2)
          print(scaling_output_4)

          self.pB.ChangeDutyCycle(abs(scaling_output_2))
          GPIO.output(self.in3, GPIO.LOW)
          GPIO.output(self.in4, GPIO.LOW)

          self.pD.ChangeDutyCycle(abs(scaling_output_4))
          GPIO.output(self.in7, GPIO.LOW)
          GPIO.output(self.in8, GPIO.LOW)

    except Exception as e:
      print('Error: ', e)
      pass