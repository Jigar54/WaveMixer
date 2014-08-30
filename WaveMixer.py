import kivy
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.app import App
from functools import partial
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.label import Label
import wave
from kivy.core.audio import SoundLoader
from kivy.uix.slider import Slider
import struct
import numpy
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.uix.checkbox import CheckBox
from kivy.graphics import Color
from kivy.graphics import Rectangle
from kivy.uix.popup import Popup

import pyaudio
Builder.load_file('bt1.kv')

from kivy.graphics import BorderImage


class MyWave(Popup):

    def mod3(self):
        if (self.l > self.l1 and self.l > self.l2):
            final = self.l
            if (self.l1 >= self.l2):
                for i in range(self.l):
                    if (i < self.l2):
                        self.mod.append(
                            self.out[i] * self.out1[i] * self.out2[i])
                    elif (i < self.l1):
                        self.mod.append(self.out[i] * self.out1[i])
                    else:
                        self.mod.append(self.out[i])

            elif (self.l2 > self.l1):
                for i in range(self.l):
                    if (i < self.l1):
                        self.mod.append(
                            self.out[i] * self.out1[i] * self.out2[i])
                    elif (i < self.l2):
                        self.mod.append(self.out[i] * self.out2[i])
                    else:
                        self.mod.append(self.out[i])

        elif (self.l1 > self.l2 and self.l1 > self.l):
            final = self.l1
            if (self.l >= self.l2):
                for i in range(self.l1):
                    if (i < self.l2):
                        self.mod.append(
                            self.out[i] * self.out1[i] * self.out2[i])
                    elif (i < self.l):
                        self.mod.append(self.out[i] * self.out1[i])
                    else:
                        self.mod.append(self.out1[i])

            elif (self.l2 > self.l):
                for i in range(self.l1):
                    if (i < self.l):
                        self.mod.append(
                            self.out[i] * self.out1[i] * self.out2[i])
                    elif (i < self.l2):
                        self.mod.append(self.out1[i] * self.out2[i])
                    else:
                        self.mod.append(self.out1[i])

        elif (self.l2 >= self.l1 and self.l2 >= self.l):
            final = self.l2
            if (self.l >= self.l1):
                for i in range(self.l2):
                    if (i < self.l1):
                        self.mod.append(
                            self.out[i] * self.out1[i] * self.out2[i])
                    elif (i < self.l):
                        self.mod.append(self.out[i] * self.out2[i])
                    else:
                        self.mod.append(self.out2[i])

            elif (self.l1 > self.l):
                for i in range(self.l2):
                    if (i < self.l2):
                        self.mod.append(
                            self.out[i] * self.out1[i] * self.out2[i])
                    elif (i < self.l1):
                        self.mod.append(self.out1[i] * self.out2[i])
                    else:
                        self.mod.append(self.out2[i])
        return final

    def mix3(self):
        if (self.l > self.l1 and self.l > self.l2):
            final = self.l
            if (self.l1 >= self.l2):
                for i in range(self.l):
                    if (i < self.l2):
                        self.mix.append(
                            self.out[i] + self.out1[i] + self.out2[i])
                    elif (i < self.l1):
                        self.mix.append(self.out[i] + self.out1[i])
                    else:
                        self.mix.append(self.out[i])

            elif (self.l2 > self.l1):
                for i in range(self.l):
                    if (i < self.l1):
                        self.mix.append(
                            self.out[i] + self.out1[i] + self.out2[i])
                    elif (i < self.l2):
                        self.mix.append(self.out[i] + self.out2[i])
                    else:
                        self.mix.append(self.out[i])

        elif (self.l1 > self.l2 and self.l1 > self.l):
            final = self.l1
            if (self.l >= self.l2):
                for i in range(self.l1):
                    if (i < self.l2):
                        self.mix.append(
                            self.out[i] + self.out1[i] + self.out2[i])
                    elif (i < self.l):
                        self.mix.append(self.out[i] + self.out1[i])
                    else:
                        self.mix.append(self.out1[i])

            elif (self.l2 > self.l):
                for i in range(self.l1):
                    if (i < self.l):
                        self.mix.append(
                            self.out[i] + self.out1[i] + self.out2[i])
                    elif (i < self.l2):
                        self.mix.append(self.out1[i] + self.out2[i])
                    else:
                        self.mix.append(self.out1[i])

        elif (self.l2 >= self.l1 and self.l2 >= self.l):
            final = self.l2
            if (self.l >= self.l1):
                for i in range(self.l2):
                    if (i < self.l1):
                        self.mix.append(
                            self.out[i] + self.out1[i] + self.out2[i])
                    elif (i < self.l):
                        self.mix.append(self.out[i] + self.out2[i])
                    else:
                        self.mix.append(self.out2[i])

            elif (self.l1 > self.l):
                for i in range(self.l2):
                    if (i < self.l2):
                        self.mix.append(
                            self.out[i] + self.out1[i] + self.out2[i])
                    elif (i < self.l1):
                        self.mix.append(self.out1[i] + self.out2[i])
                    else:
                        self.mix.append(self.out2[i])
        return final

    def callback(self, instance):
        self.out = []
        amp = self.s1.value
        shift = self.s2.value
        scale = self.s3.value
        shift = (shift)
        scale = scale
        if (self.wave1 == ''):
            print "PLEASE SELECT A FILE"
            return
        w1 = wave.open(self.wave1, 'r')
        p = w1.getparams()
        self.f = p[3]
        arr = []
        if (w1.getsampwidth() == 2):
            fmt = "=h"
        else:
            fmt = "=B"
        integer_data = []
        for i in range(self.f):
            s = w1.readframes(1)
            integer_data = struct.unpack(fmt, s)[0]
            arr.append(int(integer_data))

        w = wave.open("output.wav", "wb")
        comptype = "NONE"
        compname = "not compressed"

        w.setparams((w1.getnchannels(), w1.getsampwidth(),
                    int(w1.getframerate()*scale), w1.getnframes(), comptype, compname))
        print p[1]
        print p[3]
        w1.close()
        for i in range(self.f):
            if ((arr[i]*amp <= 255 and arr[i]*amp >= 0 and fmt == "=B") or (fmt == "=h" and arr[i]*amp <= 32767 and arr[i] >= -32768)):
                self.out.append(int(arr[i]*amp))
            elif (arr[i]*amp >= 255 and fmt == "=B"):
                self.out.append(255)
            elif (arr[i]*amp >= 32767):
                self.out.append(32767)
            elif (arr[i]*amp <= -32768):
                self.out.append(-32768)
        if(self.flag1 == 1):
            self.out.reverse()
        if (shift > 0):
            self.l = self.f-(int(shift*p[2]))
        else:
            self.l = self.f+(int(shift*p[2]))
        for i in range(self.l):
            if (shift > 0):
                self.out[i] = self.out[i+(int(shift*p[2]))]

        if (self.flag3 == 1 and self.flag23 == 1 and self.flag13 == 1):
            if (self.l > self.l1 and self.l > self.l2):
                final = self.l
                if (self.l1 >= self.l2):
                    for i in range(self.l):
                        if (i < self.l2):
                            self.mix.append(
                                self.out[i] + self.out1[i] + self.out2[i])
                        elif (i < self.l1):
                            self.mix.append(self.out[i] + self.out1[i])
                        else:
                            self.mix.append(self.out[i])

                elif (self.l2 > self.l1):
                    for i in range(self.l):
                        if (i < self.l1):
                            self.mix.append(
                                self.out[i] + self.out1[i] + self.out2[i])
                        elif (i < self.l2):
                            self.mix.append(self.out[i] + self.out2[i])
                        else:
                            self.mix.append(self.out[i])

            elif (self.l1 > self.l2 and self.l1 > self.l):
                final = self.l1
                if (self.l >= self.l2):
                    for i in range(self.l1):
                        if (i < self.l2):
                            self.mix.append(
                                self.out[i] + self.out1[i] + self.out2[i])
                        elif (i < self.l):
                            self.mix.append(self.out[i] + self.out1[i])
                        else:
                            self.mix.append(self.out1[i])

                elif (self.l2 > self.l):
                    for i in range(self.l1):
                        if (i < self.l):
                            self.mix.append(
                                self.out[i] + self.out1[i] + self.out2[i])
                        elif (i < self.l2):
                            self.mix.append(self.out1[i] + self.out2[i])
                        else:
                            self.mix.append(self.out1[i])

            elif (self.l2 >= self.l1 and self.l2 >= self.l):
                final = self.l2
                if (self.l >= self.l1):
                    for i in range(self.l2):
                        if (i < self.l1):
                            self.mix.append(
                                self.out[i] + self.out1[i] + self.out2[i])
                        elif (i < self.l):
                            self.mix.append(self.out[i] + self.out2[i])
                        else:
                            self.mix.append(self.out2[i])

                elif (self.l1 > self.l):
                    for i in range(self.l2):
                        if (i < self.l2):
                            self.mix.append(
                                self.out[i] + self.out1[i] + self.out2[i])
                        elif (i < self.l1):
                            self.mix.append(self.out1[i] + self.out2[i])
                        else:
                            self.mix.append(self.out2[i])

        elif (self.flag3 == 1 and self.flag13 == 1):
            if (self.l >= self.l1):
                final = self.l
                print final,
                print "->final"
                for i in range(self.l):
                    if (i < self.l1):
                        print i
                        print self.out1[i]
                        self.mix.append(self.out1[i] + self.out[i])
                        print self.out1[i]+self.out[i]
                    else:
                        self.mix.append(self.out[i])
            else:
                final = self.l1
                for i in range(self.l1):
                    if (i < self.l):
                        self.mix.append(self.out1[i] + self.out[i])
                    else:
                        self.mix.append(self.out1[i])

        elif (self.flag3 == 1 and self.flag23 == 1):
            if (self.l >= self.l2):
                final = self.l
                for i in range(self.l):
                    if (i < self.l2):
                        print self.out[i],
                        self.mix.append(self.out2[i] + self.out[i])
                        print self.out2[i]+self.out[i]
                    else:
                        self.mix.append(self.out[i])
            else:
                final = self.l2
                for i in range(self.l2):
                    if (i < self.l):
                        self.mix.append(self.out2[i] + self.out[i])
                    else:
                        self.mix.append(self.out2[i])

        if (self.flag2 == 1 and self.flag22 == 1 and self.flag12 == 1):
            final = self.mod3()
        elif (self.flag2 == 1 and self.flag12 == 1):
            if (self.l >= self.l1):
                final = self.l
                print final,
                print "->final"
                for i in range(self.l):
                    if (i < self.l1):
                        self.mod.append(self.out1[i]*self.out[i])
                    else:
                        self.mod.append(self.out[i])
            else:
                final = self.l1
                for i in range(self.l1):
                    if (i < self.l):
                        self.mod.append((self.out1[i]*self.out[i]))
                    else:
                        self.mod.append(self.out1[i])

        elif (self.flag2 == 1 and self.flag22 == 1):
            if (self.l >= self.l2):
                final = self.l
                for i in range(self.l):
                    if (i < self.l2):
                        self.mod.append(self.out2[i]*self.out[i])
                    else:
                        self.mod.append(self.out[i])
            else:
                final = self.l2
                for i in range(self.l2):
                    if (i < self.l):
                        self.mod.append(self.out2[i]*self.out[i])
                    else:
                        self.mod.append(self.out2[i])

        if (self.flag3 != 1 and self.flag2 != 1):
            for i in range(self.l):
                if ((self.out[i] <= 255 and self.out[i] >= 0 and fmt == "=B") or (fmt == "=h" and self.out[i] <= 32767 and self.out[i] >= -32768)):
                    self.out[i] = self.out[i]
                elif (self.out[i] >= 255 and fmt == "=B"):
                    self.out[i] = (255)
                elif (self.out[i] >= 32767):
                    self.out[i] = (32767)
                elif (self.out[i] <= -32768):
                    self.out[i] = (-32768)

                w.writeframes(''.join(struct.pack(fmt, self.out[i])))
        elif (self.flag3 == 1 and self.flag2 != 1 and (self.flag13 == 1 or self.flag23 == 1)):
            for i in range(final):
                if ((self.mix[i] <= 255 and self.mix[i] >= 0 and fmt == "=B") or (fmt == "=h" and self.mix[i] <= 32767 and self.mix[i] >= -32768)):
                    self.mix[i] = self.mix[i]
                elif (self.mix[i] >= 255 and fmt == "=B"):
                    self.mix[i] = (255)
                elif (self.mix[i] >= 32767):
                    self.mix[i] = (32767)
                elif (self.mix[i] <= -32768):
                    self.mix[i] = (-32768)
                w.writeframes(''.join(struct.pack(fmt, self.mix[i])))
        elif (self.flag2 == 1 and (self.flag12 == 1 or self.flag22 == 1)):
            for i in range(final):
                if ((self.mod[i] <= 255 and self.mod[i] >= 0 and fmt == "=B") or (fmt == "=h" and self.mod[i] <= 32767 and self.mod[i] >= -32768)):
                    self.mod[i] = self.mod[i]
                elif (self.mod[i] >= 255 and fmt == "=B"):
                    self.mod[i] = (255)
                elif (self.mod[i] >= 32767):
                    print self.mod[i]
                    self.mod[i] = 32767
                elif (self.mod[i] <= -32768):
                    self.mod[i] = -32768
                w.writeframes(''.join(struct.pack(fmt, self.mod[i])))
        else:
            print "PLEASE SELECT TWO WAVES !!!!"
        w.close()
        self.sound1 = SoundLoader.load('output.wav')
        if self.sound1:
            self.sound1.play()

    def callback1(self, instance):
        self.out1 = []
        self.mix = []
        amp = self.s11.value
        print amp
        shift = self.s12.value
        scale = self.s13.value
        shift = (shift)
        scale = scale
        print shift
        if (self.wave2 == ''):
            print "PLEASE SELECT A FILE"
            return
        w1 = wave.open(self.wave2, 'r')
        p = w1.getparams()
        self.f1 = p[3]
        arr = []
        if (w1.getsampwidth() == 2):
            fmt = "=h"
        else:
            fmt = "=B"
        integer_data = []
        for i in range(self.f1):
            s = w1.readframes(1)
            integer_data = struct.unpack(fmt, s)[0]
            arr.append(int(integer_data))

        w = wave.open("output1.wav", "wb")
        comptype = "NONE"
        compname = "not compressed"

        w.setparams((w1.getnchannels(), w1.getsampwidth(),
                    int(w1.getframerate()*scale), w1.getnframes(), comptype, compname))
        print p[1]
        print p[3]
        w1.close()
        for i in range(self.f1):
            if ((arr[i]*amp <= 255 and arr[i]*amp >= 0 and fmt == "=B") or (fmt == "=h" and arr[i]*amp <= 32767 and arr[i] >= -32768)):
                self.out1.append(int(arr[i]*amp))
            elif (arr[i]*amp >= 255 and fmt == "=B"):
                self.out1.append(255)
            elif (arr[i]*amp >= 32767):
                self.out1.append(32767)
            elif (arr[i]*amp <= -32768):
                self.out1.append(-32768)
        if(self.flag11 == 1):
            self.out1.reverse()
        if (shift > 0):
            self.l1 = self.f1-(int(shift*p[2]))
        else:
            self.l1 = self.f1 + (int(shift*p[2]))
        print self.l1
        for i in range(self.l1):
            if (shift > 0):
                self.out1[i] = self.out1[i+(int(shift*p[2]))]

        if (self.flag3 == 1 and self.flag23 == 1 and self.flag13 == 1):
            final = self.mix3()

        elif (self.flag13 == 1 and self.flag3 == 1):
            if (self.l >= self.l1):
                final = self.l
                print final,
                print "->final"
                for i in range(self.l):
                    if (i < self.l1):
                        print i
                        self.mix.append(self.out1[i] + self.out[i])
                    else:
                        self.mix.append(self.out[i])
            else:
                final = self.l1
                for i in range(self.l1):
                    if (i < self.l):
                        self.mix.append(self.out1[i] + self.out[i])
                    else:
                        self.mix.append(self.out1[i])

        elif (self.flag13 == 1 and self.flag23 == 1):
            if (self.l1 >= self.l2):
                final = self.l1
                for i in range(self.l1):
                    if (i < self.l2):
                        self.mix.append(self.out1[i] + self.out2[i])
                    else:
                        self.mix.append(self.out1[i])
            else:
                final = self.l2
                for i in range(self.l2):
                    if (i < self.l1):
                        self.mix.append(self.out1[i] + self.out2[i])
                    else:
                        self.mix.append(self.out2[i])

        if (self.flag2 == 1 and self.flag22 == 1 and self.flag12 == 1):
            final = self.mod3()

        elif (self.flag2 == 1 and self.flag12 == 1):
            if (self.l >= self.l1):
                final = self.l
                print final,
                print "->final"
                for i in range(self.l):
                    if (i < self.l1):
                        self.mod.append(self.out1[i]*self.out[i])
                    else:
                        self.mod.append(self.out[i])
            else:
                final = self.l1
                for i in range(self.l1):
                    if (i < self.l):
                        self.mod.append((self.out1[i]*self.out[i]))
                    else:
                        self.mod.append(self.out1[i])

        elif (self.flag12 == 1 and self.flag22 == 1):
            if (self.l1 >= self.l2):
                final = self.l1
                for i in range(self.l1):
                    if (i < self.l2):
                        self.mod.append(self.out2[i]*self.out1[i])
                    else:
                        self.mod.append(self.out1[i])
            else:
                final = self.l2
                for i in range(self.l2):
                    if (i < self.l1):
                        self.mod.append(self.out2[i]*self.out1[i])
                    else:
                        self.mod.append(self.out2[i])

        if (self.flag13 != 1 and self.flag12 != 1):
            for i in range(self.l1):
                if ((self.out1[i] <= 255 and self.out1[i] >= 0 and fmt == "=B") or (fmt == "=h" and self.out1[i] <= 32767 and self.out1[i] >= -32768)):
                    self.out1[i] = self.out1[i]
                elif (self.out1[i] >= 255 and fmt == "=B"):
                    self.out1[i] = (255)
                elif (self.out1[i] >= 32767):
                    self.out1[i] = (32767)
                elif (self.out1[i] <= -32768):
                    self.out1[i] = (-32768)

                w.writeframes(''.join(struct.pack(fmt, self.out1[i])))
        elif (self.flag13 == 1 and self.flag12 != 1 and (self.flag3 == 1 or self.flag23 == 1)):
            for i in range(final):
                if ((self.mix[i] <= 255 and self.mix[i] >= 0 and fmt == "=B") or (fmt == "=h" and self.mix[i] <= 32767 and self.mix[i] >= -32768)):
                    self.mix[i] = self.mix[i]
                elif (self.mix[i] >= 255 and fmt == "=B"):
                    self.mix[i] = (255)
                elif (self.mix[i] >= 32767):
                    self.mix[i] = (32767)
                elif (self.mix[i] <= -32768):
                    self.mix[i] = (-32768)
                w.writeframes(''.join(struct.pack(fmt, self.mix[i])))
        elif (self.flag12 == 1 and (self.flag2 == 1 or self.flag22 == 1)):
            for i in range(final):
                if ((self.mod[i] <= 255 and self.mod[i] >= 0 and fmt == "=B") or (fmt == "=h" and self.mod[i] <= 32767 and self.mod[i] >= -32768)):
                    self.mod[i] = self.mod[i]
                elif (self.mod[i] >= 255 and fmt == "=B"):
                    self.mod[i] = (255)
                elif (self.mod[i] >= 32767):
                    print self.mod[i]
                    self.mod[i] = 32767
                elif (self.mod[i] <= -32768):
                    self.mod[i] = -32768
                w.writeframes(''.join(struct.pack(fmt, self.mod[i])))
        else:
            print "PLEASE SELECT TWO WAVES !!!!"

        w.close()
        self.sound2 = SoundLoader.load('output1.wav')
        if self.sound2:
            self.sound2.play()

    def callback2(self, instance):
        self.out2 = []
        self.mix = []
        amp = self.s21.value
        print amp
        shift = self.s22.value
        scale = self.s23.value
        shift = (shift)
        scale = scale
        if (self.wave3 == ''):
            print "PLEASE SELECT A FILE"
            return
        w1 = wave.open(self.wave3, 'r')
        p = w1.getparams()
        self.f2 = p[3]
        arr = []
        if (w1.getsampwidth() == 2):
            fmt = "=h"
        else:
            fmt = "=B"
        integer_data = []
        for i in range(self.f2):
            s = w1.readframes(1)
            integer_data = struct.unpack(fmt, s)[0]
            arr.append(int(integer_data))

        w = wave.open("output2.wav", "wb")
        comptype = "NONE"
        compname = "not compressed"

        w.setparams((w1.getnchannels(), w1.getsampwidth(),
                    int(w1.getframerate()*scale), w1.getnframes(), comptype, compname))
        print p[1]
        print p[3]
        w1.close()
        for i in range(self.f2):
            if ((arr[i]*amp <= 255 and arr[i]*amp >= 0 and fmt == "=B") or (fmt == "=h" and arr[i]*amp <= 32767 and arr[i] >= -32768)):
                self.out2.append(arr[i]*amp)
            elif (arr[i]*amp >= 255 and fmt == "=B"):
                self.out2.append(255)
            elif (arr[i]*amp >= 32767):
                self.out2.append(32767)
            elif (arr[i]*amp <= -32768):
                self.out2.append(-32768)
        if(self.flag21 == 1):
            self.out2.reverse()

        if (shift > 0):
            self.l2 = self.f2-(int(shift*p[2]))
        else:
            self.l2 = self.f2+(int(shift*p[2]))
        for i in range(self.l2):
            if (shift > 0):
                self.out2[i] = self.out2[i+(int(shift*p[2]))]

        if (self.flag3 == 1 and self.flag23 == 1 and self.flag13 == 1):
            final = self.mix3()
        elif (self.flag23 == 1 and self.flag3 == 1):
            if (self.l >= self.l2):
                final = self.l
                print final,
                print "->final"
                for i in range(self.l):
                    if (i < self.l2):
                        self.mix.append(self.out2[i] + self.out[i])
                    else:
                        self.mix.append(self.out[i])
            else:
                final = self.l1
                for i in range(self.l2):
                    if (i < self.l):
                        self.mix.append(self.out2[i] + self.out[i])
                    else:
                        self.mix.append(self.out2[i])

        elif (self.flag13 == 1 and self.flag23 == 1):
            if (self.l1 >= self.l2):
                final = self.l1
                for i in range(self.l1):
                    if (i < self.l2):
                        self.mix.append(self.out1[i] + self.out2[i])
                    else:
                        self.mix.append(self.out1[i])
            else:
                final = self.l2
                for i in range(self.l2):
                    if (i < self.l1):
                        self.mix.append(self.out1[i] + self.out2[i])
                    else:
                        self.mix.append(self.out2[i])

        if (self.flag2 == 1 and self.flag22 == 1 and self.flag12 == 1):
            final = self.mod3()
        elif (self.flag2 == 1 and self.flag22 == 1):
            if (self.l >= self.l2):
                final = self.l
                print final,
                print "->final"
                for i in range(self.l):
                    if (i < self.l2):
                        self.mod.append(self.out2[i]*self.out[i])
                    else:
                        self.mod.append(self.out[i])
            else:
                final = self.l2
                for i in range(self.l2):
                    if (i < self.l):
                        self.mod.append((self.out2[i]*self.out[i]))
                    else:
                        self.mod.append(self.out2[i])

        elif (self.flag12 == 1 and self.flag22 == 1):
            if (self.l1 >= self.l2):
                final = self.l1
                for i in range(self.l1):
                    if (i < self.l2):
                        self.mod.append(self.out2[i]*self.out1[i])
                    else:
                        self.mod.append(self.out1[i])
            else:
                final = self.l2
                for i in range(self.l2):
                    if (i < self.l1):
                        self.mod.append(self.out2[i]*self.out1[i])
                    else:
                        self.mod.append(self.out2[i])

        if (self.flag23 != 1 and self.flag22 != 1):
            for i in range(self.l2):
                if ((self.out2[i] <= 255 and self.out2[i] >= 0 and fmt == "=B") or (fmt == "=h" and self.out2[i] <= 32767 and self.out2[i] >= -32768)):
                    self.out2[i] = self.out2[i]
                elif (self.out2[i] >= 255 and fmt == "=B"):
                    self.out2[i] = (255)
                elif (self.out2[i] >= 32767):
                    self.out2[i] = (32767)
                elif (self.out2[i] <= -32768):
                    self.out2[i] = (-32768)

                w.writeframes(''.join(struct.pack(fmt, self.out2[i])))
        elif (self.flag23 == 1 and self.flag22 != 1):
            for i in range(final):
                if ((self.mix[i] <= 255 and self.mix[i] >= 0 and fmt == "=B") or (fmt == "=h" and self.mix[i] <= 32767 and self.mix[i] >= -32768)):
                    self.mix[i] = self.mix[i]
                elif (self.mix[i] >= 255 and fmt == "=B"):
                    self.mix[i] = (255)
                elif (self.mix[i] >= 32767):
                    self.mix[i] = (32767)
                elif (self.mix[i] <= -32768):
                    self.mix[i] = (-32768)
                w.writeframes(''.join(struct.pack(fmt, self.mix[i])))
        elif (self.flag22 == 1):
            for i in range(final):
                if ((self.mod[i] <= 255 and self.mod[i] >= 0 and fmt == "=B") or (fmt == "=h" and self.mod[i] <= 32767 and self.mod[i] >= -32768)):
                    self.mod[i] = self.mod[i]
                elif (self.mod[i] >= 255 and fmt == "=B"):
                    self.mod[i] = (255)
                elif (self.mod[i] >= 32767):
                    self.mod[i] = 32767
                elif (self.mod[i] <= -32768):
                    self.mod[i] = -32768
                w.writeframes(''.join(struct.pack(fmt, self.mod[i])))
        else:
            print "PLEASE SELECT TWO WAVES !!!!"

        w.close()
        self.sound3 = SoundLoader.load('output2.wav')
        if self.sound3:
            self.sound3.play()

    def master_scene(self):
        self.lay1 = BoxLayout(orientation='horizontal')
        self.display_scene(1)
        self.display_scene1(2)
        self.display_scene2(3)
        self.add_widget(self.lay1)

    def display_scene(self, x):
        layout = StackLayout(orientation='tb-lr')
        if (x == 2):
            main = Label(text='WAVE MIXER', size_hint=(1, 0.03),
                         color=(1, 0, 0, 1), background_color=(1, 0, 0, 1))
        else:
            main = Label(text='', size_hint=(1, 0.03),
                         color=(1, 0, 0, 1), background_color=(1, 0, 0, 1))
        label1 = Label(text='File '+str(x), size_hint=(1, 0.1))
        select1 = Button(text='Select file',
                         size_hint=(1, 0.05), background_color=(1, 0, 0, 1))
        select1.bind(on_press=self.selectSound1)
        bt1 = Button(text='Play file', size_hint=(1, 0.05),
                     background_color=(1, 0, 0, 1))
        bt1.bind(on_press=self.callback)
        stop1 = Button(text='Stop Playing', size_hint=(1, 0.05),
                       background_color=(1, 0, 0, 1))
        stop1.bind(on_press=self.stopf1)
        label2 = Label(text='Amplitude', size_hint=(1, 0.1))
        label3 = Label(text='Time Shift', size_hint=(1, 0.1))
        label4 = Label(text='Time Scaling', size_hint=(1, 0.1))
        self.flag1 = 0
        self.flag2 = 0
        self.flag3 = 0
        self.s1 = Slider(min=0.0, max=5.0, value=1.0,
                         size_hint=(0.8, 0.02), background_color=(1, 0, 0, 1))
        self.s2 = Slider(min=-1.0, max=1.0, value=0.5, size_hint=(0.8, 0.02))
        self.s3 = Slider(min=0.0, max=8.0, value=2.0, size_hint=(0.8, 0.02))

        self.c1 = CheckBox(size_hint=(0.8, 0.05))
        self.c2 = CheckBox(size_hint=(0.8, 0.05))
        self.c3 = CheckBox(size_hint=(0.8, 0.05))
        label5 = Label(text='Time Reversal', size_hint=(1, 0.02))
        label6 = Label(text='Select for modulation', size_hint=(1, 0.02))
        label7 = Label(text='Select for mixing', size_hint=(1, 0.02))
        self.c1.bind(active=self.on_checkbox_active1)
        self.c2.bind(active=self.on_checkbox_active2)
        self.c3.bind(active=self.on_checkbox_active3)
        layout.add_widget(main)
        layout.add_widget(label1)
        layout.add_widget(select1)
        layout.add_widget(bt1)
        layout.add_widget(stop1)
        layout.add_widget(label2)
        layout.add_widget(self.s1)
        layout.add_widget(label3)
        layout.add_widget(self.s2)
        layout.add_widget(label4)
        layout.add_widget(self.s3)
        layout.add_widget(self.c1)
        layout.add_widget(label5)
        layout.add_widget(self.c2)
        layout.add_widget(label6)
        layout.add_widget(self.c3)
        layout.add_widget(label7)
        self.s1.bind(value=self.update_value1)
        self.s2.bind(value=self.update_value2)
        self.s3.bind(value=self.update_value3)
        self.lay1.add_widget(layout)

    def update_value1(self, slider, value):
        if value != self.s1.value:
            self.s1.value = value

    def update_value2(self, slider, value):
        if value != self.s2.value:
            self.s2.value = value

    def update_value3(self, slider, value):
        if value != self.s3.value:
            self.s3.value = value

    def on_checkbox_active1(self, checkbox, value):
        if value:
            self.flag1 = 1
        else:
            self.flag1 = 0

    def on_checkbox_active2(self, checkbox, value):
        if value:
            self.flag2 = 1
        else:
            self.flag2 = 0

    def on_checkbox_active3(self, checkbox, value):
        if value:
            self.flag3 = 1
        else:
            self.flag3 = 0

    def selectSound1(self, instance):

        # create popup layout containing a boxLayout
        content = BoxLayout(orientation='vertical', spacing=5)
        self.popup = popup = Popup(
            title='Wave Mixer V1.0', content=content, size_hint=(None, None), size=(600, 400))

        # first, create the scrollView
        self.scrollView = scrollView = ScrollView()

        # then, create the fileChooser and integrate it in the scrollView
        self.fileChooser = fileChooser = FileChooserListView(
            size_hint_y=None, path='/home/')
        fileChooser.bind(on_submit=self._validate1)
        fileChooser.height = 1500
        scrollView.add_widget(fileChooser)

        # construct the content, widget are used as a spacer
        content.add_widget(Widget(size_hint_y=None, height=5))
        content.add_widget(scrollView)
        content.add_widget(Widget(size_hint_y=None, height=5))

        # 2 buttons are created for accept or cancel the current value
        btnlayout = BoxLayout(size_hint_y=None, height=50, spacing=5)
        btn = Button(text='Ok')
        btn.bind(on_press=partial(self._validate1, fileChooser))
        btnlayout.add_widget(btn)

        btn = Button(text='Cancel')
        btn.bind(on_release=popup.dismiss)
        btnlayout.add_widget(btn)
        content.add_widget(btnlayout)

        # all done, open the popup !
        popup.open()

    def selectSound2(self, instance):

        # create popup layout containing a boxLayout
        content = BoxLayout(orientation='vertical', spacing=5)
        self.popup = popup = Popup(
            title='Wave Mixer V1.0', content=content, size_hint=(None, None), size=(600, 400))

        # first, create the scrollView
        self.scrollView = scrollView = ScrollView()

        # then, create the fileChooser and integrate it in the scrollView
        self.fileChooser = fileChooser = FileChooserListView(
            size_hint_y=None, path='/home/')
        fileChooser.bind(on_submit=self._validate2)
        fileChooser.height = 1500  # this is a bit ugly...
        scrollView.add_widget(fileChooser)

        # construct the content, widget are used as a spacer
        content.add_widget(Widget(size_hint_y=None, height=5))
        content.add_widget(scrollView)
        content.add_widget(Widget(size_hint_y=None, height=5))

        # 2 buttons are created for accept or cancel the current value
        btnlayout = BoxLayout(size_hint_y=None, height=50, spacing=5)
        btn = Button(text='Ok')
        btn.bind(on_press=partial(self._validate2, fileChooser))
        btnlayout.add_widget(btn)

        btn = Button(text='Cancel')
        btn.bind(on_release=popup.dismiss)
        btnlayout.add_widget(btn)
        content.add_widget(btnlayout)

        # all done, open the popup !
        popup.open()

    def selectSound3(self, instance):

        # create popup layout containing a boxLayout
        content = BoxLayout(orientation='vertical', spacing=5)
        self.popup = popup = Popup(
            title='Wave Mixer V1.0', content=content, size_hint=(None, None), size=(600, 400))

        # first, create the scrollView
        self.scrollView = scrollView = ScrollView()

        # then, create the fileChooser and integrate it in the scrollView
        self.fileChooser = fileChooser = FileChooserListView(
            size_hint_y=None, path='/home/')
        fileChooser.bind(on_submit=self._validate3)
        fileChooser.height = 1500
        scrollView.add_widget(fileChooser)

        # construct the content, widget are used as a spacer
        content.add_widget(Widget(size_hint_y=None, height=5))
        content.add_widget(scrollView)
        content.add_widget(Widget(size_hint_y=None, height=5))

        # 2 buttons are created for accept or cancel the current value
        btnlayout = BoxLayout(size_hint_y=None, height=50, spacing=5)
        btn = Button(text='Ok')
        btn.bind(on_press=partial(self._validate3, fileChooser))
        btnlayout.add_widget(btn)

        btn = Button(text='Cancel')
        btn.bind(on_release=popup.dismiss)
        btnlayout.add_widget(btn)
        content.add_widget(btnlayout)

        # all done, open the popup !
        popup.open()

    def _validate1(self, fileChooser, selected):

        value = fileChooser.selection
        self.popup.dismiss()
        self.popup = None

        # if the value was empty, don't change anything.

        if value == '':
            # do what you would do if the user didn't select any file
            return
        else:
            value = str(value)
            x = value.split('/')
            x = x[len(x) - 1]
            inputFile = x.split('\'')[0]
            y = inputFile.split('.')
            if(y[1] != 'wav'):
                exit(0)
            else:
                self.wave1 = inputFile

    def stopf1(self, instance):
        self.sound1 = self.sound1.stop()

    def stopf2(self, instance):
        self.sound2 = self.sound2.stop()

    def stopf3(self, instance):
        self.sound3 = self.sound3.stop()

    def _validate2(self, fileChooser, selected):

        value = fileChooser.selection
        self.popup.dismiss()
        self.popup = None

        # if the value was empty, don't change anything.

        if value == '':
            # do what you would do if the user didn't select any file
            return
        else:
            value = str(value)
            x = value.split('/')
            x = x[len(x) - 1]
            inputFile = x.split('\'')[0]
            y = inputFile.split('.')
            if(y[1] != 'wav'):
                exit(0)
            else:
                print "Selected!"
                self.wave2 = inputFile

    def _validate3(self, fileChooser, selected):

        value = fileChooser.selection
        self.popup.dismiss()
        self.popup = None

        # if the value was empty, don't change anything.

        if value == '':
            # do what you would do if the user didn't select any file
            return
        else:
            value = str(value)
            x = value.split('/')
            x = x[len(x) - 1]
            inputFile = x.split('\'')[0]
            y = inputFile.split('.')
            if(y[1] != 'wav'):
                exit(0)
            else:
                print "reached"
                self.wave3 = inputFile

    def record(self, instance):
        # Records whatever you say for 7 sec!"
        chunk = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100
        RECORD_SECONDS = 7
        new = pyaudio.PyAudio()
        s = new.open(
            format=FORMAT, channels=CHANNELS, rate=RATE, input=True, output=True, frames_per_buffer=chunk)
        print "Recording Started! Will record till 7 sec. Please be closer to your microphone and be loud."
        for i in range(0, 44100 / chunk * RECORD_SECONDS):
            data = s.read(chunk)
            self.rarr.append(data)
        wavefile = wave.open("rec.wav", 'wb')
        # rec.wav output file is created.
        wavefile.setnchannels(CHANNELS)
        wavefile.setsampwidth(new.get_sample_size(FORMAT))
        wavefile.setframerate(RATE)
        wavefile.writeframes(b''.join(self.rarr))
        wavefile.close()
        print "Recording Complete"
        s.stop_stream()
        s.close()
        new.terminate()
        return

    def display_scene1(self, x):
        layout1 = StackLayout(orientation='tb-lr')
        if (x == 2):
            main = Label(text='WAVE MIXER', size_hint=(1, 0.03),
                         color=(1, 0, 0, 1), bold=True, background_color=(1, 0, 0, 1))
        else:
            main = Label(text='', size_hint=(1, 0.03),
                         color=(1, 0, 0, 1), background_color=(1, 0, 0, 1))
        label11 = Label(text='File '+str(x), size_hint=(1, 0.1))
        main1 = Label(text='', size_hint=(1, 0.04))
        bt11 = Button(text='Play file', size_hint=(1, 0.05),
                      background_color=(1, 0, 0, 1))
        bt11.bind(on_press=self.callback1)
        select2 = Button(text='Select file',
                         size_hint=(1, 0.05), background_color=(1, 0, 0, 1))
        select2.bind(on_press=self.selectSound2)
        recordb = Button(text='Record File',
                         size_hint=(1, 0.05), background_color=(0, 1, 1, 1))
        recordb.bind(on_press=self.record)
        stop2 = Button(text='Stop Playing', size_hint=(1, 0.05),
                       background_color=(1, 0, 0, 1))
        stop2.bind(on_press=self.stopf2)
        label12 = Label(text='Amplitude', size_hint=(1, 0.1))
        label13 = Label(text='Time Shift', size_hint=(1, 0.1))
        label14 = Label(text='Time Scaling', size_hint=(1, 0.1))
        self.flag11 = 0
        self.flag12 = 0
        self.flag13 = 0
        self.s11 = Slider(min=0.0, max=5.0, value=1.0,
                          size_hint=(0.8, 0.02), background_color=(1, 0, 0, 1))
        self.s12 = Slider(min=-1.0, max=1.0, value=0.5, size_hint=(0.8, 0.02))
        self.s13 = Slider(min=0.0, max=8.0, value=2.0, size_hint=(0.8, 0.02))

        self.c11 = CheckBox(size_hint=(0.8, 0.05))
        self.c12 = CheckBox(size_hint=(0.8, 0.05))
        self.c13 = CheckBox(size_hint=(0.8, 0.05))
        label15 = Label(text='Time Reversal', size_hint=(1, 0.02))
        label16 = Label(text='Select for modulation', size_hint=(1, 0.02))
        label17 = Label(text='Select for mixing', size_hint=(1, 0.02))
        self.c11.bind(active=self.on_checkbox1_active1)
        self.c12.bind(active=self.on_checkbox1_active2)
        self.c13.bind(active=self.on_checkbox1_active3)
        layout1.add_widget(main)
        layout1.add_widget(label11)
        layout1.add_widget(select2)
        layout1.add_widget(bt11)
        layout1.add_widget(stop2)
        layout1.add_widget(label12)
        layout1.add_widget(self.s11)
        layout1.add_widget(label13)
        layout1.add_widget(self.s12)
        layout1.add_widget(label14)
        layout1.add_widget(self.s13)
        layout1.add_widget(self.c11)
        layout1.add_widget(label15)
        layout1.add_widget(self.c12)
        layout1.add_widget(label16)
        layout1.add_widget(self.c13)
        layout1.add_widget(label17)
        layout1.add_widget(main1)
        layout1.add_widget(recordb)
        self.s11.bind(value=self.update1_value1)
        self.s12.bind(value=self.update1_value2)
        self.s13.bind(value=self.update1_value3)
        self.lay1.add_widget(layout1)

    def update1_value1(self, slider, value):
        if value != self.s11.value:
            self.s11.value = value

    def update1_value2(self, slider, value):
        if value != self.s12.value:
            self.s12.value = value

    def update1_value3(self, slider, value):
        if value != self.s13.value:
            self.s13.value = value

    def on_checkbox1_active1(self, checkbox, value):
        if value:
            self.flag11 = 1
        else:
            self.flag11 = 0

    def on_checkbox1_active2(self, checkbox, value):
        if value:
            self.flag12 = 1
        else:
            self.flag12 = 0

    def on_checkbox1_active3(self, checkbox, value):
        if value:
            self.flag13 = 1
        else:
            self.flag13 = 0

    def display_scene2(self, x):
        layout2 = StackLayout(orientation='tb-lr')
        if (x == 2):
            main = Label(text='WAVE MIXER',
                         size_hint=(1, 0.03), color=(1, 0, 0, 1))
        else:
            main = Label(text='', size_hint=(1, 0.03),
                         color=(1, 0, 0, 1), background_color=(1, 0, 0, 1))
        label21 = Label(text='File '+str(x), size_hint=(1, 0.1))
        bt21 = Button(text='Play file', size_hint=(1, 0.05),
                      background_color=(1, 0, 0, 1))
        bt21.bind(on_press=self.callback2)
        stop3 = Button(text='Stop Playing', size_hint=(1, 0.05),
                       background_color=(1, 0, 0, 1))
        stop3.bind(on_press=self.stopf3)
        select3 = Button(text='Select file',
                         size_hint=(1, 0.05), background_color=(1, 0, 0, 1))
        select3.bind(on_press=self.selectSound3)
        label22 = Label(text='Amplitude', size_hint=(1, 0.1))
        label23 = Label(text='Time Shift', size_hint=(1, 0.1))
        label24 = Label(text='Time Scaling', size_hint=(1, 0.1))
        self.flag21 = 0
        self.flag22 = 0
        self.flag23 = 0
        self.s21 = Slider(min=0.0, max=5.0, value=1.0,
                          size_hint=(0.8, 0.02), background_color=(1, 0, 0, 1))
        self.s22 = Slider(min=-1.0, max=1.0, value=0.5, size_hint=(0.8, 0.02))
        self.s23 = Slider(min=0.0, max=8.0, value=2.0, size_hint=(0.8, 0.02))

        self.c21 = CheckBox(size_hint=(0.8, 0.05))
        self.c22 = CheckBox(size_hint=(0.8, 0.05))
        self.c23 = CheckBox(size_hint=(0.8, 0.05))
        label25 = Label(text='Time Reversal', size_hint=(1, 0.02))
        label26 = Label(text='Select for modulation', size_hint=(1, 0.02))
        label27 = Label(text='Select for mixing', size_hint=(1, 0.02))
        self.c21.bind(active=self.on_checkbox2_active1)
        self.c22.bind(active=self.on_checkbox2_active2)
        self.c23.bind(active=self.on_checkbox2_active3)
        layout2.add_widget(main)
        layout2.add_widget(label21)
        layout2.add_widget(select3)
        layout2.add_widget(bt21)
        layout2.add_widget(stop3)
        layout2.add_widget(label22)
        layout2.add_widget(self.s21)
        layout2.add_widget(label23)
        layout2.add_widget(self.s22)
        layout2.add_widget(label24)
        layout2.add_widget(self.s23)
        layout2.add_widget(self.c21)
        layout2.add_widget(label25)
        layout2.add_widget(self.c22)
        layout2.add_widget(label26)
        layout2.add_widget(self.c23)
        layout2.add_widget(label27)
        self.s21.bind(value=self.update2_value1)
        self.s22.bind(value=self.update2_value2)
        self.s23.bind(value=self.update2_value3)
        self.lay1.add_widget(layout2)

    def update2_value1(self, slider, value):
        if value != self.s21.value:
            self.s21.value = value

    def update2_value2(self, slider, value):
        if value != self.s22.value:
            self.s22.value = value

    def update2_value3(self, slider, value):
        if value != self.s23.value:
            self.s23.value = value

    def on_checkbox2_active1(self, checkbox, value):
        if value:
            self.flag21 = 1
        else:
            self.flag21 = 0

    def on_checkbox2_active2(self, checkbox, value):
        if value:
            self.flag22 = 1
        else:
            self.flag22 = 0

    def on_checkbox2_active3(self, checkbox, value):
        if value:
            self.flag23 = 1
        else:
            self.flag23 = 0

    def __init__(self, **kwargs):
        super(MyWave, self).__init__(**kwargs)
        # initializing all values. Tiresome but no option!!!
        self.l = 0
        self.l1 = 0
        self.l2 = 0
        self.f1 = 0
        self.f = 0
        self.f2 = 0
        self.sound1 = ''
        self.sound2 = ''
        self.sound3 = ''
        self.out = []
        self.out1 = []
        self.mix = []
        self.mod = []
        self.out2 = []
        self.rarr = []
        self.wave1 = ''
        self.wave2 = ''
        self.wave3 = ''
        self.master_scene()
    pass


class MyApp(App):
    title = 'Wave Mixer'

    def build(self):
        return MyWave()

if __name__ == '__main__':
    MyApp().run()
