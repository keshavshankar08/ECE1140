# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'interfacemJNpSU.ui'
##
## Created by: Qt User Interface Compiler version 6.4.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDoubleSpinBox, QFrame, QHBoxLayout,
    QMainWindow, QPlainTextEdit, QPushButton, QSizePolicy,
    QSpacerItem, QTabWidget, QToolButton, QVBoxLayout,
    QWidget)
import resources

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setStyleSheet(u"#centralwidget{\n"
"	background-color: #ffffff;\n"
"}\n"
"#topMenuContainer{\n"
"	background-color: #68a2ee;\n"
"}")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"#topMenuContainer{\n"
"	background-color: #41b3e1;\n"
"}")
        self.MainContainer = QWidget(self.centralwidget)
        self.MainContainer.setObjectName(u"MainContainer")
        self.MainContainer.setGeometry(QRect(0, 160, 801, 441))
        self.tabWidget = QTabWidget(self.MainContainer)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(-4, -1, 411, 441))
        self.Manual = QWidget()
        self.Manual.setObjectName(u"Manual")
        self.tabWidget.addTab(self.Manual, "")
        self.Automatic = QWidget()
        self.Automatic.setObjectName(u"Automatic")
        self.tabWidget.addTab(self.Automatic, "")
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(0, 0, 801, 161))
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.topMenuContainer = QWidget(self.widget)
        self.topMenuContainer.setObjectName(u"topMenuContainer")
        self.topMenuContainer.setStyleSheet(u"background-color: rgb(142, 182, 255);\n"
"border-color: rgb(0, 0, 0);")
        self.horizontalLayout = QHBoxLayout(self.topMenuContainer)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.menuFrame = QFrame(self.topMenuContainer)
        self.menuFrame.setObjectName(u"menuFrame")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.menuFrame.sizePolicy().hasHeightForWidth())
        self.menuFrame.setSizePolicy(sizePolicy)
        self.menuFrame.setFrameShape(QFrame.StyledPanel)
        self.menuFrame.setFrameShadow(QFrame.Raised)
        self.widget1 = QWidget(self.menuFrame)
        self.widget1.setObjectName(u"widget1")
        self.widget1.setGeometry(QRect(10, 10, 761, 51))
        self.horizontalLayout_2 = QHBoxLayout(self.widget1)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.toolButton = QToolButton(self.widget1)
        self.toolButton.setObjectName(u"toolButton")
        self.toolButton.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.toolButton.sizePolicy().hasHeightForWidth())
        self.toolButton.setSizePolicy(sizePolicy1)
        self.toolButton.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"alternate-background-color: rgb(255, 255, 255);\n"
"selection-color: rgb(255, 255, 255);\n"
"selection-background-color: rgb(255, 255, 255);\n"
"gridline-color: rgb(255, 255, 255);\n"
"border-color: rgb(255, 255, 255);")
        icon = QIcon()
        icon.addFile(u":/icons/align-justify.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.toolButton.setIcon(icon)
        self.toolButton.setIconSize(QSize(32, 32))
        self.toolButton.setPopupMode(QToolButton.MenuButtonPopup)

        self.horizontalLayout_2.addWidget(self.toolButton)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_4)

        self.backButton = QPushButton(self.widget1)
        self.backButton.setObjectName(u"backButton")
        self.backButton.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        icon1 = QIcon()
        icon1.addFile(u":/icons/arrow-left.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.backButton.setIcon(icon1)
        self.backButton.setIconSize(QSize(32, 32))
        self.backButton.setFlat(False)

        self.horizontalLayout_2.addWidget(self.backButton)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)

        self.infoButton = QPushButton(self.widget1)
        self.infoButton.setObjectName(u"infoButton")
        self.infoButton.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        icon2 = QIcon()
        icon2.addFile(u":/icons/book-open.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.infoButton.setIcon(icon2)
        self.infoButton.setIconSize(QSize(32, 32))

        self.horizontalLayout_2.addWidget(self.infoButton)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.adjustSysClock = QDoubleSpinBox(self.widget1)
        self.adjustSysClock.setObjectName(u"adjustSysClock")
        self.adjustSysClock.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.adjustSysClock.setDecimals(0)
        self.adjustSysClock.setMinimum(1.000000000000000)
        self.adjustSysClock.setMaximum(50.000000000000000)

        self.horizontalLayout_2.addWidget(self.adjustSysClock)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.sysClock = QPlainTextEdit(self.widget1)
        self.sysClock.setObjectName(u"sysClock")
        self.sysClock.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.sysClock.setReadOnly(True)

        self.horizontalLayout_2.addWidget(self.sysClock)


        self.horizontalLayout.addWidget(self.menuFrame)


        self.verticalLayout.addWidget(self.topMenuContainer)

        self.lineScheduleContainer = QWidget(self.widget)
        self.lineScheduleContainer.setObjectName(u"lineScheduleContainer")
        self.scheduleBuilder = QPushButton(self.lineScheduleContainer)
        self.scheduleBuilder.setObjectName(u"scheduleBuilder")
        self.scheduleBuilder.setGeometry(QRect(300, 20, 181, 40))
        self.scheduleBuilder.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        icon3 = QIcon()
        icon3.addFile(u":/icons/calendar.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.scheduleBuilder.setIcon(icon3)
        self.scheduleBuilder.setIconSize(QSize(32, 32))
        self.scheduleBuilder.setFlat(False)
        self.toolButton_2 = QToolButton(self.lineScheduleContainer)
        self.toolButton_2.setObjectName(u"toolButton_2")
        self.toolButton_2.setEnabled(True)
        self.toolButton_2.setGeometry(QRect(30, 20, 61, 41))
        sizePolicy1.setHeightForWidth(self.toolButton_2.sizePolicy().hasHeightForWidth())
        self.toolButton_2.setSizePolicy(sizePolicy1)
        self.toolButton_2.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"alternate-background-color: rgb(255, 255, 255);\n"
"selection-color: rgb(255, 255, 255);\n"
"selection-background-color: rgb(255, 255, 255);\n"
"gridline-color: rgb(255, 255, 255);\n"
"border-color: rgb(255, 255, 255);")
        self.toolButton_2.setIcon(icon)
        self.toolButton_2.setIconSize(QSize(32, 32))
        self.toolButton_2.setPopupMode(QToolButton.MenuButtonPopup)

        self.verticalLayout.addWidget(self.lineScheduleContainer)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Manual), QCoreApplication.translate("MainWindow", u"Manual", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Automatic), QCoreApplication.translate("MainWindow", u"Automatic", None))
        self.toolButton.setText(QCoreApplication.translate("MainWindow", u"Module", None))
        self.backButton.setText(QCoreApplication.translate("MainWindow", u"Back", None))
        self.infoButton.setText(QCoreApplication.translate("MainWindow", u"Info", None))
        self.sysClock.setPlainText("")
        self.sysClock.setPlaceholderText(QCoreApplication.translate("MainWindow", u"System Clock: hh:mm:ss", None))
        self.scheduleBuilder.setText(QCoreApplication.translate("MainWindow", u"Open Schedule Builder", None))
        self.toolButton_2.setText(QCoreApplication.translate("MainWindow", u"Module", None))
    # retranslateUi

