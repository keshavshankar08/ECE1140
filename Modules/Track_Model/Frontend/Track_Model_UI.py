# Form implementation generated from reading ui file 'Track_Model_UI.ui'
#
# Created by: PyQt6 UI code generator 6.5.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_TrackModelModule(object):
    def setupUi(self, TrackModelModule):
        TrackModelModule.setObjectName("TrackModelModule")
        TrackModelModule.resize(980, 1050)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(TrackModelModule.sizePolicy().hasHeightForWidth())
        TrackModelModule.setSizePolicy(sizePolicy)
        TrackModelModule.setMaximumSize(QtCore.QSize(980, 1050))
        font = QtGui.QFont()
        font.setFamily("Arial")
        TrackModelModule.setFont(font)
        TrackModelModule.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.centralwidget = QtWidgets.QWidget(parent=TrackModelModule)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.ModuleSection = QtWidgets.QFrame(parent=self.centralwidget)
        self.ModuleSection.setGeometry(QtCore.QRect(10, 10, 1256, 1031))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ModuleSection.sizePolicy().hasHeightForWidth())
        self.ModuleSection.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.ModuleSection.setFont(font)
        self.ModuleSection.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.ModuleSection.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.ModuleSection.setObjectName("ModuleSection")
        self.TrackLineColorValue = QtWidgets.QComboBox(parent=self.ModuleSection)
        self.TrackLineColorValue.setGeometry(QtCore.QRect(50, 20, 151, 41))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.TrackLineColorValue.sizePolicy().hasHeightForWidth())
        self.TrackLineColorValue.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(18)
        self.TrackLineColorValue.setFont(font)
        self.TrackLineColorValue.setMaxVisibleItems(10)
        self.TrackLineColorValue.setMaxCount(4)
        self.TrackLineColorValue.setObjectName("TrackLineColorValue")
        self.TrackLineColorValue.addItem("")
        self.TrackLineColorValue.addItem("")
        self.TrackLineColorValue.addItem("")
        self.TrackModelBox = QtWidgets.QGroupBox(parent=self.ModuleSection)
        self.TrackModelBox.setGeometry(QtCore.QRect(20, 60, 1211, 961))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.TrackModelBox.sizePolicy().hasHeightForWidth())
        self.TrackModelBox.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.TrackModelBox.setFont(font)
        self.TrackModelBox.setObjectName("TrackModelBox")
        self.graphicsView = QtWidgets.QGraphicsView(parent=self.TrackModelBox)
        self.graphicsView.setGeometry(QtCore.QRect(-5, 21, 941, 941))
        self.graphicsView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.graphicsView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.graphicsView.setObjectName("graphicsView")
        self.SetEnvironmentTemperatureInputBox = QtWidgets.QSpinBox(parent=self.ModuleSection)
        self.SetEnvironmentTemperatureInputBox.setGeometry(QtCore.QRect(690, 10, 71, 41))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SetEnvironmentTemperatureInputBox.sizePolicy().hasHeightForWidth())
        self.SetEnvironmentTemperatureInputBox.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(18)
        self.SetEnvironmentTemperatureInputBox.setFont(font)
        self.SetEnvironmentTemperatureInputBox.setProperty("value", 68)
        self.SetEnvironmentTemperatureInputBox.setObjectName("SetEnvironmentTemperatureInputBox")
        self.EnvironmentTemperatureLabel = QtWidgets.QLabel(parent=self.ModuleSection)
        self.EnvironmentTemperatureLabel.setGeometry(QtCore.QRect(760, 0, 191, 61))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.EnvironmentTemperatureLabel.sizePolicy().hasHeightForWidth())
        self.EnvironmentTemperatureLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial Narrow")
        font.setPointSize(24)
        self.EnvironmentTemperatureLabel.setFont(font)
        self.EnvironmentTemperatureLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.EnvironmentTemperatureLabel.setWordWrap(True)
        self.EnvironmentTemperatureLabel.setObjectName("EnvironmentTemperatureLabel")
        self.LoadTrackModelButton = QtWidgets.QPushButton(parent=self.ModuleSection)
        self.LoadTrackModelButton.setGeometry(QtCore.QRect(440, 10, 221, 51))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.LoadTrackModelButton.sizePolicy().hasHeightForWidth())
        self.LoadTrackModelButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(24)
        self.LoadTrackModelButton.setFont(font)
        self.LoadTrackModelButton.setObjectName("LoadTrackModelButton")
        self.formLayoutWidget = QtWidgets.QWidget(parent=self.ModuleSection)
        self.formLayoutWidget.setGeometry(QtCore.QRect(270, 10, 161, 71))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.FailureButtons = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.FailureButtons.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetDefaultConstraint)
        self.FailureButtons.setFieldGrowthPolicy(QtWidgets.QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)
        self.FailureButtons.setLabelAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.FailureButtons.setFormAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.FailureButtons.setContentsMargins(0, 0, 0, 0)
        self.FailureButtons.setObjectName("FailureButtons")
        self.TrackCircuitFailureToggleButton = QtWidgets.QRadioButton(parent=self.formLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.TrackCircuitFailureToggleButton.sizePolicy().hasHeightForWidth())
        self.TrackCircuitFailureToggleButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(14)
        self.TrackCircuitFailureToggleButton.setFont(font)
        self.TrackCircuitFailureToggleButton.setAutoExclusive(False)
        self.TrackCircuitFailureToggleButton.setObjectName("TrackCircuitFailureToggleButton")
        self.FailureButtons.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.TrackCircuitFailureToggleButton)
        self.BrokenRailToggleButton = QtWidgets.QRadioButton(parent=self.formLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.BrokenRailToggleButton.sizePolicy().hasHeightForWidth())
        self.BrokenRailToggleButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(14)
        self.BrokenRailToggleButton.setFont(font)
        self.BrokenRailToggleButton.setAutoExclusive(False)
        self.BrokenRailToggleButton.setObjectName("BrokenRailToggleButton")
        self.FailureButtons.setWidget(2, QtWidgets.QFormLayout.ItemRole.LabelRole, self.BrokenRailToggleButton)
        self.PowerFailureToggleButton = QtWidgets.QRadioButton(parent=self.formLayoutWidget)
        self.PowerFailureToggleButton.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PowerFailureToggleButton.sizePolicy().hasHeightForWidth())
        self.PowerFailureToggleButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(14)
        self.PowerFailureToggleButton.setFont(font)
        self.PowerFailureToggleButton.setCheckable(True)
        self.PowerFailureToggleButton.setChecked(False)
        self.PowerFailureToggleButton.setAutoExclusive(False)
        self.PowerFailureToggleButton.setObjectName("PowerFailureToggleButton")
        self.FailureButtons.setWidget(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.PowerFailureToggleButton)
        self.TrackCircuitFailureToggleButton.raise_()
        self.PowerFailureToggleButton.raise_()
        self.BrokenRailToggleButton.raise_()
        self.LineSelectHint = QtWidgets.QLabel(parent=self.ModuleSection)
        self.LineSelectHint.setGeometry(QtCore.QRect(10, 0, 251, 41))
        self.LineSelectHint.setObjectName("LineSelectHint")
        self.FailureModesBoxLabel = QtWidgets.QLabel(parent=self.ModuleSection)
        self.FailureModesBoxLabel.setGeometry(QtCore.QRect(290, 0, 121, 20))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.FailureModesBoxLabel.sizePolicy().hasHeightForWidth())
        self.FailureModesBoxLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(18)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.FailureModesBoxLabel.setFont(font)
        self.FailureModesBoxLabel.setObjectName("FailureModesBoxLabel")
        self.TrackModelBox.raise_()
        self.SetEnvironmentTemperatureInputBox.raise_()
        self.EnvironmentTemperatureLabel.raise_()
        self.LoadTrackModelButton.raise_()
        self.formLayoutWidget.raise_()
        self.TrackLineColorValue.raise_()
        self.LineSelectHint.raise_()
        self.FailureModesBoxLabel.raise_()
        TrackModelModule.setCentralWidget(self.centralwidget)

        self.retranslateUi(TrackModelModule)
        QtCore.QMetaObject.connectSlotsByName(TrackModelModule)

    def retranslateUi(self, TrackModelModule):
        _translate = QtCore.QCoreApplication.translate
        TrackModelModule.setWindowTitle(_translate("TrackModelModule", "Track Model"))
        self.TrackLineColorValue.setItemText(0, _translate("TrackModelModule", "Select a Line"))
        self.TrackLineColorValue.setItemText(1, _translate("TrackModelModule", "Red Line"))
        self.TrackLineColorValue.setItemText(2, _translate("TrackModelModule", "Green Line"))
        self.TrackModelBox.setTitle(_translate("TrackModelModule", "Track Model"))
        self.EnvironmentTemperatureLabel.setText(_translate("TrackModelModule", "<html><head/><body><p><span style=\" font-size:18pt;\">Environment Temperature (degrees Fahrenheit)</span></p></body></html>"))
        self.LoadTrackModelButton.setText(_translate("TrackModelModule", "Load Track Model"))
        self.TrackCircuitFailureToggleButton.setText(_translate("TrackModelModule", "Track Circuit Failure"))
        self.BrokenRailToggleButton.setText(_translate("TrackModelModule", "Broken Rail"))
        self.PowerFailureToggleButton.setText(_translate("TrackModelModule", "Power Failure"))
        self.LineSelectHint.setText(_translate("TrackModelModule", "<html><head/><body><p><span style=\" font-size:12pt; color:#fc0107;\">Please Load a Track Model to Select a Line!</span></p></body></html>"))
        self.FailureModesBoxLabel.setText(_translate("TrackModelModule", "Failure Modes"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    TrackModelModule = QtWidgets.QMainWindow()
    ui = Ui_TrackModelModule()
    ui.setupUi(TrackModelModule)
    TrackModelModule.show()
    sys.exit(app.exec())
