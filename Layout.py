# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets
from multi_Thread import Thread

class GUI(QtWidgets.QWidget):

    def __init__(self, parent = None):
        super().__init__(parent)
        
        self.Thread_List = []      #初始化時指派一個線程
        self.progress_bar = []
        self.date_string = ""
        self.like_count = 0
        self.Thread_count = 0
        self.arrange = False   #檢查此次的輸入是否有排入線程中

        self.layout = QtWidgets.QFormLayout()
        self.Label1 = QtWidgets.QLabel("date_Input")
        self.date_Input = QtWidgets.QLineEdit()
        self.layout.addRow(self.Label1, self.date_Input)

        self.Label2 = QtWidgets.QLabel("Push_Count")
        self.good_Input = QtWidgets.QLineEdit()
        self.layout.addRow(self.Label2, self.good_Input)

        self.btn2 = QtWidgets.QPushButton('Ok')
        self.btn2.clicked.connect(self.grab)
        self.layout.addRow(self.btn2)

        self.setLayout(self.layout)
        self.setWindowTitle("Practice")
        self.setGeometry(150, 150, 250, 500)

    def grab(self):             #多線程處理
    
        print("Get process!")
        self.date_string = self.date_Input.text()
        self.like_count = int(self.good_Input.text())
        self.arrange = False
        self.Thread_count += 1
        self.check()


    def check(self):
        
        if self.like_count < 0:
            print("Invalid input")
            return None

        for Threads in self.Thread_List:
            if not Threads.isRunning():
                self.arrange = True
                Threads.set(self.date_string, self.like_count, self.Thread_count)
                Threads.start()
                break

        if not self.arrange:
            if len(self.Thread_List) <= 10:
                self.Thread_List.append(Thread())                    #新增一個Thread到最後面
                self.Thread_List[-1].set(self.date_string, self.like_count, self.Thread_count)
                self.layout.addRow(self.Thread_List[-1].progress_bar)
                self.Thread_List[-1].start()                         #將最後一個Thread指派程序
            else:
                print("Out of Process")