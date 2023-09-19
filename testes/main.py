from PyQt5 import QtCore
from testee import *
from PyQt5.QtCore import  QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow
from datetime import datetime

modo = 0 #modo == 1 (modo automático) modo == 2 (modo programado)
x = 0

class teste (QMainWindow):
#-----------------------------INICIALIZAÇÃO---------------------------------
    def __init__(self,*args,**argvs):
        super(teste,self).__init__(*args,**argvs)
        self.ui = Ui_home()
        self.ui.setupUi(self)
        self.ui.pb_configure.clicked.connect(self.abrir_tela_config)
        self.ui.pb_voltar.clicked.connect(self.abrir_tela_home)
        self.ui.qr_enable_prog.clicked.connect(self.prog_on)
        self.ui.qr_enable_auto.clicked.connect(self.auto_on)
        self.ui.pb_confirma_auto.clicked.connect(self.set_percent)
        self.ui.te_prog.timeChanged.connect(self.get_time)
        self.ui.te_ledON.timeChanged.connect(self.get_time_led1)
        self.ui.te_ledOFF.timeChanged.connect(self.get_time_led2)
        self.ui.pb_confirma_prog.clicked.connect(self.modo_prog)
        self.ui.pb_confirma_led.clicked.connect(self.led)
        self.update_imgvaso()
        self.update_labelnivel()
        self.horario()
        self.first_time()
    
        
    def first_time(self):
        global x
        if x == 0:
            self.ui.cb_percent.setDisabled(True)
            self.ui.pb_confirma_prog.setDisabled(True)
            self.ui.te_prog.setDisabled(True)
            self.ui.pb_confirma_prog.setDisabled(True)
            
         
#-----------------------------TROCAR DE TELAS---------------------------------        
    def abrir_tela_config(self):
         self.ui.stackedWidget.setCurrentWidget(self.ui.MyConfig)

    def abrir_tela_home(self):
         self.ui.stackedWidget.setCurrentWidget(self.ui.MyHome)


#-----------------------------RADIOS BUTTONS---------------------------------
    def auto_on(self):
        if self.ui.qr_enable_auto.isChecked():
            global modo
            global x
            x = 2
            self.ui.te_prog.setEnabled(False)
            self.ui.pb_confirma_prog.setEnabled(False)
            self.ui.qr_enable_prog.setChecked(False)
            self.ui.cb_percent.setEnabled(True)
            self.ui.pb_confirma_auto.setEnabled(True)
            modo = 1
            self.modo_auto()

   
    def prog_on(self):
        global modo
        if self.ui.qr_enable_prog.isChecked():
            x = 2
            self.ui.te_prog.setEnabled(True)
            self.ui.pb_confirma_prog.setEnabled(True)
            self.ui.qr_enable_auto.setChecked(False)
            self.ui.cb_percent.setEnabled(False)
            self.ui.pb_confirma_auto.setEnabled(False)
            modo = 2
            
                        

#-----------------------------ATUALIZAÇÃO DE LABELS DA TELA HOME---------------------------------

#----------------------NIVEL----------------------

    def update_labelnivel(self):
        self.work_nivel = Work_nivel()
        self.work_nivel.start()
        self.work_nivel.valueChanged.connect(self.update_labelnivel_slot)

    def update_labelnivel_slot(self):
        if self.work_nivel.value_nivel == 0:
            self.ui.label_tanque__dado.setText("Vazio")
        elif self.work_nivel.value_nivel == 1:
            self.ui.label_tanque__dado.setText("Cheio")
        else:
            self.ui.label_tanque__dado.setText("Erro")

#----------------------UMIDADE----------------------

    def update_imgvaso(self):
        self.work_umidade = Work_umidade()
        self.work_umidade.start()
        self.work_umidade.valueChanged1.connect(self.update_imgvaso_slot)
    
    def update_imgvaso_slot(self):
        if self.work_umidade.value_umidade < 3700:
            self.ui.img_vaso.setPixmap(QtGui.QPixmap("imagens png - vaso inteligente Ocean/vaso feliz.png"))
        #else:
            self.ui.img_vaso.setPixmap(QtGui.QPixmap("imagens png - vaso inteligente Ocean/vaso_triste .png"))
        self.converte_to_percent()
        self.ui.label_US_dado.setText("{}".format(int(self.umidade)))

#------------------------------MODO AUTOMÁTICO---------------------------------

    def modo_auto(self):
        self.work_check_auto = Work_check_auto()
        self.work_check_auto.start()
        self.work_check_auto.valueChanged.connect(self.modo_auto_slot)
        global modo
    
    @QtCore.pyqtSlot()
    def modo_auto_slot(self):
        if modo == self.work_check_auto.mod:
            try:
                if self.umidade < self.percent:
                    print("Precisa acionar motor, umidade baixa")
                else:
                    print("Não precisa acionar motor, umidade alta")
            except:
                pass
        
     
    def set_percent(self):
        try:
            self.percent = self.ui.cb_percent.currentText()
            self.percent = self.percent.replace("%","")
            self.percent = int(self.percent)
            print(self.percent)
            self.modo_auto()
        except:
            pass

    def converte_to_percent(self):
        self.umidade = (self.work_umidade.value_umidade / 4095) * 100
        pass
#------------------------------MODO PROGRAMADO---------------------------------

    def modo_prog(self):
        global modo
        self.work_check_prog =Work_check_prog()
        self.work_check_prog.start()
        print('09')
        self.work_check_prog.valuechanged.connect(self.modo_prog_slot)
    
    def modo_prog_slot(self):
        if modo == self.work_check_prog.mod:
            
            self.ui.label_PI_dado.setText(f"{self.hora}:{self.min}")
            if self.work_horario.hora_atual == self.hora and self.work_horario.min_atual == self.min:
                print('Horário programado, regar!')
                self.ui.label_UI_dado.setText(f"{self.hora}:{self.min}")
            else:
                print("Ainda nao estamos no horário")
            
               

    def get_time(self):
        self.time = self.ui.te_prog.time()
        self.time = self.time.toString()
        self.hora = self.time[0:2]
        self.min = self.time[3:5]
        # print(self.hora)
        # print(self.min)
   
    def horario(self):
        self.work_horario = Work_horario()
        self.work_horario.start()
        self.work_horario.valueChanged.connect(self.set_horario_slot)

    def set_horario_slot(self):
        self.work_horario.hora_atual = str(self.work_horario.hora_atual)
        self.work_horario.min_atual = str(self.work_horario.min_atual)
        pass

#----------------------------LED-------------------------------------------------
    def get_time_led1(self):
        self.time_led1 = self.ui.te_ledON.time()
        self.time_led1 = self.time_led1.toString()
        self.hora_led1 = self.time_led1[0:2]
        self.min_led1 = self.time_led1[3:5]    
        print(self.hora_led1)
        print(self.min_led1)
        

    def get_time_led2(self):
        self.time_led2 =self.ui.te_ledOFF.time()
        self.time_led2 = self.time_led2.toString()   
        self.hora_led2 = self.time_led2[0:2]
        self.min_led2 = self.time_led2[3:5]
        print(self.hora_led2)
        print(self.min_led2)

    def led(self):
        self.work_check_led = Work_check_led()
        self.work_check_led.start()
        self.work_check_led.valuechanged.connect(self.led_slot)

#aqui
    def led_slot(self):
        if self.work_horario.hora_atual == self.hora_led1 and self.work_horario.min_atual == self.min_led1:
            print("Ligar led")
        if self.work_horario.hora_atual == self.hora_led2 and self.work_horario.min_atual == self.min_led2:
            print("Desligar led")
        else: 
            print('Nao está no horário')


#-----------------------------THREADS---------------------------------
     
class Work_nivel(QThread):
    valueChanged = pyqtSignal(int)
    def __init__(self):
        super().__init__()
        self.running = False
        
    
    def run(self):
        self.running = True
        while self.running:
            global Nivel
            self.value_nivel = 1 #gpio.input(Nivel)
            self.valueChanged.emit(self.value_nivel)
            self.msleep(1000)

    
    def stop(self):
        self.running = False
   
class Work_horario(QThread):
    valueChanged = pyqtSignal(int)
    valueChanged1 = pyqtSignal(int)
    
    def __init__(self):
        super().__init__()
        self.running = False
        
    
    def run(self):
        self.running = True
        while self.running:
            horario_atual = datetime.now()
            self.hora_atual = horario_atual.hour
            self.min_atual = horario_atual.minute
            self.valueChanged.emit(self.hora_atual)
            self.valueChanged1.emit(self.min_atual) 
            self.msleep(1000)

    
    def stop(self):
        self.running = False

class Work_umidade(QThread):
    valueChanged1 = pyqtSignal(int)
        
    def run(self):
        self.running = True
        while self.running:
            #GPIO.output(CS_ADC, GPIO.LOW)
            self.value_umidade = 300
            #print(self.value_umidade)
            self.valueChanged1.emit(self.value_umidade)
            self.msleep(1000)
            #GPIO.output(CS_ADC, GPIO.HIGH)
            #if value < 3700:
                #self.label_11.setPixmap(QtGui.QPixmap(":/teste/imagens png - vaso inteligente Ocean/vaso feliz.png"))

            #else:
                #elf.label_11.setPixmap(QtGui.QPixmap(":/teste/imagens png - vaso inteligente Ocean/vaso triste .png"))
            #self.valueChanged.emit(value)
            pass
    
    def stop(self):
        self.running = False

class Work_check_auto(QThread):
    valueChanged = pyqtSignal(int)
        
    def run(self):
        self.running = True
        while self.running:
            self.mod = 1
            self.valueChanged.emit(self.mod)
            self.msleep(1000)
            pass
    
    def stop(self):
        self.running = False

class Work_check_prog(QThread):
    valuechanged = pyqtSignal(int)
    def run(self):
        self.running = True
        while self.running:
            self.mod = 2
            self.valuechanged.emit(self.mod)
            self.msleep(1000)
            pass
    
    def stop(self):
        self.running = False

class Work_check_led(QThread):
    valuechanged = pyqtSignal(int)
    def run(self):
        self.running = True
        while self.running:
            self.mod = 1
            self.valuechanged.emit(self.mod)
            self.msleep(1000)
            pass
    
    def stop(self):
        self.running = False

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = teste()
    ui.show()
    sys.exit(app.exec_())