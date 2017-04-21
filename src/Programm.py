#!/usr/bin/env python3
import ev3dev.ev3 as ev3
import time


class Main(object):

    def __init__(self):
        # Motoren:
        self.LMLeft = ev3.LargeMotor('outA')
        self.LMRight = ev3.LargeMotor('outB')
        self.MMHeber = ev3.MediumMotor('outC')
        self.MMGreifer = ev3.MediumMotor('outD')
        self.MMGreifer.position = 0
        self.MMGreifer.stop_action = 'hold'
        self.MMGreifer.speed_sp = 100
        self.MMGreifer.run_to_abs_pos(position_sp=0, speed_sp=1000)
        # Sensoren:
        self.CSGreifer1 = ev3.ColorSensor('in1')
        self.CSGreifer2 = ev3.ColorSensor('in2')
        self.CSLeft = ev3.ColorSensor('in3')
        self.CSRight = ev3.ColorSensor('in4')

    def ersterZweig(self):
        farbeRechts = self.CSRight.color
        while farbeRechts != 1:
            m.followBlackline()
            farbeRechts = self.CSRight.color
        self.LMLeft.run_timed(time_sp=300, speed_sp=-200)
        time.sleep(0.1)
        farbeRechts = self.CSRight.color
        farbeLinks = self.CSLeft.color
        while farbeRechts != 1 or farbeLinks != 1:
            m.followBlackline()
            farbeRechts = self.CSRight.color
            farbeLinks = self.CSLeft.color
        self.LMLeft.run_timed(time_sp=300, speed_sp=-200)

    def steinUeberpruefen(self):
        farbeGreifer1 = self.CSGreifer1.color
        farbeGreifer2 = self.CSGreifer2.color
        while farbeGreifer1 == 0 and farbeGreifer2 == 0:
            self.LMLeft.run_timed(time_sp=10, speed_sp=-100)
            self.LMRight.run_timed(time_sp=10, speed_sp=-100)
            farbeGreifer1 = self.CSGreifer1.color
            farbeGreifer2 = self.CSGreifer2.color
        PositionGreifer = -300
        self.MMGreifer.run_to_abs_pos(position_sp=-300)
        while farbeGreifer1 != 0 and farbeGreifer2 != 0:
            PositionGreifer += 10
            self.MMGreifer.run_to_abs_pos(position_sp=PositionGreifer)
            farbeGreifer1 = self.CSGreifer1.color
            farbeGreifer2 = self.CSGreifer2.color
        PositionGreifer -= 10
        self.MMGreifer.run_to_abs_pos(position_sp=PositionGreifer)
        farbeGreifer1 = self.CSGreifer1.color
        farbeGreifer2 = self.CSGreifer2.color
        if farbeGreifer1 == farbeGreifer2:
            farbeStein = farbeGreifer2
        else:


    def followBlackline(self):
        farbeLinks = self.CSLeft.color
        farbeRechts = self.CSRight.color
        if farbeLinks == 6 and farbeRechts == 6:
            self.LMLeft.run_timed(time_sp=150, speed_sp=-200)
            self.LMRight.run_timed(time_sp=150, speed_sp=-200)
        elif farbeLinks == 1 and farbeRechts == 6:
            self.LMRight.run_timed(time_sp=300, speed_sp=-200)
            time.sleep(0.1)
            self.LMLeft.run_timed(time_sp=150, speed_sp=-200)
            self.LMRight.run_timed(time_sp=150, speed_sp=-200)
        elif farbeLinks == 6 and farbeRechts == 1:
            self.LMLeft.run_timed(time_sp=300, speed_sp=-200)
            time.sleep(0.1)
            self.LMLeft.run_timed(time_sp=150, speed_sp=-200)
            self.LMRight.run_timed(time_sp=150, speed_sp=-200)
        else:
            self.LMLeft.run_timed(time_sp=150, speed_sp=-200)
            self.LMRight.run_timed(time_sp=150, speed_sp=-200)

    def greiferMantel(self):
        self.MMGreifer.run_to_abs_pos(position_sp=-145)

    def greiferAuf(self):
        self.MMGreifer.run_to_abs_pos(position_sp=-300)

    def greiferZu(self):
        self.MMGreifer.run_to_abs_pos(position_sp=0)

    def greiferStein(self):
        self.MMGreifer.run_to_abs_pos(position_sp=-45)

    def testBewegung(self):
        # Gerade aus:
        self.LMLeft.run_timed(time_sp=1000, speed_sp=1000)
        self.LMRight.run_timed(time_sp=1000, speed_sp=1000)

    def heberHoch(self):
        self.MMHeber.run_to_rel_pos(position_sp=-2510, speed_sp=1000)

    def heberRunter(self):
        self.MMHeber.run_to_rel_pos(position_sp=2510, speed_sp=1000)

#####################################################################################
# Hauptprogramm:
#####################################################################################

# Einrichtung des Roboters:
m = Main()
print('Die kurfuerstlichen Roboter')
#m.heberHoch()
# Testfahrt:
#for i in range(100):
#    m.followBlackline()
