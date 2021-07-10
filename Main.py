# -*- coding: utf-8 -*-

import sys
from PyQt5 import QtWidgets
from Layout import GUI

def main():
    app = QtWidgets.QApplication(sys.argv)
    example = GUI()
    example.show()
    app.exec_()
    
if __name__ == '__main__':
    main()