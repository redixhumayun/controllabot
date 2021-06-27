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
    while True:
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
        break

    print("Running motor cleaup")
    self.stop_motors()
    GPIO.cleanup()

  def start_motors(self):

    GPIO.output(self.in1, GPIO.HIGH)
    GPIO.output(self.in2, GPIO.LOW)

    # GPIO.output(self.in3, GPIO.HIGH)
    # GPIO.output(self.in4, GPIO.LOW)

    # GPIO.output(self.in5, GPIO.HIGH)
    # GPIO.output(self.in6, GPIO.LOW)

    # GPIO.output(self.in7, GPIO.HIGH)
    # GPIO.output(self.in8, GPIO.LOW)

  def stop_motors(self):
    GPIO.output(self.in1, GPIO.LOW)
    GPIO.output(self.in2, GPIO.LOW)

    # GPIO.output(self.in3, GPIO.LOW)
    # GPIO.output(self.in4, GPIO.LOW)

    # GPIO.output(self.in5, GPIO.LOW)
    # GPIO.output(self.in6, GPIO.LOW)

    # GPIO.output(self.in7, GPIO.LOW)
    # GPIO.output(self.in8, GPIO.LOW)

  def reverse_motors(self):
    GPIO.output(self.in1, GPIO.LOW)
    GPIO.output(self.in2, GPIO.HIGH)

    # GPIO.output(self.in3, GPIO.LOW)
    # GPIO.output(self.in4, GPIO.HIGH)

    # GPIO.output(self.in5, GPIO.LOW)
    # GPIO.output(self.in6, GPIO.HIGH)

    # GPIO.output(self.in7, GPIO.LOW)
    # GPIO.output(self.in8, GPIO.HIGH)
  
  def turn_motors(self, scaling_value):
    print("scaling_value", scaling_value)
    inverted_scaling_value = 1 - abs(scaling_value)
    try:
      if scaling_value > 0:
        scaling_output_1 = inverted_scaling_value * self.duty_cycle_1
        scaling_output_3 = inverted_scaling_value * self.duty_cycle_3
        if scaling_output_1 < 100 and scaling_output_3 < 100:
          print("scaling_output_1", scaling_output_1)
          self.pA.ChangeDutyCycle(scaling_output_1)
          time.sleep(0.25)
      # elif scaling_value < 0:
      #   scaling_output_2 = inverted_scaling_value * self.duty_cycle_2
      #   scaling_output_4 = inverted_scaling_value * self.duty_cycle_4
      #   if scaling_output_2 < 100 and scaling_output_4 < 100:
      #     self.pB.ChangeDutyCycle(scaling_output_2)
      #     self.pD.ChangeDutyCycle(scaling_output_4)
    except Exception as e:
      print(e)
      pass

# GPIO.setmode(GPIO.BCM)

# GPIO.setup(in1, GPIO.OUT)
# GPIO.setup(in2, GPIO.OUT)
# GPIO.setup(enA, GPIO.OUT)
# GPIO.output(in1,GPIO.LOW)
# GPIO.output(in2,GPIO.LOW)
# pA=GPIO.PWM(enA, 2000)
# pA.start(50)

# GPIO.setup(in3, GPIO.OUT)
# GPIO.setup(in4, GPIO.OUT)
# GPIO.setup(enB, GPIO.OUT)
# GPIO.output(in3, GPIO.LOW)
# GPIO.output(in4, GPIO.LOW)
# pB = GPIO.PWM(enB, 2000)
# pB.start(50)

# try:
#   while True:
#     GPIO.output(in1,GPIO.HIGH)
#     GPIO.output(in2,GPIO.LOW)

#     GPIO.output(in3, GPIO.HIGH)
#     GPIO.output(in4, GPIO.LOW)

# except KeyboardInterrupt:
#   GPIO.cleanup()
#   sys.exit()