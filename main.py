import sys 
from PyQt5.QtWidgets import QMainWindow,QApplication
from PyQt5.QtGui import QColor
import pyvisa
import subprocess
from UI_SCPI_Terminal import Ui_MainWindow 

import resources_rc

class MiApp(QMainWindow):
	def __init__(self):
		super().__init__()
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)

		self.update_instruments_list()
		self.load_list_commands()

		#Events
		self.ui.pushButton_send.clicked.connect(self.send_data)
		self.ui.pushButton_refresh.clicked.connect(self.update_instruments_list)
		self.ui.pushButton_clean.clicked.connect(self.clear_terminal)
		self.ui.lineEdit_data.returnPressed.connect(self.send_data)
		self.ui.pushButton_help.clicked.connect(self.open_help)
		self.ui.pushButton_pass_command.clicked.connect(self.pass_command)

	def pass_command(self):
		self.ui.lineEdit_data.clear()
		self.ui.lineEdit_data.setText(self.ui.comboBox_commands_list.currentText())
		

	def load_list_commands(self):
		temp = open("commands_SCPI.txt",'r').read().split('\n')
		self.ui.comboBox_commands_list.clear()
		self.ui.comboBox_commands_list.addItems(temp)

	def open_help(self):
		path = 'FPC_UserManual.pdf'
		subprocess.Popen([path], shell=True)

	def update_terminal(self,data):
		self.ui.textBrowser_terminal_view.setTextColor(QColor.fromRgb(255,255,255))
		self.ui.textBrowser_terminal_view.append('<<' + ' ' + data)

	def send_data(self):
		try:

			rm = pyvisa.ResourceManager()
			inst = rm.open_resource(self.ui.comboBox_instruments_list.currentText())
			result = ""
			data = self.ui.lineEdit_data.text()
			if(data.count("?") > 0):
				result = inst.query(data)
			else:
				inst.write(data)
			
			self.ui.textBrowser_terminal_view.setTextColor(QColor.fromRgb(50,50,50))
			self.ui.textBrowser_terminal_view.append('>>' + ' ' + data)

			self.ui.textBrowser_terminal_view.setTextColor(QColor.fromRgb(38, 175, 155))
			self.ui.textBrowser_terminal_view.append('<<' + ' ' + result)
			inst.close()
		
		except:

			result = "Error ocurred"
			self.ui.textBrowser_terminal_view.setTextColor(QColor.fromRgb(200, 50, 50))
			self.ui.textBrowser_terminal_view.append('<<--' + ' ' + result + ' ' + '-->>')
		

	def update_instruments_list(self):
		rm = pyvisa.ResourceManager()
		list = rm.list_resources()
		self.ui.comboBox_instruments_list.clear()
		self.ui.comboBox_instruments_list.addItems(list)

	def clear_terminal(self):
		self.ui.textBrowser_terminal_view.clear()

	def closeEvent(self,e):
		pass

if __name__ == '__main__':
	app = QApplication(sys.argv)
	w = MiApp()
	w.show()
	sys.exit(app.exec_())