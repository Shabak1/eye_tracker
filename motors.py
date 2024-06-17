import numpy as np
import serial
import time
import cv2

class Motor:
  def __init__(self, path):
    self.path = path
    self.speed = 100
    self.step = 10
    self.threshold = 50

  def forward(self):
    # Code to send a forward command to the motor
    
    pass

  def backward(self):
    # Code to send a backward command to the motor
    
    pass


while cv2.getWindowProperty("Video", cv2.WND_PROP_VISIBLE) >= 1:
  # Open the serial port to the eye tracker
  ser = serial.Serial('/dev/ttyUSB0', 9600)
  # Wait for the eye tracker to start sending data
  time.sleep(1)
  # Continuously read data from the eye tracker
  while True:
      # Read a line of data from the eye tracker
      line = ser.readline()
      # Decode the data from the eye tracker
      data = line.decode('utf-8')
      # Split the data into a list of values
      values = data.split(',')
      # Get the x and y coordinates of the eye gaze
      x = float(values[0])
      y = float(values[1])
      # Convert the x and y coordinates to the center of the screen
      x -= 640 / 2
      y -= 480 / 2
    
      # Set the path to the motors
      motor_right = Motor('/dev/ttyUSB0')
      motor_left = Motor('/dev/ttyUSB1')
    
      if x < 320 and y < 240:
        motor_right.forward()
      elif x > 320 and y < 240:
        motor_left.forward()
      elif x < 320 and y > 240:
        motor_left.backward()
      elif x > 320 and y > 240:
        motor_right.backward()
      elif x == 320 and y == 0:
        motor_right.forward()
        motor_left.forward()
      elif x == 320 and y == 480:
        motor_right.backward()
        motor_left.backward()
      elif x == 0 and y == 240:
        motor_right.forward()
        motor_left.backward()
      elif x == 640 and y == 240:
        motor_right.backward()
        motor_left.forward()
        pass
