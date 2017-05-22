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
        self.heberRunter()
        self.greiferAuf()
        time.sleep(2)
        farbeGreifer = self.CSGreifer.color
        while farbeGreifer == 0 or farbeGreifer == 5:
            self.LMLeft.run_timed(time_sp=100, speed_sp=-200)
            self.LMRight.run_timed(time_sp=100, speed_sp=-200)
            farbeGreifer = self.CSGreifer.color
            print(farbeGreifer)
        self.LMLeft.run_timed(time_sp=300, speed_sp=-200)
        self.LMRight.run_timed(time_sp=300, speed_sp=-200)
        # AN GREIFER AUF ANPASSEN!!!
        Position = 0
        gedrückt = self.TSGreifer.is_pressed
        while gedrückt != 1:
            self.MMGreifer.run_to_abs_pos(position_sp=Position)
            Position += 5
            gedrückt = self.TSGreifer.is_pressed
        if Position >= -100:
            Stein = "Mantel"
        else:
            Stein = "Power"
        farbeStein = self.CSGreifer.color
        return Stein, farbeStein

    def followBlackline(self):
        farbeLinks = self.CSLeft.color
        farbeRechts = self.CSRight.color
        if farbeLinks == 6 and farbeRechts == 6:
            self.LMLeft.run_timed(time_sp=150, speed_sp=-200)
            time.sleep(0.1)
            self.LMRight.run_timed(time_sp=150, speed_sp=-200)
        elif farbeLinks == 1 and farbeRechts == 6:
            self.LMLeft.run_timed(time_sp=150, speed_sp=-200)
            time.sleep(0.1)
            self.LMLeft.run_timed(time_sp=150, speed_sp=-200)
            self.LMRight.run_timed(time_sp=150, speed_sp=-200)
            time.sleep(0.1)
            self.LMRight.run_timed(time_sp=150, speed_sp=-200)
        elif farbeLinks == 6 and farbeRechts == 1:
            self.LMLeft.run_timed(time_sp=150, speed_sp=-200)
            self.LMRight.run_timed(time_sp=150, speed_sp=-200)
        else:
            self.LMLeft.run_timed(time_sp=150, speed_sp=200)
            self.LMRight.run_timed(time_sp=150, speed_sp=-200)

    def greiferMantel(self):
        self.MMGreifer.run_to_abs_pos(position_sp=-145)

    def greiferAuf(self):
        self.MMGreifer.run_to_abs_pos(position_sp=-330)

    def greiferZu(self):
        self.MMGreifer.run_to_abs_pos(position_sp=0)

    def greiferStein(self):
        self.MMGreifer.run_to_abs_pos(position_sp=-45)

    def testBewegung(self):
        # Gerade aus:
        self.LMLeft.run_timed(time_sp=200, speed_sp=-100)
        self.LMRight.run_timed(time_sp=200, speed_sp=-100)

    def heberHoch(self):
        self.MMHeber.run_to_abs_pos(position_sp=0)

    def heberRunter(self):
        self.MMHeber.run_to_abs_pos(position_sp=-430)

    def Beginn(self):
        for i in range(100):
            self.LMLeft.run_timed(time_sp=275, speed_sp=-600)
            self.LMRight.run_timed(time_sp=275, speed_sp=-600)
        time.sleep(1)
        self.LMLeft.run_timed(time_sp=850, speed_sp=-200)
        self.LMRight.run_timed(time_sp=850, speed_sp=200)

    def kleineBewegung(self):
        self.LMLeft.run_timed(time_sp=1000, speed_sp=-100)
        self.LMRight.run_timed(time_sp=1000, speed_sp=-100)

    def ersterZweig(self):
        for i in range(12):
            pass
#
#####################################################################################
# Hauptprogramm:
#####################################################################################

    def Programm(self):
        self.Beginn()
        time.sleep(3)
        self.kleineBewegung()
        #ersterZweig()

# Einrichtung des Roboters:
m = Main()
print('Die kurfuerstlichen Roboter')

