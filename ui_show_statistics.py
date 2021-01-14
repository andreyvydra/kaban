# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designs/show_statistics.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(452, 597)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("designs\\../img/Без названия.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        Form.setStyleSheet("background-color: #333333;\n"
"")
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.todo = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.todo.setFont(font)
        self.todo.setStyleSheet("color: #ffffff;")
        self.todo.setText("")
        self.todo.setObjectName("todo")
        self.gridLayout.addWidget(self.todo, 1, 1, 1, 1)
        self.label = QtWidgets.QLabel(Form)
        self.label.setStyleSheet("color: #ffffff;")
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setStyleSheet("color: #ffffff;")
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setStyleSheet("color: #ffffff;")
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 4, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(Form)
        self.label_7.setStyleSheet("color: #ffffff;")
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 3, 0, 1, 1)
        self.quantity = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.quantity.setFont(font)
        self.quantity.setStyleSheet("color: #ffffff;")
        self.quantity.setText("")
        self.quantity.setObjectName("quantity")
        self.gridLayout.addWidget(self.quantity, 0, 1, 1, 1)
        self.progress = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.progress.setFont(font)
        self.progress.setStyleSheet("color: #ffffff;")
        self.progress.setText("")
        self.progress.setObjectName("progress")
        self.gridLayout.addWidget(self.progress, 2, 1, 1, 1)
        self.done = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.done.setFont(font)
        self.done.setStyleSheet("color: #ffffff;")
        self.done.setText("")
        self.done.setObjectName("done")
        self.gridLayout.addWidget(self.done, 3, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setStyleSheet("color: #ffffff;")
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 2, 0, 1, 1)
        self.percentDone = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.percentDone.setFont(font)
        self.percentDone.setStyleSheet("color: #ffffff;")
        self.percentDone.setText("")
        self.percentDone.setObjectName("percentDone")
        self.gridLayout.addWidget(self.percentDone, 4, 1, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.status = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.status.sizePolicy().hasHeightForWidth())
        self.status.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.status.setFont(font)
        self.status.setStyleSheet("color: #ffffff;\n"
"")
        self.status.setText("")
        self.status.setAlignment(QtCore.Qt.AlignCenter)
        self.status.setObjectName("status")
        self.verticalLayout.addWidget(self.status)
        self.medal = QtWidgets.QLabel(Form)
        self.medal.setText("")
        self.medal.setAlignment(QtCore.Qt.AlignCenter)
        self.medal.setObjectName("medal")
        self.verticalLayout.addWidget(self.medal)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Статистика"))
        self.label.setText(_translate("Form", "Общее количество задач:"))
        self.label_3.setText(_translate("Form", "Задач в статусе \"\'ожидание\":"))
        self.label_2.setText(_translate("Form", "Процент завершённых задач:"))
        self.label_7.setText(_translate("Form", "Задач в статусе \"завершено\":"))
        self.label_5.setText(_translate("Form", "Задач в статусе \"в процессе\":"))