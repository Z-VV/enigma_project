import sys
import time
import requests
import time
from datetime import datetime
from datetime import timedelta
from localhost import Connector
from tkinter import messagebox
from tkinter import *
import os
import shutil
from distutils.dir_util import copy_tree
from os import remove
from sys import argv
import unknown_support
import pandas as pd
import traceback


try:
    base_dir = os.path.dirname(os.path.realpath(__file__))
    check_dir = base_dir.replace('enigma','')+'MQL4\\Include\\Zmq'
    if not os.path.exists(check_dir):
        os.mkdir(base_dir.replace('enigma','')+'MQL4\\Include\\Zmq')
        os.mkdir(base_dir.replace('enigma', '') + 'MQL4\\Include\\Mql')
        copy_tree('Zmq',base_dir.replace('enigma','')+'MQL4\\Include\\Zmq')
        copy_tree('Mql', base_dir.replace('enigma', '') + 'MQL4\\Include\\Mql')
        shutil.copy('libsodium.dll',base_dir.replace('enigma', '') + 'MQL4\\Libraries')
        shutil.copy('libzmq.dll', base_dir.replace('enigma', '') + 'MQL4\\Libraries')
        shutil.copy('enigma.ex4', base_dir.replace('enigma', '') + 'MQL4\\Experts')
except:
    pass
if not os.path.exists('signal_numbers.txt'):
    open("signal_numbers.txt", 'w').close()

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True
    
def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root,top
    root = tk.Tk()
    root.attributes('-alpha', 0.9)
    top = Toplevel1 (root)
    unknown_support.init(root, top)
    Run().conf_token_label()
    root.after(5000,Run().scanning)
    root.mainloop()

w = None
def create_Toplevel1(rt, *args, **kwargs):
    '''Starting point when module is imported by another module.
       Correct form of call: 'create_Toplevel1(root, *args, **kwargs)' .'''
    global w, w_win, root
    #rt = root
    root = rt
    w = tk.Toplevel (root)
    top = Toplevel1 (w)
    unknown_support.init(w, top, *args, **kwargs)
    return (w, top)

def destroy_Toplevel1():
    global w
    w.destroy()
    w = None

    
class Toplevel1:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#ececec' # Closest X11 color: 'gray92'
        font9 = "-family {Yu Gothic UI Light} -size 9 -slant italic"
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.',background=_bgcolor)
        self.style.configure('.',foreground=_fgcolor)
        self.style.configure('.',font="TkDefaultFont")
        self.style.map('.',background=
            [('selected', _compcolor), ('active',_ana2color)])

        top.geometry("385x240+966+182")
        top.minsize(148, 1)
        top.maxsize(1924, 1055)
        top.resizable(0,0)
        top.title("enigma")
        top.configure(borderwidth="5")
        top.configure(background="#2a2a2a")
        top.configure(cursor="arrow")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="black")
        
        self.Frame1 = tk.Frame(top)
        self.Frame1.place(relx=0.003, rely=0, relheight=1.021
                , relwidth=0.997)
        self.Frame1.configure(relief='ridge')
        self.Frame1.configure(borderwidth="2")
        self.Frame1.configure(relief="ridge")
        self.Frame1.configure(background="black")
        self.Frame1.configure(highlightbackground="#00b7b7")
        self.Frame1.configure(highlightcolor="#828282")
        self.Frame1.configure(pady="15")
        self.Frame1.configure(takefocus="30")

        self.Frame2 = tk.Frame(self.Frame1)
        self.Frame2.place(relx=0.005, rely=-0.03, relheight=1.05, relwidth=0.99)

        self.Frame2.configure(relief='groove')
        self.Frame2.configure(borderwidth="2")
        self.Frame2.configure(relief="groove")
        self.Frame2.configure(background='black')#"#828282")

        self.Label2 = tk.Label(self.Frame2)
        self.Label2.place(relx=0.034, rely=0.091, height=22, width=64)
        self.Label2.configure(background="#5f5f5f")
        self.Label2.configure(disabledforeground="#a3a3a3")
        self.Label2.configure(foreground="#c3c3c3")
        self.Label2.configure(relief="groove")
        self.Label2.configure(text='''TOKEN''')

        self.Entry1 = tk.Entry(self.Frame2)
        self.Entry1.place(relx=0.213, rely=0.091,height=24, relwidth=0.695)
        self.Entry1.configure(background="#313131")
        self.Entry1.configure(disabledforeground="#a3a3a3")
        self.Entry1.configure(font="TkFixedFont")
        self.Entry1.configure(foreground="#1c1c1c")
        self.Entry1.configure(insertbackground="black")
        self.Entry1.bind("<Button-3>", RightClicker)

        self.object = Run()

        self.Button1 = tk.Button(self.Frame2,command=self.object.button_press)
        self.Button1.place(relx=0.095, rely=0.766, height=33, width=306)
        self.Button1.configure(activebackground="#ececec")
        self.Button1.configure(activeforeground="#000000")
        self.Button1.configure(background="#686868")
        self.Button1.configure(disabledforeground="#a3a3a3")
        self.Button1.configure(foreground="#000000")
        self.Button1.configure(highlightbackground="#d9d9d9")
        self.Button1.configure(highlightcolor="black")
        self.Button1.configure(pady="0")
        self.Button1.configure(text='''Connect''')

        self.Label3 = tk.Label(self.Frame2)
        self.Label3.place(relx=0.55, rely=0.255, height=23, width=147)
        self.Label3.configure(background="#686868")
        self.Label3.configure(disabledforeground="#a3a3a3")
        self.Label3.configure(foreground="#000000")
        self.Label3.configure(text='''Server''')

        self.Label4 = tk.Label(self.Frame2)
        self.Label4.place(relx=0.55, rely=0.38, height=23, width=147)
        self.Label4.configure(background="#686868")
        self.Label4.configure(disabledforeground="#a3a3a3")
        self.Label4.configure(foreground="#000000")
        self.Label4.configure(text='''MT4''')

        self.TSeparator2 = ttk.Separator(self.Frame2)
        self.TSeparator2.place(relx=-0.039, rely=0.639, relwidth=1.137)

        self.spinbox = Spinbox(self.Frame2, from_=0.01, to=1,increment=0.01)
        self.spinbox.configure(background="#686868")
        self.spinbox.place(relx=0.169, rely=0.25, height=23, width=40)

        self.spinLabel = tk.Label(self.Frame2)
        self.spinLabel.place(relx=0.032, rely=0.25, height=23, width=48)
        self.spinLabel.configure(background="#686868",text='Lot Size:')

    def Label_Create(self):
        self.Button1 = tk.Label(self.Frame2)
        self.Button1.place(relx=0.095, rely=0.766, height=33, width=306)
        self.Button1.configure(background="#519c98")
        self.Button1.configure(disabledforeground="#a3a3a3")
        self.Button1.configure(foreground="#000000")
        self.Button1.configure(pady="0")
        self.Button1.configure(text='''CONNECTED''')

        self.spinbox.destroy()
        self.Entry1.destroy()

        self.spinLabel.configure(text='Lot Size: '+str(self.object.lot_size), background="#519c98")
        self.spinLabel.place(relx=0.03, rely=0.25, height=23, width=80)


class RightClicker:
    def __init__(self, e):
        commands = ["Cut","Copy","Paste"]
        menu = tk.Menu(None, tearoff=0, takefocus=0)
        menu.configure(background="#686868")
        for txt in commands:
            menu.add_command(label=txt, command=lambda e = e, txt=txt:self.click_command(e,txt))
        menu.tk_popup(e.x_root + 40, e.y_root + 10, entry="0")

    def click_command(self, e, cmd):
        e.widget.event_generate(f'<<{cmd}>>')


class Run:
    def __init__(self):
        self.signal_url = 'https://enigma-lab.herokuapp.com/api/signals/?format=json'
        self.report_url = 'https://enigma-lab.herokuapp.com/api/reports/'
        self.token = None
        self.token_is_valid = None
        self.running = False
        self.zmq = None
        self.response = None
        self.MT_is_connected = False
        self.server_is_connected = False
        self.status_label_create = True
        self.lot_size = None

    def get_token(self):
        self.token = top.Entry1.get()
        self.lot_size = top.spinbox.get()
        print(self.lot_size)
        print(self.token)
        if len(self.token) == 0:
            try:
                with open('token.txt', 'r') as file:
                    lines = file.readlines()
                    file.close()
                    self.token = lines[0]
                    self.headers = {'Authorization': 'Token ' + str(self.token)}
                    self.conf_token_label()
                    return True
            except:
                with open('token.txt', 'w') as file:
                    file.close()
                    messagebox.showerror('error',
                                         message='On the first use of the App ,you have to enter a Valid Token! !')
        elif len(self.token) == 40:
            with open('token.txt', 'w') as file:
                file.write(self.token)
                file.close()
            self.headers = {'Authorization': 'Token ' + str(self.token)}
            self.conf_token_label()
            return True
        else:
            messagebox.showerror('error', message='Please enter valid Token !')
        self.conf_token_label()

    def conf_token_label(self):
        with open('token.txt', 'r')as f:
            lines = f.readlines()
            print(lines)
            f.close()
            if len(lines) != 0:
                token = lines[0]
                if len(token) == 40 and token_is_valid:
                    top.Label2.configure(foreground='#519c98')
                else:
                    top.Label2.configure(foreground='#cf305d')
            else:
                top.Label2.configure(foreground='#cf305d')

    def button_press(self):
        if self.get_token():
            if self.server_initial_connect():
                if self.mt_initial_connect():
                    self.scanning()

    def send_report(self, text):
        data = {'text': text}
        print(requests.post(url=self.report_url, data=data, headers=self.headers))

    def server_initial_connect(self):
        try:
            self.response = requests.get(url=self.signal_url, headers=self.headers).json()
            print(self.signal_url)
            print(self.headers)
            print(self.response)
        except:
            messagebox.showerror('error', message='No connection to the Server !')
            top.Label3.configure(background='#cf305d')
            self.response = {}
        if 'detail' in self.response:
            if self.response['detail'] == 'Invalid token.':
                messagebox.showerror('error', message='Invalid Token ! Please contact the "Supplier" !')
                top.Label3.configure(background='#cf305d')
                top.Label2.configure(foreground='#cf305d')
                self.token_is_valid = False
                self.send_report(str(self.response)+self.token)
                return False
            if self.response['detail'] == 'Invalid token header. No credentials provided.':
                messagebox.showerror('error', message='Please enter a valid Token !')
                top.Label3.configure(background='#cf305d')
                top.Label2.configure(foreground='#cf305d')
                self.token_is_valid = False
                self.send_report(str(self.response) + self.token)
                return False
        if len(self.response) > 1:
            self.token_is_valid = True
            if 'symbol' in self.response[-1]:
                try:
                    print(self.response[-1]['symbol'])
                    top.Label3.configure(background="#519c98")
                    self.send_report('Connected with the Server!')
                    return True
                except:
                    self.send_report('Line 320 Exception!'+str(self.response)+str(traceback.print_exc()))
            else:
                top.Label3.configure(background='#cf305d')
                self.send_report('Line 323'+str(self.response)+str(traceback.print_exc()))

    def mt_initial_connect(self):
        try:
            self.zmq = Connector()
            self.zmq._DWX_MTX_GET_ALL_OPEN_TRADES_()
            time.sleep(1)
            mt_response = self.zmq._get_response_()
            print(mt_response)
            if mt_response['_action'] == 'OPEN_TRADES':
                top.Label4.configure(background='#519c98')
                top.Button1.configure(background='#519c98')
                self.send_report('Connected with METATRADER !' + str(mt_response))
                self.running = True
                return True
            else:
                top.Label4.configure(background='#cf305d')
                self.zmq._DWX_ZMQ_SHUTDOWN_()
                messagebox.showerror('error', message='No connection with METATRADER !')
                self.send_report('No connection with METATRADER !'+str(mt_response))
        except:
            traceback.print_exc()
            self.zmq._DWX_ZMQ_SHUTDOWN_()
            top.Label4.configure(background='#cf305d')
            messagebox.showerror('error', message='No connection with METATRADER !')
            self.send_report('No connection with METATRADER ! Line 346!'+str(traceback.print_exc()))

    def scanning(self):
        if self.running:
            self.Loop()
        root.after(10000, self.scanning)

    def server_response_read(self):
        if len(self.response) <= 3:
            number_scanned_signals = len(self.response)
        else:
            number_scanned_signals = 4
        for x in range(1, number_scanned_signals):
            signal_date_str = self.response[-x]['created'].split('T')[0]
            signal_time_str = self.response[-x]['created'].split('T')[1].replace('Z', '').split('.')[0]
            dt_signal_time = datetime.strptime(signal_date_str + ' ' + signal_time_str, '%Y-%m-%d %H:%M:%S')
            time_difference = datetime.utcnow() - dt_signal_time
            if time_difference <= timedelta(minutes=5):
                print(-x)
                print(self.response[-x])
                with open('signal_numbers.txt', 'r') as file:
                    lines = file.readlines()
                    for i in range(0, len(lines)):
                        lines[i] = int(lines[i])
                    print(lines)
                    file.close()

                number = int(self.response[-x]['number'])

                if number not in lines or len(lines) == 0:
                    print('YES')
                    new_dic = {}
                    print(self.response[-x]['signal_type'])
                    print(self.response[-x]['symbol'])
                    print(self.response[-x]['buy_sell'])
                    print(self.response[-x]['stop_loss'])
                    print(self.response[-x]['take_profit'])

                    signal_type = self.response[-x]['signal_type']
                    symbol = self.response[-x]['symbol']
                    buy_sell = self.response[-x]['buy_sell']
                    stop_loss = int(self.response[-x]['stop_loss'])
                    take_profit = int(self.response[-x]['take_profit'])
                    provider = int(self.response[-x]['provider'])
                    with open('signal_numbers.txt', 'a') as file:
                        file.write(str(number) + '\n')
                        file.close()

                    new_dic['signal_type'] = signal_type
                    new_dic['symbol'] = symbol
                    new_dic['buy_sell'] = buy_sell
                    new_dic['stop'] = stop_loss
                    new_dic['limit'] = take_profit
                    new_dic['provider'] = provider
                    self.send_report(str(new_dic))
                    self.mt4_send_signal(new_dic)
                    time.sleep(1)
        print(datetime, datetime.now())

    def MT_connection_check(self):
        try:
            self.zmq._set_response_(_resp={'empty': 0})
            self.zmq._DWX_MTX_GET_ALL_OPEN_TRADES_()
            time.sleep(1)
            mt_response = self.zmq._get_response_()

            if mt_response == {'empty': 0}:
                self.MT_is_connected = False
                self.send_report(mt_response)
                self.zmq._DWX_ZMQ_SHUTDOWN_()
                time.sleep(1)
                self.zmq = Connector()
            if mt_response['_action'] == 'OPEN_TRADES':
                self.MT_is_connected = True
        except:
            traceback.print_exc()
            self.send_report(str(traceback.print_exc()))
            self.MT_is_connected = False

    def Server_connection_check(self):
        try:
            self.response = requests.get(url=self.signal_url, headers=self.headers).json()
            if ('symbol' and 'buy_sell') in self.response[-1]:
                self.server_is_connected = True
            else:
                self.server_is_connected = False
        except Exception as e:
            print(self.response)
            self.send_report(str(self.response)+str(traceback.print_exc()))
            self.server_is_connected = False

    def Loop(self):
        self.MT_connection_check()
        self.Server_connection_check()
        if self.MT_is_connected and not self.server_is_connected:
            top.Label4.configure(background="#519c98")
            top.Label3.configure(background='#cf305d')
            top.Button1.configure(background='#cf305d')
            top.Button1.configure(text='''NOT CONNECTED ''')
        elif not self.MT_is_connected and self.server_is_connected:
            top.Label3.configure(background="#519c98")
            top.Label4.configure(background='#cf305d')
            top.Button1.configure(background='#cf305d')
            top.Button1.configure(text='''NOT CONNECTED ''')
        elif not self.MT_is_connected and not self.server_is_connected:
            top.Label3.configure(background='#cf305d')
            top.Label4.configure(background='#cf305d')
            top.Button1.configure(background='#cf305d')
            top.Button1.configure(text='''NOT CONNECTED ''')
        else:
            top.Label3.configure(background="#519c98")  # server
            top.Label4.configure(background="#519c98")  # MT_4
            if self.status_label_create:
                top.Button1.destroy()
                top.Label_Create()
                self.status_label_create = False
            else:
                top.Button1.configure(background="#519c98")
                top.Button1.configure(text='''CONNECTED ''')
            if len(self.response) != 0:
                self.server_response_read()

    def mt4_send_signal(self, new_dic):
        if new_dic['signal_type'] == 'entry':
            self.mt4_open_trade(new_dic)
        if new_dic['signal_type'] == 'change_part':
            self.mt4_change_trade_close_partially(new_dic)
        if new_dic['signal_type'] == 'change_keep':
            self.mt4_change_trade_keep(new_dic)
        if new_dic['signal_type'] == 'close':
            self.mt4_close_trade(new_dic)
        if new_dic['signal_type'] == 'close_all':
            self.mt4_close_all()

    def mt4_close_trade(self, new_dic):
        self.zmq._set_response_(_resp={'empty': 0})
        self.zmq._DWX_MTX_GET_ALL_OPEN_TRADES_()
        time.sleep(0.5)
        mt_response = self.zmq._get_response_()
        print(mt_response)
        if mt_response['_action'] == 'OPEN_TRADES':
            trades = mt_response['_trades']
            for x, y in trades.items():
                if y['_symbol'] == new_dic['symbol'] and y['_magic'] == 2020:
                    ticket = x
                    self.zmq._DWX_MTX_CLOSE_TRADE_BY_TICKET_(ticket)
                    time.sleep(0.5)
                    mt_response = self.zmq._get_response_()
                    print(mt_response)
                    self.send_report(str(mt_response))

    def mt4_close_all(self):
        self.zmq._DWX_MTX_CLOSE_TRADES_BY_MAGIC_(2020)
        time.sleep(0.5)
        mt_response = self.zmq._get_response_()
        print(mt_response)
        self.send_report(str(mt_response))

    def mt4_change_trade_close_partially(self, new_dic):
        self.zmq._set_response_(_resp={'empty': 0})
        self.zmq._DWX_MTX_GET_ALL_OPEN_TRADES_()
        time.sleep(0.5)
        mt_response = self.zmq._get_response_()
        if mt_response['_action'] == 'OPEN_TRADES':
            trades = mt_response['_trades']
            for x, y in trades.items():
                print(y['_symbol'], new_dic['symbol'], y['_magic'])
                if y['_symbol'] == new_dic['symbol'] and y['_magic'] == 2020:
                    ticket = x
                    print(str(ticket) + 'that is the ticket')
                    self.zmq._DWX_MTX_MODIFY_TRADE_BY_TICKET_(ticket, new_dic['stop'], new_dic['limit'])
                    time.sleep(0.5)
                    mt_response = self.zmq._get_response_()
                    print(mt_response)
                    self.send_report(str(mt_response))
                    if lot_size != 0.01:
                        self.zmq._DWX_MTX_CLOSE_PARTIAL_BY_TICKET_(ticket, round(float(lot_size) / 2, 2))
                        time.sleep(0.5)
                        mt_response = self.zmq._get_response_()
                        print(mt_response)
                        self.send_report(str(mt_response))

    def mt4_change_trade_keep(self, new_dic):
        self.zmq._set_response_(_resp={'empty': 0})
        self.zmq._DWX_MTX_GET_ALL_OPEN_TRADES_()
        time.sleep(0.5)
        mt_response = self.zmq._get_response_()
        print(mt_response)
        if mt_response['_action'] == 'OPEN_TRADES':
            trades = mt_response['_trades']
            for x, y in trades.items():
                if y['_symbol'] == new_dic['symbol'] and y['_magic'] == 2020:
                    ticket = x
                    self.zmq._DWX_MTX_MODIFY_TRADE_BY_TICKET_(ticket, new_dic['stop'], new_dic['limit'])
                    time.sleep(0.5)
                    mt_response = self.zmq._get_response_()
                    print(mt_response)
                    self.send_report(str(mt_response))

    def mt4_open_trade(self, new_dic):
        new_trade = self.zmq._generate_default_order_dict()
        new_trade['_symbol'] = new_dic['symbol']
        if new_dic['buy_sell'] == 'SELL':
            new_trade['_type'] = 1
        new_trade['_SL'] = new_dic['stop']
        new_trade['_TP'] = new_dic['limit']
        new_trade['_lots'] = self.lot_size
        new_trade['_comment'] = new_dic['provider']
        new_trade['_magic'] = 2020
        print(new_trade)
        self.zmq._DWX_MTX_NEW_TRADE_(_order=new_trade)
        time.sleep(0.5)
        mt_response = self.zmq._get_response_()
        print(mt_response)
        self.send_report(str(mt_response))

vp_start_gui()


