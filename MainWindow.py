# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        # 主窗口命名
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(328, 273)
        # 主窗口容器初始化
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        # 主窗口容器命名为centralwidget
        self.centralwidget.setObjectName("centralwidget")
        # 佈局類
        self.formLayout = QtWidgets.QFormLayout(self.centralwidget)
        self.formLayout.setObjectName("formLayout")

        # QLabel用于显示文本或图像。不提供用户交互功能。
        # 标签的视觉外观可以通过多种方式进行配置，
        # 并且可以用于为另一个小部件指定焦点助记键。
        self.label_3 = QtWidgets.QLabel(self.centralwidget)

        # 字體
        font = QtGui.QFont()
        font.setPointSize(28)
        font.setBold(True)
        font.setWeight(75)
        # label類同意字體
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        # 
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.SpanningRole, self.label_3)
        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(15)
        # 類別
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label)
        # 輸入
        self.text_box = QtWidgets.QLineEdit(self.centralwidget)
        self.text_box.setObjectName("text_box")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.text_box)
        
        # 按鈕設置
        self.calc_laebl_button= QtWidgets.QPushButton(self.centralwidget)
        self.calc_laebl_button.setObjectName("calc_laebl_button")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.calc_laebl_button)

        # 輸出类
        self.results_output = QtWidgets.QLabel(self.centralwidget)
        # 预计输出内容
        self.results_output.setText("")
        self.results_output.setObjectName("results_output")
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.SpanningRole, self.results_output)
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        # 为小组件，布局等命名
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_3.setText(_translate("MainWindow", "電商評論 情感分析"))

        self.label.setText(_translate("MainWindow", "輸入"))
        self.calc_laebl_button.setText(_translate("MainWindow", "確認"))


