import serial
import string
import tkinter as tk
import threading
import sys
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import(FigureCanvasTkAgg, NavigationToolbar2Tk)

sensorValue = " "
voltageValue = 0.0
ser = serial.Serial('/dev/ttyACM0')

def sensing():
    while True:
        sensorValue = ser.readline()
        sensorValue = sensorValue.decode('utf-8').strip()
        print(sensorValue)
        voltageValue = int(sensorValue) * (5.0/1023.0)
        print("Voltage: " + str(round(voltageValue, 4)) + " Volts")

        cmDistance = 2*(10650.08 * pow(int(sensorValue),-0.935) - 10)
        print("Distance: " + str(round(cmDistance, 4)) + " cm")

        mmDistance = cmDistance * 10
        print("Distance: " + str(round(mmDistance, 4)) + " mm")

        inchDistance = cmDistance / 2.54
        print("Distance: " + str(round(inchDistance, 4)) + " inches")

        print(" ")

t1 = threading.Thread(target=sensing)
t1.daemon = True
t1.start()

root = tk.Tk()

userFrame = tk.LabelFrame(root, padx=0, pady=0)
userFrame.pack()

def startClick():
    print("start!")

def stopClick():
    print("stop!")

def recordClick():
    print("record!")

startButton = tk.Button(userFrame, text="Start", width=7, height=2, bg="green", command=startClick)
startButton.grid(row=0, column=0, padx=12)
stopButton = tk.Button(userFrame, text="Stop", width=7, height=2, bg="red", command=stopClick)
stopButton.grid(row=0, column=1, padx=12)
recordButton = tk.Button(userFrame, text="Record", width=7, height=2, bg="grey", command=recordClick)
recordButton.grid(row=0, column=2, padx=12)

distFrame = tk.LabelFrame(root, padx=20, pady=0)
distFrame.pack()

clicked = tk.StringVar(distFrame)
clicked.set("cm  ")
measureOptions = tk.OptionMenu(distFrame, clicked, "cm  ", "mm ", "inch")
measureOptions.grid(row=0, column=0)

distFrame2 = tk.LabelFrame(distFrame, padx=50, pady=0)
distFrame2.grid(row=0, column=1)

distValue = tk.Label(distFrame2, width=7, text="--", padx=10)
distValue.grid(row=0, column=0)

distUnit = tk.Label(distFrame2, width=3, textvariable=clicked, padx=10)
distUnit.grid(row=0, column = 1)

graphFrame = tk.LabelFrame(root)
graphFrame.pack(expand=True)

fig = Figure(figsize=(5,4), dpi=100)
fig.add_subplot(111).plot([1,2,3], [4,5,1])

canvas = FigureCanvasTkAgg(fig, master=graphFrame)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

root.geometry("380x280") # root.geometry("320x240")
root.mainloop()

sys.exit()
