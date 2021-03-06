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
        #self.MMGreifer.stop_action = 'hold'
        self.MMGreifer.speed_sp = 1500
        self.MMGreifer.ramp_up_sp = 300
        self.MMHeber.position = 0
        #self.MMHeber.stop_action = 'hold'
        self.MMHeber.speed_sp = 300
        self.MMGreifer.ramp_up_sp = 300
        # Sensoren:
        self.TSGreifer = ev3.TouchSensor('in1')
        self.CSGreifer = ev3.ColorSensor('in2')
        self.CSLeft = ev3.ColorSensor('in3')
        self.CSRight = ev3.ColorSensor('in4')

    def textLaden(self):
        Pfad = "Auswertung.txt"
        read = open(Pfad , 'r')
        dateitext = read.read()
        return dateitext

    def dateiErstellen(self):
        Pfad = 'Auswertung.txt'
        write = open(Pfad, 'w')
        text = "Auswertung:"
        text = write.write(text + "\n")

    def textSchreiben(self, text):
        textAlt = self.textLaden()
        text = textAlt + text
        Pfad = 'Auswertung.txt'
        write = open(Pfad, 'w')
        text = write.write(text + "\n")

    def steinUeberpruefen(self):
        text = "Stein wird ueberprueft:"
        self.textSchreiben(text)
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
        print(Stein, farbeStein, strecke)
        text = "Steintyp: " + Stein + "; Farbe des Steins: " + farbeStein + "; Strecke(unwichtig): " + str(strecke)
        self.textSchreiben(text)
        return Stein, farbeStein, strecke

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
        self.MMHeber.run_to_abs_pos(position_sp=-440)

    def Beginn(self):
        self.LMLeft.run_timed(time_sp=2600, speed_sp=-300)
        self.LMRight.run_timed(time_sp=2600, speed_sp=-300)
        time.sleep(5)
        self.LMLeft.run_timed(time_sp=1000, speed_sp=-200)
        self.LMRight.run_timed(time_sp=1000, speed_sp=200)

    def kleineBewegung(self):
        self.LMLeft.run_timed(time_sp=5000, speed_sp=-100)
        self.LMRight.run_timed(time_sp=5000, speed_sp=-100)

    def ersterZweig(self):
        self.LMLeft.run_timed(time_sp=550, speed_sp=-200)
        self.LMRight.run_timed(time_sp=550, speed_sp=200)
        time.sleep(2)
        self.LMLeft.run_timed(time_sp=4400, speed_sp=-100)
        self.LMRight.run_timed(time_sp=4400, speed_sp=-100)

    def rechterZweig(self):
        self.LMLeft.run_timed(time_sp=550, speed_sp=-200)
        self.LMRight.run_timed(time_sp=550, speed_sp=200)
        time.sleep(2)
        stein, farbeStein, strecke = self.steinUeberpruefen()
        return stein, farbeStein, strecke

    def linkerZweig(self):
        for i in range(4):
            self.LMLeft.run_timed(time_sp=1000, speed_sp=100)
            self.LMRight.run_timed(time_sp=1000, speed_sp=100)
        time.sleep(2)
        self.LMLeft.run_timed(time_sp=1100, speed_sp=200)
        self.LMRight.run_timed(time_sp=1100, speed_sp=-200)
        stein, farbeStein, strecke = self.steinUeberpruefen()
        return stein, farbeStein, strecke

    def ersterZweigRueckweg(self, rechts, strecke):
        self.LMLeft.run_timed(time_sp=500, speed_sp=200)
        self.LMRight.run_timed(time_sp=500, speed_sp=200)
        time.sleep(5)
        if rechts == True:
             pass
        else:
             self.LMLeft.run_timed(time_sp=1000, speed_sp=-200)
             self.LMRight.run_timed(time_sp=1000, speed_sp=200)
        time.sleep(1)
        self.LMLeft.run_timed(time_sp=550, speed_sp=200)
        self.LMRight.run_timed(time_sp=550, speed_sp=-200)
        time.sleep(1)
        # An der Gabelung
        self.LMLeft.run_timed(time_sp=4400, speed_sp=100)
        self.LMRight.run_timed(time_sp=4400, speed_sp=100)
        time.sleep(5)
        self.LMLeft.run_timed(time_sp=550, speed_sp=200)
        self.LMRight.run_timed(time_sp=550, speed_sp=-200)
        time.sleep(1)
        self.LMLeft.run_timed(time_sp=4500, speed_sp=100)
        self.LMRight.run_timed(time_sp=4500, speed_sp=100)
        time.sleep(5)

    def zweiterZweig(self):
        self.kleineBewegung()
        time.sleep(2)
        self.kleineBewegung()
        time.sleep(2)
        self.LMLeft.run_timed(time_sp=550, speed_sp=-200)
        self.LMRight.run_timed(time_sp=550, speed_sp=200)
        time.sleep(2)
        self.LMLeft.run_timed(time_sp=4400, speed_sp=-100)
        self.LMRight.run_timed(time_sp=4400, speed_sp=-100)

    def zweiterZweigRueckweg(self, rechts, strecke):
        self.LMLeft.run_timed(time_sp=500, speed_sp=200)
        self.LMRight.run_timed(time_sp=500, speed_sp=200)
        time.sleep(5)
        if rechts == False:
            pass
        else:
            self.LMLeft.run_timed(time_sp=1000, speed_sp=-200)
            self.LMRight.run_timed(time_sp=1000, speed_sp=200)
        time.sleep(1)
        self.LMLeft.run_timed(time_sp=550, speed_sp=200)
        self.LMRight.run_timed(time_sp=550, speed_sp=-200)
        time.sleep(1)
        # An der Gabelung
        self.LMLeft.run_timed(time_sp=4400, speed_sp=100)
        self.LMRight.run_timed(time_sp=4400, speed_sp=100)
        time.sleep(5)
        self.LMLeft.run_timed(time_sp=550, speed_sp=200)
        self.LMRight.run_timed(time_sp=550, speed_sp=-200)
        time.sleep(1)
        self.LMLeft.run_timed(time_sp=9000, speed_sp=100)
        self.LMRight.run_timed(time_sp=9000, speed_sp=100)
        time.sleep(5)

    def dritterZweig(self):
        self.kleineBewegung()
        time.sleep(2)
        self.kleineBewegung()
        time.sleep(2)
        self.kleineBewegung()
        time.sleep(2)
        self.LMLeft.run_timed(time_sp=550, speed_sp=-200)
        self.LMRight.run_timed(time_sp=550, speed_sp=200)
        time.sleep(2)
        self.LMLeft.run_timed(time_sp=4400, speed_sp=-100)
        self.LMRight.run_timed(time_sp=4400, speed_sp=-100)

    def zurBase(self):
        self.LMLeft.run_timed(time_sp=1000, speed_sp=-200)
        self.LMRight.run_timed(time_sp=1000, speed_sp=200)
        time.sleep(1)
        self.LMLeft.run_timed(time_sp=10000, speed_sp=-100)
        self.LMRight.run_timed(time_sp=10000, speed_sp=-100)
        time.sleep(10)


    def FollowBlackLineBack(self):
        farbeLinks = self.CSLeft.color
        farbeRechts = self.CSRight.color
        while not(farbeLinks == 1 and farbeRechts == 1):
            if farbeLinks == 6 and farbeRechts == 6:
               self.LMLeft.run_timed(time_sp=150, speed_sp=200)
               self.LMRight.run_timed(time_sp=150, speed_sp=200)
               farbeLinks = self.CSLeft.color
               farbeRechts = self.CSRight.color
               print(farbeLinks, farbeRechts)
            elif farbeLinks == 1 and farbeRechts == 6:
               self.LMLeft.run_timed(time_sp=150, speed_sp=200)
               time.sleep(0.1)
               self.LMLeft.run_timed(time_sp=150, speed_sp=200)
               self.LMRight.run_timed(time_sp=150, speed_sp=200)
               time.sleep(0.1)
               self.LMRight.run_timed(time_sp=150, speed_sp=200)
               farbeLinks = self.CSLeft.color
               farbeRechts = self.CSRight.color
               print(farbeLinks, farbeRechts)
            elif farbeLinks == 6 and farbeRechts == 1:
               self.LMRight.run_timed(time_sp=150, speed_sp=200)
               time.sleep(0.1)
               self.LMLeft.run_timed(time_sp=150, speed_sp=200)
               self.LMRight.run_timed(time_sp=150, speed_sp=200)
               time.sleep(0.1)
               self.LMLeft.run_timed(time_sp=150, speed_sp=200)
               farbeLinks = self.CSLeft.color
               farbeRechts = self.CSRight.color
               print(farbeLinks, farbeRechts)
            else:
               farbeLinks = self.CSLeft.color
               farbeRechts = self.CSRight.color
               print("ERROR!!!")
        print("fertig")
        time.sleep(1)

    def ZielPlatzieren(self):
        farbeStein = self.CSGreifer.color
        self.heberHoch()
        if farbeStein == 2:
            self.LMLeft.run_timed(time_sp=550, speed_sp=200)
            self.LMRight.run_timed(time_sp=550, speed_sp=-200)
            time.sleep(1)
            self.LMLeft.run_timed(time_sp=4500, speed_sp=100)
            self.LMRight.run_timed(time_sp=4500, speed_sp=100)
            time.sleep(5)
            self.LMLeft.run_timed(time_sp=1100, speed_sp=-200)
            self.LMRight.run_timed(time_sp=1100, speed_sp=200)
            time.sleep(1.5)
            self.LMLeft.run_timed(time_sp=9000, speed_sp=100)
            self.LMRight.run_timed(time_sp=9000, speed_sp=100)
            time.sleep(5)
            self.LMLeft.run_timed(time_sp=1100, speed_sp=-200)
            self.LMRight.run_timed(time_sp=1100, speed_sp=200)
            time.sleep(1)
        elif farbeStein == 3:
            self.LMLeft.run_timed(time_sp=1650, speed_sp=200)
            self.LMRight.run_timed(time_sp=1650, speed_sp=-200)
            time.sleep(1)
            self.LMLeft.run_timed(time_sp=4500, speed_sp=100)
            self.LMRight.run_timed(time_sp=4500, speed_sp=100)
            time.sleep(1)
        elif farbeStein == 4:
            self.LMLeft.run_timed(time_sp=550, speed_sp=-200)
            self.LMRight.run_timed(time_sp=550, speed_sp=200)
            time.sleep(1)
            self.LMLeft.run_timed(time_sp=4500, speed_sp=100)
            self.LMRight.run_timed(time_sp=4500, speed_sp=100)
            time.sleep(5)
            self.LMLeft.run_timed(time_sp=1100, speed_sp=200)
            self.LMRight.run_timed(time_sp=1100, speed_sp=-200)
            time.sleep(1.5)
            self.LMLeft.run_timed(time_sp=9000, speed_sp=100)
            self.LMRight.run_timed(time_sp=9000, speed_sp=100)
            time.sleep(5)
            self.LMLeft.run_timed(time_sp=1100, speed_sp=200)
            self.LMRight.run_timed(time_sp=1100, speed_sp=-200)
            time.sleep(1)
        elif farbeStein == 5:
            self.LMLeft.run_timed(time_sp=550, speed_sp=-200)
            self.LMRight.run_timed(time_sp=550, speed_sp=200)
            time.sleep(1)
            self.LMLeft.run_timed(time_sp=3000, speed_sp=100)
            self.LMRight.run_timed(time_sp=3000, speed_sp=100)
            time.sleep(5)
            self.LMLeft.run_timed(time_sp=1100, speed_sp=200)
            self.LMRight.run_timed(time_sp=1100, speed_sp=-200)
            time.sleep(1.5)
            self.LMLeft.run_timed(time_sp=4500, speed_sp=100)
            self.LMRight.run_timed(time_sp=4500, speed_sp=100)
            time.sleep(5)
            self.LMLeft.run_timed(time_sp=1100, speed_sp=200)
            self.LMRight.run_timed(time_sp=1100, speed_sp=-200)
            time.sleep(1)
        self.heberRunter()
        self.greiferAuf()
        time.sleep(1)
        return farbeStein

    def Zielzurueck(self, farbeStein):
        if farbeStein == 2:
            self.LMLeft.run_timed(time_sp=1100, speed_sp=200)
            self.LMRight.run_timed(time_sp=1100, speed_sp=-200)
            time.sleep(1)
            self.LMLeft.run_timed(time_sp=9000, speed_sp=-100)
            self.LMRight.run_timed(time_sp=9000, speed_sp=-100)
            time.sleep(5)
            self.LMLeft.run_timed(time_sp=1100, speed_sp=200)
            self.LMRight.run_timed(time_sp=1100, speed_sp=-200)
            time.sleep(1.5)
            self.LMLeft.run_timed(time_sp=4500, speed_sp=-100)
            self.LMRight.run_timed(time_sp=4500, speed_sp=-100)
            time.sleep(5)
            self.LMLeft.run_timed(time_sp=550, speed_sp=-200)
            self.LMRight.run_timed(time_sp=550, speed_sp=200)
            time.sleep(1)
        if farbeStein == 3:
            self.LMLeft.run_timed(time_sp=4500, speed_sp=-100)
            self.LMRight.run_timed(time_sp=4500, speed_sp=-100)
            time.sleep(1)
            self.LMLeft.run_timed(time_sp=1650, speed_sp=-200)
            self.LMRight.run_timed(time_sp=1650, speed_sp=200)
            time.sleep(1)
        if farbeStein == 4:
            self.LMLeft.run_timed(time_sp=1100, speed_sp=-200)
            self.LMRight.run_timed(time_sp=1100, speed_sp=200)
            time.sleep(1)
            self.LMLeft.run_timed(time_sp=9000, speed_sp=-100)
            self.LMRight.run_timed(time_sp=9000, speed_sp=-100)
            time.sleep(5)
            self.LMLeft.run_timed(time_sp=1100, speed_sp=-200)
            self.LMRight.run_timed(time_sp=1100, speed_sp=200)
            time.sleep(1.5)
            self.LMLeft.run_timed(time_sp=4500, speed_sp=-100)
            self.LMRight.run_timed(time_sp=4500, speed_sp=-100)
            time.sleep(5)
            self.LMLeft.run_timed(time_sp=550, speed_sp=200)
            self.LMRight.run_timed(time_sp=550, speed_sp=-200)
            time.sleep(1)
        if farbeStein == 5:
            self.LMLeft.run_timed(time_sp=1100, speed_sp=200)
            self.LMRight.run_timed(time_sp=1100, speed_sp=-200)
            time.sleep(1)
            self.LMLeft.run_timed(time_sp=4500, speed_sp=-100)
            self.LMRight.run_timed(time_sp=4500, speed_sp=-100)
            time.sleep(5)
            self.LMLeft.run_timed(time_sp=1100, speed_sp=200)
            self.LMRight.run_timed(time_sp=1100, speed_sp=-200)
            time.sleep(1.5)
            self.LMLeft.run_timed(time_sp=4000, speed_sp=-100)
            self.LMRight.run_timed(time_sp=4000, speed_sp=-100)
            time.sleep(5)
            self.LMLeft.run_timed(time_sp=550, speed_sp=200)
            self.LMRight.run_timed(time_sp=550, speed_sp=-200)
            time.sleep(1)

    def fundamentBesorgen(self):
        self.LMLeft.run_timed(time_sp=2600, speed_sp=-300)
        self.LMRight.run_timed(time_sp=2600, speed_sp=-300)
        time.sleep(5)
        self.LMLeft.run_timed(time_sp=1000, speed_sp=200)
        self.LMRight.run_timed(time_sp=1000, speed_sp=-200)
        time.sleep(1)
        self.LMLeft.run_timed(time_sp=1000, speed_sp=-200)
        self.LMRight.run_timed(time_sp=1000, speed_sp=-200)
        time.sleep(5)
        self.LMLeft.run_timed(time_sp=500, speed_sp=-200)
        self.LMRight.run_timed(time_sp=500, speed_sp=200)
        time.sleep(1)
        self.LMLeft.run_timed(time_sp=4500, speed_sp=100)
        self.LMRight.run_timed(time_sp=4500, speed_sp=100)
        time.sleep(1)
        self.LMLeft.run_timed(time_sp=1000, speed_sp=-200)
        self.LMRight.run_timed(time_sp=1000, speed_sp=200)
        time.sleep(1)
        self.LMLeft.run_timed(time_sp=1000, speed_sp=-200)
        self.LMRight.run_timed(time_sp=1000, speed_sp=-200)
        time.sleep(5)
        self.LMLeft.run_timed(time_sp=1000, speed_sp=-200)
        self.LMRight.run_timed(time_sp=1000, speed_sp=200)
        time.sleep(1)
        self.heberRunter()
        self.greiferAuf()
        time.sleep(1)
        self.LMLeft.run_timed(time_sp=10000, speed_sp=100)
        self.LMRight.run_timed(time_sp=10000, speed_sp=100)
        time.sleep(10)

    #
#####################################################################################
# Hauptprogramm:
#####################################################################################

    def programm(self):
        self.Beginn()
        time.sleep(5)
        self.kleineBewegung()
        time.sleep(2.5)
        self.ersterZweig()
        time.sleep(5)
        strecke = 0
        stein, farbeStein, strecke = self.rechterZweig()
        text = "Rechter Zweig überprüft und abgefahren!"
        self.textSchreiben(text)
        time.sleep(5)
        rechtsE = True
        if stein == "MANTEL":
            text = "Mantel festgestellt! Rückfahrt beginnt!"
        else:
            text = "Powerstein festgestellt! Anderer Zweig wird befahren!"
            self.textSchreiben(text)
            stein, farbeStein, strecke = self.linkerZweig()
            rechtsE = False
            text = "Linker Zweig abgefahren!"
            self.textSchreiben(text)
        text = "Rueckweg von erster Kreuzung beginnt!"
        self.textSchreiben(text)
        self.ersterZweigRueckweg(rechtsE, strecke)
        farbeStein = self.ZielPlatzieren()
        text = "Rueckkehr vom Fundament wird angetreten!"
        self.Zielzurueck(farbeStein)
        text = "Zweiter Zweig wird abgefahren!"
        self.zweiterZweig()
        time.sleep(5)
        stein, farbeStein, strecke = self.rechterZweig()
        text = "Rechter Zweig überprüft und abgefahren!"
        self.textSchreiben(text)
        time.sleep(5)
        rechtsZ = True
        if stein == "MANTEL":
            text = "Mantel festgestellt! Rückfahrt beginnt!"
        else:
            text = "Powerstein festgestellt! Anderer Zweig wird befahren!"
            self.textSchreiben(text)
            stein, farbeStein, strecke = self.linkerZweig()
            rechtsZ = False
            text = "Linker Zweig abgefahren!"
            self.textSchreiben(text)
        text = "Rueckweg von zweiter Kreuzung beginnt!"
        self.textSchreiben(text)
        self.zweiterZweigRueckweg(rechtsZ, strecke)
        farbeStein = self.ZielPlatzieren()
        text = "Rueckkehr vom Fundament wird angetreten!"
        self.Zielzurueck(farbeStein)
        text = "Dritter Zweig wird abgefahren!"
        self.dritterZweig()
        time.sleep(5)
        stein, farbeStein, strecke = self.rechterZweig()
        text = "Rechter Zweig überprüft und abgefahren!"
        self.textSchreiben(text)
        time.sleep(5)
        rechtsD = True
        if stein == "MANTEL":
            text = "Mantel festgestellt! Rückfahrt beginnt!"
        else:
            text = "Powerstein festgestellt! Anderer Zweig wird befahren!"
            self.textSchreiben(text)
            stein, farbeStein, strecke = self.linkerZweig()
            rechtsD = False
            text = "Linker Zweig abgefahren!"
            self.textSchreiben(text)
        text = "Rueckweg von dritter Kreuzung beginnt!"
        self.textSchreiben(text)
        self.dritterZweigRueckweg(rechtsD, strecke)
        farbeStein = self.ZielPlatzieren()
        text = "Rueckkehr vom Fundament wird angetreten!"
        self.Zielzurueck(farbeStein)
        self.zurBase()

#Einrichtung des Roboters:
m = Main()
print('Die kurfuerstlichen Roboter')
m.dateiErstellen()
m.programm()