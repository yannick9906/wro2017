#!/usr/bin/env python3
import ev3dev.ev3 as ev3
import time


class Main(object):

    def __init__(self):
        # Motoren:
        self.LMLeft = ev3.LargeMotor('outB')
        self.LMLeft.ramp_up_sp = 100
        self.LMLeft.ramp_down_sp = 100
        self.LMRight = ev3.LargeMotor('outD')
        self.LMRight.ramp_up_sp = 100
        self.LMRight.ramp_down_sp = 100
        self.MMHeber = ev3.MediumMotor('outC')
        self.MMGreifer = ev3.MediumMotor('outA')
        self.MMGreifer.position = 0
        self.MMGreifer.stop_action = 'hold'
        self.MMGreifer.speed_sp = 300
        self.MMGreifer.ramp_up_sp = 300
        self.MMHeber.position = 0
        self.MMHeber.stop_action = 'hold'
        self.MMHeber.speed_sp = 300
        self.MMGreifer.ramp_up_sp = 300
        # Sensoren:
        self.TSGreifer = ev3.TouchSensor('in1')
        self.CSGreifer = ev3.ColorSensor('in2')
        self.CSLeft = ev3.ColorSensor('in3')
        self.CSRight = ev3.ColorSensor('in4')

    def runToGreenEnd(self):
        self.LMLeft.run_forever()
        self.LMRight.run_forever()
        nogreen = True
        while nogreen:
            nogreen = not(self.CSLeft.color==3 and self.CSRight.color==3)
        self.LMRight.stop()
        self.LMLeft.stop()
        print("Green end reached.")

    def runToFirstJunctionFromGreen(self):
        self.runToGreenEnd()
        while not(self.CSRight.color==1 and self.CSLeft.color==1):
            self.LMLeft.run_forever()
            self.LMRight.run_forever()
            if self.CSLeft.color==1 and self.CSRight!=1:
                self.LMLeft.stop()
                print("Left")
            elif self.CSLeft.color!=1 and self.CSRight==1:
                self.LMRight.stop()
                print("Right")
        print("Junction reached.")

    def run(self):
        self.runToFirstJunctionFromGreen()

m = Main()
m.run()