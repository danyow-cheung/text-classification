import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication
from MainWindow import Ui_MainWindow
from predict import predict_main

# 加载.ui文件
qt_file = "template.ui"
Form, Window = uic.loadUiType(qt_file)

def write_text(text):
    with open("data/test_goods.txt","a",encoding='utf-8') as f:
        f.write(text+'\n')
        print("寫入成功")

def clear_txt():
    with open("data/test_goods.txt","w",encoding='utf-8') as f:
        f.write("")
        print("重置成功")

class MyWindow(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self):
        #QtWidgets.QMainWindow.__init__(self)
        QtWidgets.QDialog.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.calc_laebl_button.clicked.connect(self.clasify_text)

    def clasify_text(self):
        # 獲取內容
        text = self.text_box.text()
        print('获取到的输入',text)
        if text =='':
            content = '请输入'
            total_price_string = "{}".format(content)
        else:
            # 寫入文件
            write_text(text)
            # 調用預測函數
            output = predict_main()
            # 存儲結果
            label_output = []
            for i in output:
                label_output.append(i)

            if label_output[-1] == 1:
                content = "負面"
            else:
                content='正面'
            total_price_string = "預測類別為: {}".format(content)
        self.results_output.setText(total_price_string)

# 展示
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())

