#!/usr/bin/env python3
import ev3dev.ev3 as ev3
import time


class Main(object):

    def __init__(self):
        # Motoren:
        self.LMLeft = ev3.LargeMotor('outB')
        self.LMLeft.speed_sp = 200
        self.LMLeft.ramp_up_sp = 100
        self.LMLeft.ramp_down_sp = 100
        self.LMRight = ev3.LargeMotor('outD')
        self.LMRight.speed_sp = 200
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

        self.LMRight.stop()
        self.LMLeft.stop()

    def logToFile(self, text):
        print(text)
        with open("logfile.log", 'a') as file:
            file.write("\n"+text)

    def readOutSensors(self):
        self.logToFile('TSGreifer: '+str(self.TSGreifer.is_pressed)+' CSGreifer: '+str(self.CSGreifer.color)+' CSLeft: '+str(self.CSLeft.color)+' CSRight: '+str(self.CSRight.color))

    def rotate90DegLeft(self):
        self.LMLeft.run_timed(time_sp=1100)
        self.LMRight.run_timed(time_sp=1100, speed_sp=-200)
        time.sleep(1.1)

    def rotate90DegRight(self):
        self.LMRight.run_timed(time_sp=1100)
        self.LMLeft.run_timed(time_sp=1100, speed_sp=-200)
        time.sleep(1.1)

    def rotate45DegLeft(self):
        self.LMRight.run_timed(time_sp=550, speed_sp=-200)
        self.LMLeft.run_timed(time_sp=550)
        time.sleep(.6)

    def rotate45DegRight(self):
        self.LMRight.run_timed(time_sp=550)
        self.LMLeft.run_timed(time_sp=550, speed_sp=-200)
        time.sleep(.6)

    def runToGreenEnd(self):
        self.LMLeft.run_forever()
        self.LMRight.run_forever()
        green = True
        while green:
            self.readOutSensors()
            green = (self.CSLeft.color==3 or self.CSLeft.color==2) and (self.CSRight.color==3 or self.CSRight.color==2)
        self.LMRight.stop()
        self.LMLeft.stop()
        self.logToFile("Green end reached.")

    def runToFirstJunctionFromGreen(self):
        self.runToGreenEnd()
        self.runToNextJunction()

    def runToNextJunction(self):
        self.LMLeft.speed_sp = 200
        self.LMRight.speed_sp = 200
        while not(self.CSRight.color==1 and self.CSLeft.color==1):
            self.LMLeft.run_forever()
            self.LMRight.run_forever()
            if self.CSLeft.color==1 and self.CSRight!=1:
                self.LMLeft.stop()
                self.logToFile("Left")
            elif self.CSLeft.color!=1 and self.CSRight==1:
                self.LMRight.stop()
                self.logToFile("Right")
        self.logToFile("Junction reached.")
        self.LMLeft.stop()
        self.LMRight.stop()

    def greiferAuf(self):
        self.MMGreifer.run_to_abs_pos(position_sp=-330)

    def heberHoch(self):
        self.MMHeber.run_to_abs_pos(position_sp=0)

    def heberRunter(self):
        self.MMHeber.run_to_abs_pos(position_sp=-440)

    def steinUeberpruefen(self):
        self.heberHoch()
        self.heberRunter()
        self.greiferAuf()
        time.sleep(2)
        farbeGreifer = self.CSGreifer.color
        strecke = 0
        while farbeGreifer == 0:
            self.LMLeft.run_timed(time_sp=100, speed_sp=-200)
            self.LMRight.run_timed(time_sp=100, speed_sp=-200)
            strecke += 1
            farbeGreifer = self.CSGreifer.color
            print(farbeGreifer)
        self.LMLeft.run_timed(time_sp=300, speed_sp=-200)
        self.LMRight.run_timed(time_sp=300, speed_sp=-200)
        time.sleep(1)
        # AN GREIFER AUF ANPASSEN!!!
        Position = 0
        gedrückt = self.TSGreifer.is_pressed
        while gedrückt != 1:
            self.MMGreifer.run_to_abs_pos(position_sp=Position)
            Position += 5
            gedrückt = self.TSGreifer.is_pressed
        if strecke >= 50:
            Stein = "POWER"
        else:
            Stein = "MANTEL"
        farbeStein = self.CSGreifer.color
        self.heberHoch()
        self.logToFile(str(Stein)+" "+str(farbeStein)+" "+str(strecke))
        return Stein, farbeStein, strecke

    def firstbranch1(self):
        # Erste Ast
        self.rotate45DegLeft()
        self.runToNextJunction()
        self.rotate45DegLeft()
        self.rotate90DegLeft()
        self.rotate90DegLeft()

    def firstbranch1back(self):
        self.runToNextJunction()
        self.rotate45DegRight()
        self.runToNextJunction()
        self.rotate45DegRight()

    def runToFundament(self, color):
        self.runToNextJunction()
        self.runToNextJunction()
        if color == 1:
            pass
        elif color == 2:
            pass
        elif color == 3:
            pass
        elif color == 4:
            pass
        elif color == 5:
            pass

    def run(self):
        self.runToFirstJunctionFromGreen()
        self.rotate90DegRight()
        self.runToNextJunction()

        self.firstbranch1()

        stein, farbe, strecke = self.steinUeberpruefen()
        if stein == "MANTEL":
            self.firstbranch1back()
            self.runToFundament(farbe)
        elif stein == "POWER":
            pass  # Todo fallen lassen & Farbe merken


m = Main()
m.run()
