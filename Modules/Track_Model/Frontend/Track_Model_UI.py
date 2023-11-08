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
        TrackModelModule.resize(1280, 1050)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(TrackModelModule.sizePolicy().hasHeightForWidth())
        TrackModelModule.setSizePolicy(sizePolicy)
        TrackModelModule.setMaximumSize(QtCore.QSize(1280, 1050))
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
        self.TrackLineColorValue.setGeometry(QtCore.QRect(80, 20, 151, 41))
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
        icon = QtGui.QIcon.fromTheme("red")
        self.TrackLineColorValue.addItem(icon, "")
        icon = QtGui.QIcon.fromTheme("green")
        self.TrackLineColorValue.addItem(icon, "")
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
        self.pushButton = QtWidgets.QPushButton(parent=self.TrackModelBox)
        self.pushButton.setGeometry(QtCore.QRect(290, 30, 40, 40))
        self.pushButton.setStyleSheet("background-color: #008000")
        self.pushButton.setText("")
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(parent=self.TrackModelBox)
        self.label.setGeometry(QtCore.QRect(340, 40, 91, 16))
        self.label.setStyleSheet("color: #008000")
        self.label.setObjectName("label")
        self.pushButton_2 = QtWidgets.QPushButton(parent=self.TrackModelBox)
        self.pushButton_2.setGeometry(QtCore.QRect(480, 30, 40, 40))
        self.pushButton_2.setStyleSheet("background-color: #FF0000")
        self.pushButton_2.setText("")
        self.pushButton_2.setObjectName("pushButton_2")
        self.label_2 = QtWidgets.QLabel(parent=self.TrackModelBox)
        self.label_2.setGeometry(QtCore.QRect(530, 40, 111, 16))
        self.label_2.setStyleSheet("color: #FF0000")
        self.label_2.setObjectName("label_2")
        self.formLayoutWidget_2 = QtWidgets.QWidget(parent=self.TrackModelBox)
        self.formLayoutWidget_2.setGeometry(QtCore.QRect(939, 57, 271, 391))
        self.formLayoutWidget_2.setObjectName("formLayoutWidget_2")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget_2)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label_4 = QtWidgets.QLabel(parent=self.formLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_4)
        self.block_grade_display = QtWidgets.QLineEdit(parent=self.formLayoutWidget_2)
        self.block_grade_display.setObjectName("block_grade_display")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.ItemRole.FieldRole, self.block_grade_display)
        self.label_7 = QtWidgets.QLabel(parent=self.formLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_7)
        self.speed_limit_display = QtWidgets.QLineEdit(parent=self.formLayoutWidget_2)
        self.speed_limit_display.setObjectName("speed_limit_display")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.ItemRole.FieldRole, self.speed_limit_display)
        self.label_19 = QtWidgets.QLabel(parent=self.formLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_19.setFont(font)
        self.label_19.setObjectName("label_19")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_19)
        self.traffic_light_display = QtWidgets.QLineEdit(parent=self.formLayoutWidget_2)
        self.traffic_light_display.setObjectName("traffic_light_display")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.ItemRole.FieldRole, self.traffic_light_display)
        self.label_6 = QtWidgets.QLabel(parent=self.formLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_6)
        self.infrastructure_display = QtWidgets.QLineEdit(parent=self.formLayoutWidget_2)
        self.infrastructure_display.setObjectName("infrastructure_display")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.ItemRole.FieldRole, self.infrastructure_display)
        self.label_9 = QtWidgets.QLabel(parent=self.formLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_9)
        self.switch_direction_display = QtWidgets.QLineEdit(parent=self.formLayoutWidget_2)
        self.switch_direction_display.setObjectName("switch_direction_display")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.ItemRole.FieldRole, self.switch_direction_display)
        self.label_5 = QtWidgets.QLabel(parent=self.formLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(10, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_5)
        self.elevation_display = QtWidgets.QLineEdit(parent=self.formLayoutWidget_2)
        self.elevation_display.setObjectName("elevation_display")
        self.formLayout.setWidget(10, QtWidgets.QFormLayout.ItemRole.FieldRole, self.elevation_display)
        self.label_8 = QtWidgets.QLabel(parent=self.formLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.formLayout.setWidget(11, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_8)
        self.label_11 = QtWidgets.QLabel(parent=self.formLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.formLayout.setWidget(14, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_11)
        self.beacon_display = QtWidgets.QLineEdit(parent=self.formLayoutWidget_2)
        self.beacon_display.setObjectName("beacon_display")
        self.formLayout.setWidget(14, QtWidgets.QFormLayout.ItemRole.FieldRole, self.beacon_display)
        self.label_12 = QtWidgets.QLabel(parent=self.formLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.formLayout.setWidget(15, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_12)
        self.track_heater_display = QtWidgets.QLineEdit(parent=self.formLayoutWidget_2)
        self.track_heater_display.setObjectName("track_heater_display")
        self.formLayout.setWidget(15, QtWidgets.QFormLayout.ItemRole.FieldRole, self.track_heater_display)
        self.label_3 = QtWidgets.QLabel(parent=self.formLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_3)
        self.block_length_display = QtWidgets.QLineEdit(parent=self.formLayoutWidget_2)
        self.block_length_display.setObjectName("block_length_display")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.block_length_display)
        self.label_10 = QtWidgets.QLabel(parent=self.formLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_10)
        self.crossing_status_display = QtWidgets.QLineEdit(parent=self.formLayoutWidget_2)
        self.crossing_status_display.setObjectName("crossing_status_display")
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.ItemRole.FieldRole, self.crossing_status_display)
        self.cum_elevation_display = QtWidgets.QLineEdit(parent=self.formLayoutWidget_2)
        self.cum_elevation_display.setObjectName("cum_elevation_display")
        self.formLayout.setWidget(11, QtWidgets.QFormLayout.ItemRole.FieldRole, self.cum_elevation_display)
        self.label_13 = QtWidgets.QLabel(parent=self.TrackModelBox)
        self.label_13.setGeometry(QtCore.QRect(1010, 480, 141, 16))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_13.setFont(font)
        self.label_13.setObjectName("label_13")
        self.formLayoutWidget_3 = QtWidgets.QWidget(parent=self.TrackModelBox)
        self.formLayoutWidget_3.setGeometry(QtCore.QRect(940, 510, 271, 215))
        self.formLayoutWidget_3.setObjectName("formLayoutWidget_3")
        self.formLayout_2 = QtWidgets.QFormLayout(self.formLayoutWidget_3)
        self.formLayout_2.setContentsMargins(0, 0, 0, 0)
        self.formLayout_2.setObjectName("formLayout_2")
        self.passenger_occupancy_display = QtWidgets.QLineEdit(parent=self.formLayoutWidget_3)
        self.passenger_occupancy_display.setObjectName("passenger_occupancy_display")
        self.formLayout_2.setWidget(7, QtWidgets.QFormLayout.ItemRole.FieldRole, self.passenger_occupancy_display)
        self.label_18 = QtWidgets.QLabel(parent=self.formLayoutWidget_3)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_18.setFont(font)
        self.label_18.setObjectName("label_18")
        self.formLayout_2.setWidget(7, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_18)
        self.train_ID_display = QtWidgets.QLineEdit(parent=self.formLayoutWidget_3)
        self.train_ID_display.setObjectName("train_ID_display")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.train_ID_display)
        self.label_26 = QtWidgets.QLabel(parent=self.formLayoutWidget_3)
        self.label_26.setObjectName("label_26")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_26)
        self.label_14 = QtWidgets.QLabel(parent=self.formLayoutWidget_3)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_14.setFont(font)
        self.label_14.setObjectName("label_14")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_14)
        self.direction_of_travel_display = QtWidgets.QLineEdit(parent=self.formLayoutWidget_3)
        self.direction_of_travel_display.setObjectName("direction_of_travel_display")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.direction_of_travel_display)
        self.label_16 = QtWidgets.QLabel(parent=self.formLayoutWidget_3)
        self.label_16.setObjectName("label_16")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_16)
        self.authority_display = QtWidgets.QLineEdit(parent=self.formLayoutWidget_3)
        self.authority_display.setObjectName("authority_display")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.ItemRole.FieldRole, self.authority_display)
        self.label_15 = QtWidgets.QLabel(parent=self.formLayoutWidget_3)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_15.setFont(font)
        self.label_15.setObjectName("label_15")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_15)
        self.current_speed_display = QtWidgets.QLineEdit(parent=self.formLayoutWidget_3)
        self.current_speed_display.setObjectName("current_speed_display")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.ItemRole.FieldRole, self.current_speed_display)
        self.label_17 = QtWidgets.QLabel(parent=self.formLayoutWidget_3)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_17.setFont(font)
        self.label_17.setObjectName("label_17")
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_17)
        self.acceleration_display = QtWidgets.QLineEdit(parent=self.formLayoutWidget_3)
        self.acceleration_display.setObjectName("acceleration_display")
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.ItemRole.FieldRole, self.acceleration_display)
        self.label_20 = QtWidgets.QLabel(parent=self.TrackModelBox)
        self.label_20.setGeometry(QtCore.QRect(1010, 30, 141, 20))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_20.setFont(font)
        self.label_20.setObjectName("label_20")
        self.formLayoutWidget_4 = QtWidgets.QWidget(parent=self.TrackModelBox)
        self.formLayoutWidget_4.setGeometry(QtCore.QRect(940, 750, 271, 131))
        self.formLayoutWidget_4.setObjectName("formLayoutWidget_4")
        self.formLayout_3 = QtWidgets.QFormLayout(self.formLayoutWidget_4)
        self.formLayout_3.setContentsMargins(0, 0, 0, 0)
        self.formLayout_3.setObjectName("formLayout_3")
        self.label_22 = QtWidgets.QLabel(parent=self.formLayoutWidget_4)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_22.setFont(font)
        self.label_22.setObjectName("label_22")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_22)
        self.label_23 = QtWidgets.QLabel(parent=self.formLayoutWidget_4)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_23.setFont(font)
        self.label_23.setObjectName("label_23")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_23)
        self.tickets_sold_display = QtWidgets.QLineEdit(parent=self.formLayoutWidget_4)
        self.tickets_sold_display.setObjectName("tickets_sold_display")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.tickets_sold_display)
        self.label_24 = QtWidgets.QLabel(parent=self.formLayoutWidget_4)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_24.setFont(font)
        self.label_24.setObjectName("label_24")
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_24)
        self.passengers_boarding_display = QtWidgets.QLineEdit(parent=self.formLayoutWidget_4)
        self.passengers_boarding_display.setObjectName("passengers_boarding_display")
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.ItemRole.FieldRole, self.passengers_boarding_display)
        self.label_25 = QtWidgets.QLabel(parent=self.formLayoutWidget_4)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_25.setFont(font)
        self.label_25.setObjectName("label_25")
        self.formLayout_3.setWidget(3, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_25)
        self.passengers_disembarking_display = QtWidgets.QLineEdit(parent=self.formLayoutWidget_4)
        self.passengers_disembarking_display.setObjectName("passengers_disembarking_display")
        self.formLayout_3.setWidget(3, QtWidgets.QFormLayout.ItemRole.FieldRole, self.passengers_disembarking_display)
        self.station_name_display = QtWidgets.QLineEdit(parent=self.formLayoutWidget_4)
        self.station_name_display.setObjectName("station_name_display")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.station_name_display)
        self.label_21 = QtWidgets.QLabel(parent=self.TrackModelBox)
        self.label_21.setGeometry(QtCore.QRect(1000, 720, 153, 22))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_21.setFont(font)
        self.label_21.setObjectName("label_21")
        self.SetEnvironmentTemperatureInputBox = QtWidgets.QSpinBox(parent=self.ModuleSection)
        self.SetEnvironmentTemperatureInputBox.setGeometry(QtCore.QRect(870, 20, 71, 41))
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
        self.EnvironmentTemperatureLabel.setGeometry(QtCore.QRect(950, 10, 191, 61))
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
        self.LoadTrackModelButton.setGeometry(QtCore.QRect(570, 10, 221, 51))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.LoadTrackModelButton.sizePolicy().hasHeightForWidth())
        self.LoadTrackModelButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(24)
        self.LoadTrackModelButton.setFont(font)
        self.LoadTrackModelButton.setStyleSheet("color: #00ffff")
        self.LoadTrackModelButton.setObjectName("LoadTrackModelButton")
        self.formLayoutWidget = QtWidgets.QWidget(parent=self.ModuleSection)
        self.formLayoutWidget.setGeometry(QtCore.QRect(320, 10, 161, 71))
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
        self.LineSelectHint = QtWidgets.QLabel(parent=self.ModuleSection)
        self.LineSelectHint.setGeometry(QtCore.QRect(30, 0, 251, 41))
        self.LineSelectHint.setObjectName("LineSelectHint")
        self.FailureModesBoxLabel = QtWidgets.QLabel(parent=self.ModuleSection)
        self.FailureModesBoxLabel.setGeometry(QtCore.QRect(340, 0, 121, 20))
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
        self.FailureModesBoxLabel.setStyleSheet("color: #ffa500")
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
        self.label.setText(_translate("TrackModelModule", "= Empty Block"))
        self.label_2.setText(_translate("TrackModelModule", "= Occupied Block"))
        self.label_4.setText(_translate("TrackModelModule", "Block Grade (%)"))
        self.label_7.setText(_translate("TrackModelModule", "Speed Limit (mph)"))
        self.label_19.setText(_translate("TrackModelModule", "Traffic Light"))
        self.label_6.setText(_translate("TrackModelModule", "Infrastructure"))
        self.label_9.setText(_translate("TrackModelModule", "Active Switch Direction"))
        self.label_5.setText(_translate("TrackModelModule", "Elevation (m)"))
        self.label_8.setText(_translate("TrackModelModule", "Cumulative Elevation (m)"))
        self.label_11.setText(_translate("TrackModelModule", "Beacon"))
        self.label_12.setText(_translate("TrackModelModule", "Track Heater"))
        self.label_3.setText(_translate("TrackModelModule", "Block Length (m)"))
        self.label_10.setText(_translate("TrackModelModule", "Crossing Status"))
        self.label_13.setText(_translate("TrackModelModule", "Train Information"))
        self.label_18.setText(_translate("TrackModelModule", "Passenger Occupancy"))
        self.label_26.setText(_translate("TrackModelModule", "Train ID"))
        self.label_14.setText(_translate("TrackModelModule", "Direction of Travel"))
        self.label_16.setText(_translate("TrackModelModule", "Authority (ft)"))
        self.label_15.setText(_translate("TrackModelModule", "Current Speed (mph)"))
        self.label_17.setText(_translate("TrackModelModule", "Acceleration(mi/s^2)"))
        self.label_20.setText(_translate("TrackModelModule", "Block Information"))
        self.label_22.setText(_translate("TrackModelModule", "Station Name"))
        self.label_23.setText(_translate("TrackModelModule", "Tickets Sold"))
        self.label_24.setText(_translate("TrackModelModule", "Passengers Boarding"))
        self.label_25.setText(_translate("TrackModelModule", "Passengers Disembarking"))
        self.label_21.setText(_translate("TrackModelModule", "Station Information"))
        self.EnvironmentTemperatureLabel.setText(_translate("TrackModelModule", "<html><head/><body><p><span style=\" font-size:18pt;\">Environment Temperature (degrees Fahrenheit)</span></p></body></html>"))
        self.LoadTrackModelButton.setText(_translate("TrackModelModule", "Load Track Model"))
        self.TrackCircuitFailureToggleButton.setText(_translate("TrackModelModule", "Track Circuit Failure"))
        self.PowerFailureToggleButton.setText(_translate("TrackModelModule", "Power Failure"))
        self.BrokenRailToggleButton.setText(_translate("TrackModelModule", "Broken Rail"))
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
