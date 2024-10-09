# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
# import run
from parser1 import parser1 
from parser2 import parser2
import subprocess
import sys

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(741, 494)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(90, 230, 511, 41))
        self.pushButton.setObjectName("pushButton")
        
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setGeometry(QtCore.QRect(90, 190, 511, 31))
        self.checkBox.setObjectName("checkBox")
        
        self.dateEdit = QtWidgets.QDateEdit(self.centralwidget)
        self.dateEdit.setGeometry(QtCore.QRect(90, 150, 141, 31))
        self.dateEdit.setObjectName("dateEdit")
        
        self.dateEdit_2 = QtWidgets.QDateEdit(self.centralwidget)
        self.dateEdit_2.setGeometry(QtCore.QRect(250, 150, 141, 31))
        self.dateEdit_2.setObjectName("dateEdit_2")
        
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(92, 90, 511, 41))
        self.lineEdit.setText("Ведите текст для поиска")
        self.lineEdit.setObjectName("lineEdit")
        
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(90, 30, 511, 41))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItems(['Все сайты', 'КС РФ', "ВС РФ"])
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 741, 22))
        self.menubar.setObjectName("menubar")
        
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        # Подключение кнопки к методу
        self.pushButton.clicked.connect(self.on_button_clicked)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Поиск"))
        self.checkBox.setText(_translate("MainWindow", "Создать общий файл"))

    # Метод, который будет выполняться при нажатии на кнопку
    def on_button_clicked(self):
        # Получаем выбранные даты
        start_date = self.dateEdit.date().toString("dd.MM.yyyy")
        end_date = self.dateEdit_2.date().toString("dd.MM.yyyy")
        
        # Получаем текст из lineEdit
        line_edit_text = self.lineEdit.text()
        
        # Получаем выбранный элемент из comboBox
        selected_option = self.comboBox.currentText()
        
        # Получаем состояние checkBox
        check_box_state = self.checkBox.isChecked()

        # Выводим собранные данные
        print("Даты:")
        print(f"Начальная дата: {start_date}")
        print(f"Конечная дата: {end_date}")
        print(f"Текст в lineEdit: {line_edit_text}")
        print(f"Выбранный вариант: {selected_option}")
        print(f"Состояние checkBox (выбран): {check_box_state}")



        required_packages = [
            'selenium',
            'python-docx'
        ]

        # Функция для установки пакетов
        def install(package):
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

        # Установка всех необходимых пакетов
        for package in required_packages:
            install(package)

        print("Все библиотеки установлены. Теперь запускаем основной код...")

        if selected_option == 'Все сайты':
            if check_box_state:
                parser1(line_edit_text,start_date,end_date, 'add_to_file')
                parser2(line_edit_text,start_date,end_date, 'add_to_file')
            else:
                parser1(line_edit_text,start_date,end_date, 'make_new_file')
                parser2(line_edit_text,start_date,end_date, 'make_new_file')
        elif selected_option == 'КС РФ':
            parser1(line_edit_text,start_date,end_date, 'make_new_file')
        elif selected_option == 'ВС РФ':
            parser2(line_edit_text,start_date,end_date, 'make_new_file')

        





if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
