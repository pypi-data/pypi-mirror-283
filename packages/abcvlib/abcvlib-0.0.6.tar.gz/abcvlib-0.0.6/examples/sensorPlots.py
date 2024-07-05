# -*- coding: utf-8 -*-
import sys
import threading
from multiprocessing import Process, Queue

import numpy as np
import pyqtgraph as pg
from PyQt5 import QtCore, QtGui, QtWidgets

from abcvlibserver.abcvlibserver import Message, Server, Response
# This function is responsible for displaying the data
# it is run in its own process to liberate main process
from jp.oist.abcvlib.core.learning.fbclasses.Episode import Episode


def display(count, q):

    app = QtWidgets.QApplication(sys.argv)

    fontHuge = QtGui.QFont()
    fontHuge.setPixelSize(40)
    fontLarge = QtGui.QFont()
    fontLarge.setPixelSize(40)
    fontMed = QtGui.QFont()
    fontMed.setPixelSize(20)

    red = pg.mkPen(255, 0, 0)
    red_light = pg.mkPen(255, 0, 0, 50)
    green = pg.mkPen(0, 255, 0)
    green_light = pg.mkPen(0, 255, 0, 50)
    blue = pg.mkPen(0, 0, 255)
    blue_light = pg.mkPen(0, 0, 50)

    view = pg.GraphicsView()
    l = pg.GraphicsLayout(border=(100, 100, 100))
    view.setCentralItem(l)
    view.show()
    view.setWindowTitle('Sensor Plots')

    l2 = l.addLayout(border=(50, 0, 0), colspan=3)

    ## Add 3 plots into the first row (automatic position)
    p1 = l2.addPlot(title="Theta")
    p1.setLabel('bottom', "Samples")
    p1.setLabel('left', "Deg")
    p1.addLegend()

    p2 = l2.addPlot(title="Angular Velocity")
    p2.addLegend()
    p2.setLabel('bottom', "Samples")
    p2.setLabel('left', "Deg/s")

    l.nextRow()

    l3 = l.addLayout(border=(50, 0, 0), colspan=3)

    p3 = l3.addPlot(title="Wheel Encoder Count")
    p3.addLegend()
    p3.setLabel('bottom', "Samples")
    p3.setLabel('left', "Count")

    p4 = l3.addPlot(title="Wheel Distance Traveled")
    p4.addLegend()
    p4.setLabel('bottom', "Samples")
    p4.setLabel('left', "mm?")

    p5 = l3.addPlot(title="Wheel Speed")
    p5.addLegend()
    p5.setLabel('bottom', "Samples")
    p5.setLabel('left', "mm/s ?")
    p5.getViewBox().setYRange(-200, 200)

    theta_curve = p1.plot(pen='y', name='Theta')
    angularVel_curve = p2.plot(pen='y', name='Angular Velocity')
    encoderCountL_curve = p3.plot(pen='r', name='Left')
    encoderCountR_curve = p3.plot(pen='b', name='Right')
    wheelDistanceL_curve = p4.plot(pen='r', name='Left')
    wheelDistanceR_curve = p4.plot(pen='b', name='Right')
    wheelSpeedL_curve = p5.plot(pen=red_light, name='Left')
    wheelSpeedR_curve = p5.plot(pen=blue_light, name='Right')
    wheelSpeedL_LP_curve = p5.plot(pen=red, name='LeftLP')
    wheelSpeedR_LP_curve = p5.plot(pen=blue, name='RightLP')

    window = 10000
    samples = np.zeros(shape=(window))
    theta = np.zeros(shape=window)
    thetadot = np.zeros(shape=window)
    wheelCount = np.zeros(shape=(2,window))
    wheelDistance = np.zeros(shape=(2,window))
    wheelSpeed = np.zeros(shape=(2,window))
    wheelSpeedLP = np.zeros(shape=(2,window))


    def updateData(q: Queue):
        global count
        count += 1
        item: Episode
        item = q.get()
        samples[:-1] = samples[1:]
        theta[:-1] = theta[1:]
        thetadot[:-1] = thetadot[1:]
        wheelCount[:,:-1] = wheelCount[:,1:]
        wheelDistance[:,:-1] = wheelDistance[:,1:]
        wheelSpeed[:,:-1] = wheelSpeed[:,1:]
        wheelSpeedLP[:,:-1] = wheelSpeedLP[:,1:]
        samples[-1] = count
        theta[-1] = item.Timesteps(0).OrientationData().Tiltangle(item.Timesteps(0).OrientationData().TiltangleLength() - 1) * (180 / 3.14159)
        thetadot[-1] = item.Timesteps(0).OrientationData().Tiltvelocity(item.Timesteps(0).OrientationData().TiltvelocityLength() - 1) * (180 / 3.14159)
        wheelCount[:,-1] = item.Timesteps(0).WheelData().Left().Counts(item.Timesteps(0).WheelData().Left().CountsLength() - 1)
        wheelDistance[:,-1] = item.Timesteps(0).WheelData().Left().Distances(item.Timesteps(0).WheelData().Left().DistancesLength() - 1)
        wheelSpeed[:,-1] = item.Timesteps(0).WheelData().Left().SpeedsBuffered(item.Timesteps(0).WheelData().Left().SpeedsBufferedLength() - 1)
        wheelSpeedLP[:,-1] = item.Timesteps(0).WheelData().Left().SpeedsExpavg(item.Timesteps(0).WheelData().Left().SpeedsExpavgLength() - 1)

    def updateCurves():

        theta_curve.setData(samples, theta)
        angularVel_curve.setData(samples, thetadot)
        encoderCountL_curve.setData(samples, wheelCount[0])
        encoderCountR_curve.setData(samples, wheelCount[1])
        wheelDistanceL_curve.setData(samples, wheelDistance[0])
        wheelDistanceR_curve.setData(samples, wheelDistance[1])
        wheelSpeedL_curve.setData(samples, wheelSpeed[0])
        wheelSpeedR_curve.setData(samples, wheelSpeed[1])
        wheelSpeedL_LP_curve.setData(samples, wheelSpeedLP[0])
        wheelSpeedR_LP_curve.setData(samples, wheelSpeedLP[1])

    timer = QtCore.QTimer()
    timer.timeout.connect(lambda: updateCurves())
    timer.start(5)

    timer2 = QtCore.QTimer()

    timer2.timeout.connect(lambda: updateData(q))
    timer2.start(5)

    QtWidgets.QApplication.instance().exec_()


def startServer(run: threading.Event, q: Queue):

    class MyMessage(Message):
        def _on_episode_received(self, episode: Episode):
            q.put(episode)
            super()._on_episode_received(episode)

        def _on_response_request(self):
            response = Response().default()
            return response

    server = Server(MyMessage)
    server.start()


if __name__ == '__main__':
    count = 0
    q = Queue()
    # Event for stopping the IO thread
    run = threading.Event()
    run.set()

    # Start display process
    gui = Process(target=display, args=(count, q))
    gui.start()

    serverThread = threading.Thread(target=startServer, args=(run, q), daemon=True)
    serverThread.start()

    input("See ? Main process immediately free ! Type any key to quit.")
    run.clear()
    print("Waiting for graph window process to join...")
    gui.join()
    print("Process joined successfully. C YA !")