    # This Python file uses the following encoding: utf-8
from PyQt5 import QtGui, QtCore, QtWidgets
import numpy as np
import datetime
from typing import Callable

from .config import loadConfigCurrent
config = loadConfigCurrent()
from ..ui.plotWidget import PlotWidget
from ..ui.histogramLUTWidget import HistogramLUTWidget
from ..ui.menuDb import MenuDb
from .pyqtgraph import pg

class WidgetPlot():
    """
    Class to handle ploting in 1d.
    """

    # For mypy
    plotWidget: PlotWidget
    plotItem: pg.PlotItem
    checkBoxCrossHair: QtWidgets.QCheckBox
    pushButtonCopy: QtWidgets.QPushButton
    winId: Callable
    frameGeometry: QtCore.QRect
    tabWidget: QtWidgets.QTabWidget
    findChildren: Callable
    config: dict
    plot2dzLabel: QtWidgets.QLabel
    histWidget: HistogramLUTWidget
    plotType: str
    comboBoxcm: QtWidgets.QComboBox
    checkBoxLogX: QtWidgets.QCheckBox
    checkBoxLogY: QtWidgets.QCheckBox
    labelCoordinate: QtWidgets.QLabel
    xData: np.ndarray
    yData: np.ndarray
    zData: np.ndarray
    sliceItems: dict


    def __init__(self, databaseAbsPath    : str) -> None:

        super(WidgetPlot, self).__init__()

        # Crosshair lines
        self.vLine = None
        self.hLine = None
        # self.crossHairRemove

        # For the right-click on the plot title
        self.databaseAbsPath= databaseAbsPath

        # Help deciding when drawing crosshair
        self.plotWidget.installEventFilter(self)
        self.plotWidgetHovered = False

        self.displayCrossHair = False

        # Connect signal
        self.plotItem.titleLabel.mousePressEvent = self.clickTitle
        self.plotItem.scene().sigMouseMoved.connect(self.mouseMoved)
        self.checkBoxCrossHair.stateChanged.connect(self.checkBoxCrossHairState)
        self.pushButtonCopy.clicked.connect(self.pushButtonCopyClicked)



    ####################################
    #
    #           Copie plot to clipboard
    #
    ####################################



    def pushButtonCopyClicked(self) -> None:
        """
        Called when user wants to place a screenshot of its plot in the
        clipboard.
        """

        screen    = QtWidgets.QApplication.primaryScreen()
        clipboard = QtWidgets.QApplication.clipboard()

        # We remove -25 because otherwise the tabwidget is still visible
        pixmap = screen.grabWindow(self.winId(),
                                   x=0,
                                   y=0,
                                   width=self.frameGeometry().width()-self.tabWidget.frameGeometry().width()-25)
        clipboard.setPixmap(pixmap)

        self.pushButtonCopy.setText('Copied to clipboard !')

        self._clipboardTimer = QtCore.QTimer()
        self._clipboardTimer.timeout.connect(self.pushButtonCopyUpdate)
        self._clipboardTimer.setInterval(2000)
        self._clipboardTimer.start()



    def pushButtonCopyUpdate(self):
        """
        Called 2s after the user click on the pushButtonCopy.
        Update its text and delete the timer
        """

        self.pushButtonCopy.setText('Click to copy')
        self._clipboardTimer.stop()
        self._clipboardTimer.deleteLater()
        self._clipboardTimer = None



    ####################################
    #
    #           Method related to style
    #
    ####################################


    def updateStyle(self) -> None:

        for qlabel in self.findChildren(QtWidgets.QLabel)+self.findChildren(QtWidgets.QCheckBox)+self.findChildren(QtWidgets.QGroupBox):
            qlabel.setStyleSheet("background-color: "+str(self.config['styles'][self.config['style']]['dialogBackgroundColor'])+";")
            qlabel.setStyleSheet("color: "+str(self.config['styles'][self.config['style']]['dialogTextColor'])+";")

        self.plotItem.getAxis('bottom')._updateLabel()
        font=QtGui.QFont()
        font.setPixelSize(self.config['tickLabelFontSize'])
        self.plotItem.getAxis('bottom').setTickFont(font)
        self.plotItem.getAxis('left').setTickFont(font)
        self.plotItem.getAxis('bottom').setPen(self.config['styles'][self.config['style']]['pyqtgraphxAxisTicksColor'])
        self.plotItem.getAxis('left').setPen(self.config['styles'][self.config['style']]['pyqtgraphyAxisTicksColor'])
        self.plotItem.getAxis('bottom').setTextPen(self.config['styles'][self.config['style']]['pyqtgraphxAxisTickLabelsColor'])
        self.plotItem.getAxis('left').setTextPen(self.config['styles'][self.config['style']]['pyqtgraphyAxisTickLabelsColor'])

        if self.plotType=='2d':
            self.plot2dzLabel.setFont(font)
            self.histWidget.axis.setTickFont(font)

        self.plotItem.setTitle(title=self.plotItem.titleLabel.text,
                               color=self.config['styles'][self.config['style']]['pyqtgraphTitleTextColor'])

        self.plotItem.setLabel(axis='bottom',
                               text=self.plotItem.axes['bottom']['item'].labelText,
                               units=self.plotItem.axes['bottom']['item'].labelUnits,
                               **{'color'     : self.config['styles'][self.config['style']]['pyqtgraphxLabelTextColor'],
                                  'font-size' : str(self.config['axisLabelFontSize'])+'pt'})
        self.plotItem.setLabel(axis='left',
                               text=self.plotItem.axes['left']['item'].labelText,
                               units=self.plotItem.axes['left']['item'].labelUnits,
                               **{'color'     : self.config['styles'][self.config['style']]['pyqtgraphyLabelTextColor'],
                                  'font-size' : str(self.config['axisLabelFontSize'])+'pt'})

        # Update colormap
        if self.plotType=='2d':
            index = self.comboBoxcm.findText(self.config['plot2dcm'])
            self.comboBoxcm.setCurrentIndex(index)


    ####################################
    #
    #           Method related to the title
    #
    ####################################


    def clickTitle(self, b: QtWidgets.QGraphicsSceneMouseEvent) -> None:

        # We open a homemade menu
        if b.button()==2:
            MenuDb(self.databaseAbsPath)



    def eventFilter(self, object : PlotWidget,
                          event  : QtGui.QFocusEvent) -> bool:
        """
        Return True/False when the mouse enters/leaves by the PlotWidget.
        """

        if event.type()==QtCore.QEvent.Enter:
            self.plotWidgetHovered = True
            return True
        elif event.type()==QtCore.QEvent.Leave:
            self.plotWidgetHovered = False
        return False



    def checkBoxCrossHairState(self, b: int) -> None:
        """
        Method called when user click on the log checkBoxes.
        Modify the scale, linear or logarithmic, of the plotItem following
        which checkbox are checked.
        """

        if self.checkBoxCrossHair.isChecked():
            self.displayCrossHair = True
        else:
            self.displayCrossHair = False



    def isMouseOverView(self) -> bool:
        """
        Return true if mouse is over the view of the plot.
        """

        # We implement a workaround for the log mode of 1D plot.
        # See: https://github.com/pyqtgraph/pyqtgraph/issues/1470#issuecomment-864568004
        if self.plotType=='1d':
            if self.checkBoxLogX.isChecked():
                xmin = 10**self.plotItem.axes['bottom']['item'].range[0]
                xmax = 10**self.plotItem.axes['bottom']['item'].range[1]
            else:
                xmin = self.plotItem.axes['bottom']['item'].range[0]
                xmax = self.plotItem.axes['bottom']['item'].range[1]
            if self.checkBoxLogY.isChecked():
                ymin = 10**self.plotItem.axes['left']['item'].range[0]
                ymax = 10**self.plotItem.axes['left']['item'].range[1]
            else:
                ymin = self.plotItem.axes['left']['item'].range[0]
                ymax = self.plotItem.axes['left']['item'].range[1]
        else:
            xmin = self.plotItem.axes['bottom']['item'].range[0]
            xmax = self.plotItem.axes['bottom']['item'].range[1]

            ymin = self.plotItem.axes['left']['item'].range[0]
            ymax = self.plotItem.axes['left']['item'].range[1]

        xmax -= (xmax-xmin)/100
        ymax -= (ymax-ymin)/100

        if self.mousePos[0] > xmin and self.mousePos[0] < xmax \
        and self.mousePos[1] > ymin and self.mousePos[1] < ymax \
        and self.plotWidgetHovered:
            return True
        else:
            return False



    def mouseMoved(self, pos: QtCore.QPointF) -> None:
        """
        Handle the event when the mouse move hover the plotitem.
        Basically do two things:
            Display mouse coordinates
            Draw and undraw a crosshair instead of the mouse cursor

        Parameters
        ----------
        pos : QtCore.QPointF
            Position of the mouse in the scene.
            Will be converted in View unit using mapSceneToView.
        """

        # Get mouse coordinates in "good" units
        pos = self.plotItem.vb.mapSceneToView(pos)

        # We implement a workaround for the log mode of 1D plot.
        # See: https://github.com/pyqtgraph/pyqtgraph/issues/1470#issuecomment-864568004
        if self.plotType=='1d':
            if self.checkBoxLogX.isChecked():
                x = 10**pos.x()
            else:
                x = pos.x()
            if self.checkBoxLogY.isChecked():
                y = 10**pos.y()
            else:
                y = pos.y()
        else:
            x = pos.x()
            y = pos.y()

        # Save it
        self.mousePos = x, y

        # If mouse is over the viewbox, we change cursor in crosshair
        # If mouse is not over the viewbox, we change back the crosshair in cursor and remove the crosshair
        # Get displayed axes range
        if self.isMouseOverView():

            # Update the displayed mouse coordinates
            self.setMouseCoordinate()

            # Update cursor when hovering infiniteLine
            self.sliceItemHovering()

            # Display the "crosshair"
            if self.displayCrossHair:
                self.crossHair()
        else:
            self.setMouseCoordinate(blank=True)

            if self.displayCrossHair:
                self.crossHair(remove=True)



    def setMouseCoordinate(self, blank: bool=False) -> None:
        """
        Display the mouse coodinate in respect to the plot view in the GUI.
        If the x axis is a time axis, we display coordinate in human readable
        format.
        For 1d plot we display :x, y.
        For 2d plot we display :x, y, z.

        Parameters
        ----------
        blank : bool
            If True, display an empty text, effectively erasing the previous
            entry. Used when the mouse leave the plotItem.
        """

        if blank:
            self.labelCoordinate.setText('')
        else:

            spaceX = ''
            spaceY = ''
            if self.mousePos[0]>0:
                spaceX = '&nbsp;'
            if self.mousePos[1]>0:
                spaceY = '&nbsp;'


            if self.plotType=='1d':

                if isinstance(self.plotItem.getAxis('bottom'), pg.DateAxisItem):
                    x = datetime.datetime.utcfromtimestamp(self.mousePos[0]).strftime('%Y-%m-%d %H:%M:%S')
                    self.labelCoordinate.setText('x: {:}<br/>y: {}{:.{nbDecimal}e}'.format(x, spaceY, self.mousePos[1], nbDecimal=config['plotCoordinateNbNumber']))
                else:
                    self.labelCoordinate.setText('x: {}{:.{nbDecimal}e}<br/>y: {}{:.{nbDecimal}e}'.format(spaceX, self.mousePos[0],spaceY, self.mousePos[1], nbDecimal=config['plotCoordinateNbNumber']))
            elif self.plotType=='2d':

                n = np.abs(self.xData-self.mousePos[0]).argmin()
                m = np.abs(self.yData-self.mousePos[1]).argmin()
                z = self.zData[n,m]

                spaceZ = ''
                if z>0:
                    spaceZ = '&nbsp;'

                self.labelCoordinate.setText('x: {}{:.{nbDecimal}e}<br/>y: {}{:.{nbDecimal}e}<br/>z: {}{:.{nbDecimal}e}'.format(spaceX, self.mousePos[0], spaceY, self.mousePos[1], spaceZ, z, nbDecimal=config['plotCoordinateNbNumber']))
            else:
                raise ValueError('plotType unknown')



    def sliceItemHovering(self, defaultCursor: QtCore.Qt.CursorShape=QtCore.Qt.ArrowCursor) -> None:
        """
        Called when user cursor if hovering a sliceItem.

        Parameters
        ----------
        defaultCursor : QtCore.Qt.CursorShape, default QtCore.Qt.ArrowCursor
            Cursor to put back when the mouse leave an sliceItem.
        """

        # If we are hovering at least one sliceItem, the cursor is modified
        for line in list(self.sliceItems.values()):
            if line.mouseHovering:
                defaultCursor = QtCore.Qt.PointingHandCursor


        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(defaultCursor))



    def crossHair(self, remove        : bool=False,
                        defaultCursor : QtCore.Qt.CursorShape=QtCore.Qt.ArrowCursor) -> None:
        """
        Handle the crossHair draw on the viewbox.

        Parameters
        ----------
        remove : bool, default False
            If the crossHair should be removed.
        defaultCursor : QtCore.Qt.CursorShape, default QtCore.Qt.ArrowCursor
            Cursor to put back when the crosshair is removed.
        """

        # if the plot is a 2dplot, there is a possibility that the user mouse is
        # above an infiniteLine, if so, we remove the crosshair
        if self.plotType=='2d':
            for line in list(self.sliceItems.values()):
                if line.mouseHovering:
                    remove = True

        # If 'vline' is None it means the crosshair hasn't been created
        if not remove and self.vLine is None:
            # Build the crosshair style

            if config['crossHairLineStyle']=='solid':
                lineStyle = QtCore.Qt.SolidLine
            elif config['crossHairLineStyle']=='dashed':
                lineStyle = QtCore.Qt.DashLine
            elif config['crossHairLineStyle']=='dotted':
                lineStyle = QtCore.Qt.DotLine
            elif config['crossHairLineStyle']=='dashed-dotted':
                lineStyle = QtCore.Qt.DashDotLine
            else:
                raise ValueError('Config parameter "crossHairLineStyle" not recognize')


            penInfLine = pg.mkPen(config['crossHairLineColor'],
                                  width=config['crossHairLineWidth'],
                                  style=lineStyle)

            vLine = pg.InfiniteLine(angle=90, movable=False, pen=penInfLine)
            hLine = pg.InfiniteLine(angle=0,  movable=False, pen=penInfLine)
            self.plotItem.addItem(vLine, ignoreBounds=True)
            self.plotItem.addItem(hLine, ignoreBounds=True)
            self.vLine = vLine
            self.hLine = hLine

            QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.BlankCursor))

        # If the crosshair exist, and we want to remove it
        elif remove and self.vLine is not None:

            self.plotItem.removeItem(self.vLine)
            self.plotItem.removeItem(self.hLine)
            self.vLine = None
            self.hLine = None

            QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(defaultCursor))


        # Otherwise, we update its position
        elif self.vLine is not None:

            self.vLine.setPos(self.mousePos[0])
            self.hLine.setPos(self.mousePos[1])
