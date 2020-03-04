"""
** mafaa **

Pyboard stepper code for L239D

For 6 wires unipolar stepper connect the common wires to negative to make 5 wires stepper
Pyboard inputs can be connected parallel 2 L239D ICs pins (1, 2, 7, 9, 10 & 15) to drive 2 stepper motors
W - Wave Drive
F - Full step Drive

calculate number of steps for 360 degrees and call for forward & backward rotation required
# Trav_Dist = (Requried distance / wheel circumfrence) * steps to cover 360 degree  #travel distance

Code Uturn rotation not required if managed with forward_rot & backward_rot codes
    code to understand drive both motors in opposite direction
"""

import pyb
from pyb import Pin, delay

class PybStepper:
    # set up stepper motors pinout 
    def __init__(self, A1, A2, B1, B2, E1, E2):
        #global P_A1, P_A2, P_B1, P_B2, P_E1, P_E2
        self.P_A1 = pyb.Pin(A1, pyb.Pin.OUT_PP)
        self.P_A2 = pyb.Pin(A2, pyb.Pin.OUT_PP)
        self.P_B1  =pyb.Pin(B1, pyb.Pin.OUT_PP)
        self.P_B2 = pyb.Pin(B2, pyb.Pin.OUT_PP)
        self.P_E1 = pyb.Pin(E1, pyb.Pin.OUT_PP, pyb.Pin.PULL_UP)
        self.P_E2 = pyb.Pin(E2, pyb.Pin.OUT_PP, pyb.Pin.PULL_UP)
        pyb.delay(5)

    def W_forwardStep(self):
        self.setStepper(1, 0, 1, 0)
        self.setStepper(0, 1, 1, 0)
        self.setStepper(0, 1, 0, 1)
        self.setStepper(1, 0, 0, 1)

    def W_backwardStep(self):
        self.setStepper(1, 0, 0, 1)
        self.setStepper(0, 1, 0, 1)
        self.setStepper(0, 1, 1, 0)
        self.setStepper(1, 0, 1, 0)

    def F_forwardStep(self):
        self.setStepper(1, 0, 1, 0)
        self.setStepper(1, 1, 1, 0)
        self.setStepper(0, 1, 1, 0)
        self.setStepper(0, 1, 1, 1)
        self.setStepper(0, 1, 0, 1)
        self.setStepper(1, 1, 0, 1)
        self.setStepper(1, 0, 0, 1)
        self.setStepper(1, 0, 1, 1)

    def F_backwardStep(self):
        self.setStepper(1, 0, 0, 1)
        self.setStepper(1, 1, 0, 1)
        self.setStepper(0, 1, 0, 1)
        self.setStepper(0, 1, 1, 1)
        self.setStepper(0, 1, 1, 0)
        self.setStepper(1, 1, 1, 0)
        self.setStepper(1, 0, 1, 0)
        self.setStepper(1, 0, 1, 1)

    def setStepper(self, in1, in2, in3, in4):
        self.P_A1.value(in1)
        self.P_A2.value(in2)
        self.P_B1.value(in3)
        self.P_B2.value(in4)
        pyb.delay(5)

    # this will de-energize all coils, motor draws zero current
    # Note: Stepper motor can freely rotate by hand
    def clear_all(self):
        self.P_A1.low()
        self.P_A2.low()
        self.P_B1.low()
        self.P_B2.low()
        pyb.delay(5)

    #Rot_cou: Rotation count 
    def forward_rot(self, Rot_cou, E):
        print ("forward rotation") 
        if E == 0:  # 2 - both Motors
          self.P_E1.high()
          self.P_E2.high()
        elif E == 1:  # 1 - only Motor 1 - Rt turn
          self.P_E1.high()
          self.P_E2.low()
        else:  # 2 - only Motor 2 - Lt turn
          self.P_E1.high()
          self.P_E2.high()
        for i in range(Rot_cou): 
          self.W_forwardStep() 
          pyb.delay(5)

    def backward_rot(self, Rot_cou, E):
        print ("backward rotation")
        if E == 0:  # 2 - both Motors
          self.P_E1.high()
          self.P_E2.high()
        elif E == 1:  # 1 - only Motor 1 - Rt turn
          self.P_E1.high()
          self.P_E2.low()
        else:  # 2 - only Motor 2 - Lt turn
          self.P_E1.low()
          self.P_E2.high()
        for i in range(Rot_cou):
          self.F_backwardStep() 
          pyb.delay(5)

    def Uturn_rot(self, Rot_cou):
        print ("UStep")
        for i in range(Rot_cou):
           self.P_E1.high()
           self.P_E2.low()
           pyb.delay(1)
           self.F_forwardStep()
           #pyb.delay(5)
           self.P_E1.low()
           self.P_E2.high()
           pyb.delay(1)
           self.F_backwardStep() 
           #pyb.delay(5)
