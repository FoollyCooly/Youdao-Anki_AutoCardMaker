# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.2.4
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QPlainTextEdit,
    QPushButton, QSizePolicy, QSpinBox, QTextBrowser,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(480, 640)
        font = QFont()
        font.setFamilies([u"\u5e7c\u5706"])
        Form.setFont(font)
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setObjectName(u"gridLayout")
        self.input_box = QPlainTextEdit(Form)
        self.input_box.setObjectName(u"input_box")

        self.gridLayout.addWidget(self.input_box, 1, 0, 1, 5)

        self.mn_box = QSpinBox(Form)
        self.mn_box.setObjectName(u"mn_box")
        self.mn_box.setValue(5)

        self.gridLayout.addWidget(self.mn_box, 2, 1, 1, 1)

        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 2, 2, 1, 1)

        self.label_4 = QLabel(Form)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 0, 0, 1, 3)

        self.exp_box = QSpinBox(Form)
        self.exp_box.setObjectName(u"exp_box")
        self.exp_box.setMaximum(3)
        self.exp_box.setValue(3)

        self.gridLayout.addWidget(self.exp_box, 2, 3, 1, 1)

        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)

        self.start_Button = QPushButton(Form)
        self.start_Button.setObjectName(u"start_Button")

        self.gridLayout.addWidget(self.start_Button, 2, 4, 1, 1)

        self.output_box = QTextBrowser(Form)
        self.output_box.setObjectName(u"output_box")

        self.gridLayout.addWidget(self.output_box, 3, 0, 1, 5)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"\u6700\u5927\u4f8b\u53e5\u6570\u91cf \uff1a", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"\u6bcf\u4e2a\u8bcd\u6c47\u4e00\u884c\uff0c\u8f93\u5165\u4e0b\u65b9", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"\u4fdd\u7559\u4e49\u9879\u6570\u91cf \uff1a", None))
        self.start_Button.setText(QCoreApplication.translate("Form", u"\u542f\u52a8", None))
    # retranslateUi