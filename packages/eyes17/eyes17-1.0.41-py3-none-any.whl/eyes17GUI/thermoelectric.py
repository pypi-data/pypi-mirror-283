# -*- coding: utf-8; mode: python; indent-tabs-mode: t; tab-width:4 -*-
'''
Code for science experiments using expEYES-17 interface
Logs data from thermocouple sensor MAX6675

And EMF from ADS1115

for thermoelectric experiment

'''

import sys, time, math, os.path

from . import utils
from .QtVersion import *

import sys, time, functools
from .utils import pg
import numpy as np

from .layouts import ui_thermoelectric

from .layouts.gauge import Gauge

from . eyes17 import eyemath17 as em
from .layouts.advancedLoggerTools import LOGGER
from eyes17.SENSORS import ADS1115


class Expt(QtWidgets.QWidget, ui_thermoelectric.Ui_Form):
    TIMER = 10  #Every 10 mS
    running = True
    TMAX = 120
    RESET = 0
    ACTIVE = 1
    PAUSED = 2
    ADC = None

    def __init__(self, device=None):
        super(Expt, self).__init__()
        self.datapoints = 0
        self.state = self.RESET
        self.recording = False
        self.setupUi(self)

        self.p = device  # connection to the device hardware
        self.logger = LOGGER(self.p.I2C)

        colors = ['#00ffff', '#008080', '#ff0000', '#800000', '#ff00ff', '#800080', '#00FF00', '#008000', '#ffff00',
                  '#808000', '#0000ff', '#000080', '#a0a0a4', '#808080', '#ffffff', '#4000a0']
        labelStyle = {'color': 'rgb(200,250,200)', 'font-size': '12pt'}
        self.graph.setLabel('left', 'Thermo EMF -->', units='V', **labelStyle)
        self.graph.setLabel('bottom', 'Hot Junction Temperature -->', units='C', **labelStyle)

        self.valueTable.setHorizontalHeaderLabels(['Temperature', 'EMF(mV)'])
        '''
		item = QtWidgets.QTableWidgetItem()
		self.valueTable.setItem(0, pos, item)
		item.setText('')
		'''
        self.start_time = time.time()
        row = 1;
        col = 1;

        self.Tgauge = Gauge(self, 'Temp')
        self.Tgauge.setObjectName('T')
        self.Tgauge.set_MinValue(0)
        self.Tgauge.set_MaxValue(100)
        self.gaugeLayout.addWidget(self.Tgauge, 1, 1)

        self.emfgauge = Gauge(self, 'EMF(mV)')
        self.emfgauge.setObjectName('EMF')
        self.emfgauge.set_MinValue(0)
        self.emfgauge.set_MaxValue(3)
        self.gaugeLayout.addWidget(self.emfgauge, 1, 2)

        self.curve = self.graph.plot(pen=colors[0], connect="finite")
        self.fitcurve = self.graph.plot(pen=colors[1], width=2, connect="finite")

        self.graph.setRange(xRange=[0, 100])
        self.region = pg.LinearRegionItem()
        self.region.setBrush([255, 0, 50, 50])
        self.region.setZValue(10)
        for a in self.region.lines: a.setCursor(QtGui.QCursor(QtCore.Qt.SizeHorCursor));
        self.graph.addItem(self.region, ignoreBounds=False)
        self.region.setRegion([30, 80])

        self.TData = np.empty(500)
        self.EMFData = np.empty(500)

        self.locateADS1115()
        self.lastT = 200

        self.startTime = time.time()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updateEverything)
        self.timer.start(self.TIMER)
        self.setTheme("default")

    def setTheme(self, theme):
        self.setStyleSheet("")
        path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'layouts', 'themes')
        self.setStyleSheet(open(os.path.join(path, theme + ".qss"), "r").read())

    def recover(self):
        self.logger = LOGGER(self.p.I2C)
        print('recover', self.p.connected)
        self.locateADS1115()

    def locateADS1115(self):
        ## Search for ADS1115
        self.ADC = None
        x = self.logger.I2CScan()
        self.msg('ADS1115 not found')
        self.msgwin.setStyleSheet('color:darkred;')
        for a in x:
            possiblesensors = self.logger.sensormap.get(a, None)
            if 'ADS1115' in possiblesensors:
                self.msg('ADS1115 located at: %s' % a)
                self.msgwin.setStyleSheet('color:black;')
                self.ADC = ADS1115.connect(self.p.I2C)  # Measure the ADC
                self.ADC.setGain('GAIN_SIXTEEN')  # options : 'GAIN_TWOTHIRDS','GAIN_ONE','GAIN_TWO','GAIN_FOUR','GAIN_EIGHT','GAIN_SIXTEEN'

    # Define the function to mesaure the temperature
    def temperature(self):
        #Written by Ujjwal Nikam, NSHE
        """Function to measure the instanteneous temperature"""
        R0 = 1000  # PT1000 (RTD Name)
        Alpha = 3.85 / 1000  # Temperature coefficient
        t0 = time.time()  # Time initialization
        n = 1  # NO of measurements for averaging
        Rsum = 0
        for x in range(0, n):  # Loop for averaging
            r = self.p.get_resistance()  # Measure the resistance in ohm
            if r == np.inf:
                return False
            Rsum = Rsum + r  # Sum of resistance
        R = Rsum / n  # Average resistance
        T = (1 / Alpha) * ((R / R0) - 1)  # Calculate Temperature from Resistance
        return T

    def updateEverything(self):
        if not self.p.connected:
            return

        #self.setTheme("default")
        '''
        #Temperature from MAX6675
        self.p.SPI.start('CS1')
        val = self.p.SPI.send16(0xFFFF)
        self.p.SPI.stop('CS1')
        temp = (val >> 3) * 0.25
        if (val & 0x4):
            self.msg(self.tr('thermocouple not attached. : ') + str(val))
            return
        '''
        #Temperature from PT1000
        temp = self.temperature()
        if temp == False:
            self.msg(self.tr('PT1000 not connected between SEN and GND'))
            self.Tgauge.update_value(0)
            self.Tgauge.set_enable_filled_Polygon(False)
            return
        elif temp > 500:
            self.msg(self.tr('PT1000 value too high. check connections'))
            self.Tgauge.update_value(100)
            self.Tgauge.set_enable_filled_Polygon(False)
            return
        else:
            self.Tgauge.set_enable_filled_Polygon()
            self.Tgauge.update_value(temp)

        if self.ADC is None:
            self.msg(self.tr('ADS1115 not found. check connections  . chan:'+str(self.adsBox.currentIndex())))
            emf = 0
            self.emfgauge.set_enable_filled_Polygon(False)
            self.emfgauge.update_value(0)
        else:
            if self.adsBox.currentIndex() < 4:
                emf = self.ADC.readADC_SingleEnded(self.adsBox.currentIndex())  # ADC reading in Channel Ax
            elif self.adsBox.currentIndex() == 4:
                emf = self.ADC.readADC_Differential('01')  # ADC reading differential b/w 0 and 1
            else:
                emf = self.ADC.readADC_Differential('23')  # ADC between 2 and 3
            self.emfgauge.set_enable_filled_Polygon()
            self.emfgauge.update_value(emf)

        if self.ADC is not None:
            self.msg(self.tr('Temp: ') + '%.2f' % (temp) + ', ' + self.tr('EMF: ') + '%.3f' % (emf))

        if self.state == self.ACTIVE:
            if abs(temp - self.lastT) >= self.intervalBox.value() and (-10 < temp < 200):
                self.valueTable.setRowCount(self.datapoints + 1)
                self.lastT = temp
                #Temperature
                item = self.valueTable.item(self.datapoints, 0)
                if item is None:
                    item = QtWidgets.QTableWidgetItem()
                    self.valueTable.setItem(self.datapoints, 0, item)
                item.setText('%.3f' % temp)

                #EMF
                item = self.valueTable.item(self.datapoints, 1)
                if item is None:
                    item = QtWidgets.QTableWidgetItem()
                    self.valueTable.setItem(self.datapoints, 1, item)
                item.setText('%.3f' % (emf))
                self.valueTable.scrollToBottom()

                self.TData[self.datapoints] = temp
                self.EMFData[self.datapoints] = emf
                self.datapoints += 1
                self.curve.setData(self.TData[:self.datapoints], self.EMFData[:self.datapoints])

    def toggleLogging(self):
        icon = QtGui.QIcon()

        if self.state == self.RESET:  #Was off. start recording data
            self.lastT = 200
            self.state = self.ACTIVE
            self.logButton.setText(self.tr('PAUSE MEASUREMENTS'))
            icon.addPixmap(QtGui.QPixmap(":/control/stop.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        elif self.state == self.ACTIVE:
            self.state = self.PAUSED
            self.logButton.setText(self.tr('RESET DATA'))
            self.msg(self.tr('Paused recording'))
            icon.addPixmap(QtGui.QPixmap(":/control/reset.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        elif self.state == self.PAUSED:
            self.state = self.RESET
            self.graph.setXRange(0, 100)
            self.curve.setData([], [])
            self.curve.clear()
            self.fitcurve.clear()
            self.datapoints = 0
            self.valueTable.scrollToTop()
            self.TData = np.empty(500)
            self.EMFData = np.empty(500)
            self.logButton.setText(self.tr('START MEASUREMENTS'))
            self.msg(self.tr('Clear Traces and Data'))
            icon.addPixmap(QtGui.QPixmap(":/control/play.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        self.logButton.setIcon(icon)

    def setInterval(self):
        self.intervalBox.setValue(2)

    def linearFit(self):
        res = ''
        self.isPaused = True;
        S, E = self.region.getRegion()
        start = (np.abs(self.TData[:self.datapoints] - S)).argmin()
        end = (np.abs(self.TData[:self.datapoints] - E)).argmin()
        print(S,E,start, end, self.TData[start:end], self.EMFData[start:end])
        try:
            fa = em.fit_line(self.TData[start:end], self.EMFData[start:end])
            if fa is not None:
                self.fitcurve.clear()
                self.fitcurve.setData(self.TData[start:end], fa[0])
                res += '%.3f, %.3f'%(fa[1][0],fa[1][1])

        except Exception as e:
            res += '--<br>'
            print(e)
            pass
        self.msgBox = QtWidgets.QMessageBox(self)
        self.msgBox.setWindowModality(QtCore.Qt.NonModal)
        self.msgBox.setWindowTitle('Linear Fit Results')
        self.msgBox.setText(res)
        self.msgBox.show()

    def updateHandler(self, device):
        if (device.connected):
            self.p = device

    def msg(self, m):
        self.msgwin.setText(self.tr(m))

    def saveData(self):
        fn = QFileDialog.getSaveFileName(self, "Save file", QtCore.QDir.currentPath(),
                                         "Text files (*.txt);;CSV files (*.csv)", "CSV files (*.csv)")
        if (len(fn) == 2):  #Tuple
            fn = fn[0]
        if '.' not in fn:
            fn+='.csv'
        print(fn)
        if fn != '':
            f = open(fn, 'wt')
            f.write('time')
            f.write('Temperature(C),EMF(mV)\n')
            for a in range(self.datapoints):
                f.write('%.3f,%.3f\n' % (self.TData[a], self.EMFData[a]))
            f.close()
            self.msg(self.tr('Traces saved to ') + fn)


if __name__ == '__main__':
    from . eyes17 import eyes

    dev = eyes17.eyes.open()
    app = QApplication(sys.argv)

    # translation stuff
    lang = QLocale.system().name()
    t = QTranslator()
    t.load("lang/" + lang, os.path.dirname(__file__))
    app.installTranslator(t)
    t1 = QTranslator()
    t1.load("qt_" + lang,
            QLibraryInfo.location(QLibraryInfo.TranslationsPath))
    app.installTranslator(t1)

    mw = Expt(dev)
    mw.show()
    sys.exit(app.exec_())
