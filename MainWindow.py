# -*- coding: utf-8 -*-
import sys
import socket
import os
import sqlite3
from new_wind import Ui_Dialog
from PyQt5.QtGui import *
from PyQt5.QtWidgets import  *
from PyQt5.QtCore import *
from struct import unpack


def client_program():
    host = socket.gethostname()  # as both code is running on same pc
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    return client_socket

def get_information(client, inf):
    client.send(inf.encode())
    data = client.recv(4096).decode()
    data = data.split(';')
    return data



class MainWindow(QMainWindow, Ui_Dialog):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("DnD")
        self.k = {"1": "1 монстр",
             '1.5': "2 монстра",
             '2': "3-6 монстра",
             '2.5': "7-11 монстров",
             "3": "12-14 монстров",
             "4": "от 15 монстров "}

        self.players_count = []
        self.players = 10
        self.levels = 20
        self.rb = 0
        self.client = client_program()
        self.monsters_text = ['Название: ', "\nКласс доспеха: ", "\nХиты: ", '\nСила: ', ' Ловкость: ',
                              " Телосложение: ",
                              " Интеллект: ", " Мудрость: ", " Харизма: ", "\nДействие: ", "\nРеакция: ", "\nОписание:"]

        self.setupUi(self)

        self.pushButton.pressed.connect(self.correct_players)
        self.pushButton_2.pressed.connect(self.information_from_user)
        self.pushButton_3.pressed.connect(self.show_mon_inf_from_server)
        self.pushButton_4.pressed.connect(self.delete_players)
        self.show()


    def delete_players(self):
        if self.players_count !=[]:
            self.textBrowser_2.clear()
            self.players_count = []
            self.players = 10
    def information_from_user(self):
        if self.radioButton.isChecked():
            self.rb = 1
        if self.radioButton_2.isChecked():
            self.rb = 4
        if self.radioButton_3.isChecked():
            self.rb = 3
        if self.radioButton_4.isChecked():
            self.rb = 2
        if ((self.players_count !=[]) and (self.rb!=0)):
            information = ''
            gamer = []
            levels = []
            for i in self.players_count:
                gamer.append(str(i[0]))
                levels.append(str(i[1]))
            gamer = ",".join(gamer)
            levels = ",".join(levels)
            information = f"1;{gamer};{levels};{str(self.rb)}"
            inf = get_information(self.client, information)
            self.update_inf_listwidget(inf)

    def correct_players(self):
        name = str(self.lineEdit.text())
        level = str(self.lineEdit_2.text())
        if name == '':
            QMessageBox.question(self, 'Error', 'Выбирите Количество игроков', QMessageBox.Ok)
        else:
            if not (name.isdigit()):
                QMessageBox.question(self, 'Error', 'Количество игроков численное', QMessageBox.Ok)
            else:
                try:
                    if not(0 < int(name) <= self.players):
                        QMessageBox.question(self, 'Error', 'Количество игроков меньше 0 или больше 10', QMessageBox.Ok)
                except:
                    pass

        if level == '':
            QMessageBox.question(self, 'Error', 'Введите уровень', QMessageBox.Ok)
        else:
            if not (level.isdigit()):
                QMessageBox.question(self, 'Error', 'Уровень-число', QMessageBox.Ok)
            else:
                  if not(0 < int(level) <= 20):
                    QMessageBox.question(self, 'Error', 'Уровень больше 20  ил уровень меньше 1', QMessageBox.Ok)
                  else:
                      self.players_count.append([name, level])
                      self.players -= int(name)
        self.show_players()

    def show_players(self):
        text = ''
        for player in self.players_count:
            text += f'Количество игроков: {player[0]} Уровень: {player[1]}\n'
        self.textBrowser_2.setText(text)

    def update_inf_listwidget(self, inf):
        self.listWidget.clear()
        for i in range(len(inf)):
            monster = inf[i].split(',')
            monsters_count = self.k[monster[1]]
            self.listWidget.insertItem(i+1, f"{monsters_count} с опытом {monster[0]}")

    def show_mon_inf_from_server(self):
        item = self.listWidget.currentItem()
        if item !=None:
            item = item.text().split()[4]
            inf = send_monsters_information(item)
            self.textBrowser.clear()
            data = ''
            for i in range(len(inf)):
                if inf[i] != None and i !=0 and i != len(inf) - 1:
                    data += f'{self.monsters_text[i-1]} {inf[i]}'
            self.textBrowser.setPlainText(data)




def send_monsters_information(score):
    inf = ''
    con = sqlite3.connect("monsters.db")
    cur = con.cursor()
    sql_select = "SELECT * FROM monsters WHERE weight = ? ORDER BY RANDOM() LIMIT 1  "
    cur.execute(sql_select, (score, ))
    rec = cur.fetchall()[0]
    return rec


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    app.exec_()