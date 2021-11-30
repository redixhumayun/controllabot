
import RPi.GPIO as GPIO          
from time import sleep

# motor 1
in1 = 8
in2 = 7
enA = 12

# motor 2
in3 = 6
in4 = 5
enB = 13

# motor 3
in5 = 24
in6 = 23
enC = 25

# motor 4
in7 = 27
in8 = 17
enD = 22

GPIO.setmode(GPIO.BCM)

GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(enA, GPIO.OUT)
GPIO.output(in1, GPIO.LOW)
GPIO.output(in2, GPIO.LOW)
pA = GPIO.PWM(enA, 1500)
pA.start(0)

GPIO.setup(in3, GPIO.OUT)
GPIO.setup(in4, GPIO.OUT)
GPIO.setup(enB, GPIO.OUT)
GPIO.output(in3, GPIO.LOW)
GPIO.output(in4, GPIO.LOW)
pB = GPIO.PWM(enB, 1500)
pB.start(0)

GPIO.setup(in5, GPIO.OUT)
GPIO.setup(in6, GPIO.OUT)
GPIO.setup(enC, GPIO.OUT)
GPIO.output(in5, GPIO.LOW)
GPIO.output(in6, GPIO.LOW)
pC = GPIO.PWM(enC, 1500)
pC.start(0)

GPIO.setup(in7, GPIO.OUT)
GPIO.setup(in8, GPIO.OUT)
GPIO.setup(enD, GPIO.OUT)
GPIO.output(in7, GPIO.LOW)
GPIO.output(in8, GPIO.LOW)
pD = GPIO.PWM(enD, 1500)
pD.start(0)

try:
  while True:
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)

    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in4, GPIO.LOW)

    GPIO.output(in5, GPIO.HIGH)
    GPIO.output(in6, GPIO.LOW)

    GPIO.output(in7, GPIO.HIGH)
    GPIO.output(in8, GPIO.LOW)

    for dc in range(0, 50, 3):
      pA.ChangeDutyCycle(dc)
      pB.ChangeDutyCycle(dc)
      pC.ChangeDutyCycle(dc)
      pD.ChangeDutyCycle(dc)
      sleep(0.1)
except KeyboardInterrupt:
  print("Cleaning up GPIO pins")
  GPIO.cleanup()