from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from email.mime.text import MIMEText
import base64
import os,sys
import pickle
import os.path
import email
import time
from datetime import datetime
import fxcmpy
import pandas as pd
import random
import re
import requests
from random import randrange




pd.set_option('max_columns',None)


def gmail_connect():
    global service

    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token1.pickle3'):
        with open('token1.pickle3', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'C:\\Users\master\desktop\Plan_B\website\\signals_forex.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token1.pickle3', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    return service

def ListMessagesWithLabels(service, user_id, label_ids=[]):


    response = service.users().messages().list(userId=user_id,
                                               labelIds=label_ids).execute()
    messages = []
    if 'messages' in response:
      messages.extend(response['messages'])
    while 'nextPageToken' in response:
      page_token = response['nextPageToken']
      response = service.users().messages().list(userId=user_id,
                                                 labelIds=label_ids,
                                                 pageToken=page_token).execute()
      messages.extend(response['messages'])
    return messages




def GetMimeMessage(service, user_id, msg_id):

    message = service.users().messages().get(userId=user_id, id=msg_id,
                                             format='raw').execute()

    #print('Message snippet: %s' % message['snippet'])

    msg_str = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))

    mime_msg = email.message_from_bytes(msg_str)

    return message,mime_msg

def connect():
    global con
    token = '4fd79c5b1b0886b4ffab4044a9f3200039df8684'  # real
    con = fxcmpy.fxcmpy(access_token=token, log_level="error",server='real')
    print(con.get_accounts())
    print('OK')
    return con


def compose_data_dic(symbol,data,timestamp):
    data_dic = {}
    if symbol == 'AUD/JPN':
        symbol = 'AUD/JPY'
    if symbol == 'USD/JPY' or symbol == 'GBP/JPY'  or symbol == 'EUR/JPY' or symbol == 'CHF/JPY':
        data_dic['stop_loss'] = float(data[13][:3] + '.' + data[13][3:])
        data_dic['TP1'] = float(data[15][:3] + '.' + data[15][3:])
        data_dic['TP2'] = float(data[17][:3] + '.' + data[17][3:])
        data_dic['TP3'] = float(data[19][:3] + '.' + data[19][3:])
        data_dic['TP4'] = float(data[21][:3] + '.' + data[21][3:])
        data_dic['entry_price'] = float(data[10][:3] + '.' + data[10][3:])

    elif symbol == 'CAD/JPY' or symbol == 'AUD/JPY' or symbol == 'NZD/JPY':
        data_dic['stop_loss'] = float(data[13][:2] + '.' + data[13][2:])
        data_dic['TP1'] = float(data[15][:2] + '.' + data[15][2:])
        data_dic['TP2'] = float(data[17][:2] + '.' + data[17][2:])
        data_dic['TP3'] = float(data[19][:2] + '.' + data[19][2:])
        data_dic['TP4'] = float(data[21][:2] + '.' + data[21][2:])
        data_dic['entry_price'] = float(data[10][:2] + '.' + data[10][2:])

    elif symbol == 'USD/CHF' or symbol == 'AUD/USD' or symbol == 'EUR/GBP' or symbol == 'NZD/USD' or symbol == 'AUD/CAD':
        data_dic['stop_loss'] = float('0.' + data[13])
        data_dic['TP1'] = float('0.' + data[15])
        data_dic['TP2'] = float('0.' + data[17])
        data_dic['TP3'] = float('0.' + data[19])
        data_dic['TP4'] = float('0.' + data[21])
        data_dic['entry_price'] = float('0.' + data[10])

    elif symbol == 'GBP/USD' or symbol == 'EUR/USD' or symbol == 'EUR/CHF' or symbol == 'GBP/CHF' or symbol == 'EUR/CAD' or\
            symbol == 'USD/CAD' or symbol == 'EUR/AUD':
        data_dic['stop_loss'] = float('1.' + data[13][1::])
        data_dic['TP1'] = float('1.' + data[15][1::])
        data_dic['TP2'] = float('1.' + data[17][1::])
        data_dic['TP3'] = float('1.' + data[19][1::])
        data_dic['TP4'] = float('1.' + data[21][1::])
        data_dic['entry_price'] = float('1.' + data[10][1::])

    else:
        data_dic['stop_loss'] = 0
        data_dic['TP1'] = 0
        data_dic['TP2'] = 0
        data_dic['TP3'] = 0
        data_dic['TP4'] = 0
        data_dic['entry_price'] = 0

    data_dic['time'] = timestamp
    data_dic['symbol'] = symbol
    data_dic['buy_sell'] = data[6]

    print(data_dic)

    return data_dic



def pickle_create():
    dataframe = pd.DataFrame(columns=['time', 'symbol','buy_sell','entry_price', 'stop_loss', 'TP1', 'TP2', 'TP3','TP4', 'tradeID'])
    dataframe.to_pickle('email_signals.pkl')
    data = pd.read_pickle('email_signals.pkl')
    print(data)

def pickle_append(data_dic):
    data = pd.read_pickle('email_signals.pkl')
    dataNEW = pd.DataFrame([data_dic], columns=['time', 'symbol','buy_sell','entry_price', 'stop_loss', 'TP1', 'TP2', 'TP3','TP4','tradeID'])
    data = data.append(dataNEW)
    data.reset_index(drop=True,inplace=True)

    data.to_pickle('email_signals.pkl')
    print(data.tail(10))

def pickle_load_TP(symbol):
    TP_dic = {}
    data = pd.read_pickle('email_signals.pkl')
    for x in range(len(data)):
        if data['symbol'][x] == symbol:
            print(data['TP1'][x],data['TP2'][x],data['TP3'][x],data['TP4'][x])
            TP_dic = {
                'time' :data['time'][x],
                'symbol':data['symbol'][x],
                'buy_sell':data['buy_sell'][x],
                'entry_price': data['entry_price'][x],
                'stop_loss': data['stop_loss'][x],
                'TP1': data['TP1'][x],
                'TP2': data['TP2'][x],
                'TP3': data['TP3'][x],
                'TP4': data['TP4'][x],
                'tradeID': data['tradeID'][x]
            }

    return TP_dic

def open_trade(data_dic):
    if data_dic['buy_sell'] == 'BUY':
        isBuy = True
    else:
        isBuy = False

    tradeID = con.open_trade(symbol=data_dic['symbol'], is_buy=isBuy, amount=1,
                   time_in_force='GTC',
                   order_type='AtMarket', is_in_pips=False, limit=data_dic['TP4'],
                   stop=data_dic['stop_loss'])
    return tradeID

def change_trade_TP1(TP_dic):
    con.change_trade_stop_limit(TP_dic['tradeID'], is_in_pips=False,
                                is_stop=False, rate=TP_dic['entry_price'])
    con.close_trade(trade_id=TP_dic['tradeID'], amount=1)

def change_trade_TP2(TP_dic):
    con.change_trade_stop_limit(TP_dic['tradeID'], is_in_pips=False,
                                is_stop=False, rate=TP_dic['TP1'])
    con.close_trade(trade_id=TP_dic['tradeID'], amount=1)

def change_trade_TP3(TP_dic):
    con.change_trade_stop_limit(TP_dic['tradeID'], is_in_pips=False,
                                is_stop=False, rate=TP_dic['TP2'])
    con.close_trade(trade_id=TP_dic['tradeID'], amount=1)

def close_trade(symbol):
    #con.close_all_for_symbol(symbol)
    data = pd.read_pickle('email_signals.pkl')
    print(data)
    data = data[data.symbol != symbol]
    data.reset_index(drop=True,inplace=True)
    print(data)
    data.to_pickle('email_signals.pkl')



def api_post_entry(data_dic):
    url = 'http://127.0.0.1:8000/api/signals/?format=json'
    token = '73d46c9377145f87364876b276419206b17a2a7d'
    headers = {'Authorization': 'Token '+token}
    # ['time', 'symbol','buy_sell','entry_price', 'stop_loss', 'TP1', 'TP2', 'TP3','TP4', 'tradeID']
    stop_loss_price = data_dic['stop_loss']
    take_profit_price = data_dic['TP4']
    entry_price = data_dic['entry_price']

    if data_dic['buy_sell'] == 'BUY':
        if data_dic['symbol'] == 'USD/JPY' or data_dic['symbol'] == 'GBP/JPY' or data_dic['symbol'] == 'NZD/JPY' or\
                data_dic['symbol'] == 'AUD/JPY' or data_dic['symbol'] == 'EUR/JPY' or data_dic['symbol'] == 'CAD/JPY' or\
                data_dic['symbol'] == 'CHF/JPY':
            take_pips = int((take_profit_price - entry_price) * 1000)
            stop_pips = int((entry_price - stop_loss_price) * 1000)
        else:
            take_pips = int((take_profit_price - entry_price) * 100000)
            stop_pips = int((entry_price - stop_loss_price) * 100000)
    else:
        if data_dic['symbol'] == 'USD/JPY' or data_dic['symbol'] == 'GBP/JPY' or data_dic['symbol'] == 'NZD/JPY' or \
                data_dic['symbol'] == 'AUD/JPY' or data_dic['symbol'] == 'EUR/JPY' or data_dic['symbol'] == 'CAD/JPY' or\
                data_dic['symbol'] == 'CHF/JPY':
            take_pips = int((entry_price - take_profit_price) * 1000)
            stop_pips = int((stop_loss_price - entry_price) * 1000)
        else:
            take_pips = int((entry_price - take_profit_price) * 100000)
            stop_pips = int((stop_loss_price - entry_price) * 100000)

    symbol = data_dic['symbol'].replace('/', '')

    number = randrange(1000000)
    print(number)
    myobj = {'signal_type': 'entry','symbol': symbol, 'buy_sell': data_dic['buy_sell'],
             'take_profit': take_pips, 'stop_loss': stop_pips, 'provider': 1, 'number': number}
    x = requests.post(url,headers=headers, data=myobj)
    print(x.text)

def api_post_close(data_dic):
    url = 'http://127.0.0.1:8000/api/signals/?format=json'
    token = '73d46c9377145f87364876b276419206b17a2a7d'
    headers = {'Authorization': 'Token ' + token}

    number = randrange(1000000)
    print(number)

    symbol = data_dic['symbol'].replace('/', '')

    myobj = {'signal_type': 'close', 'symbol': symbol, 'buy_sell': data_dic['buy_sell'],
             'take_profit': 1000, 'stop_loss': 1000,'provider': 1, 'number': number}
    x = requests.post(url, headers=headers, data=myobj)
    print(x.text)

def api_post_change_part(TP,data_dic):
    url = 'http://127.0.0.1:8000/api/signals/?format=json'
    token = '73d46c9377145f87364876b276419206b17a2a7d'
    headers = {'Authorization': 'Token ' + token}
    number = randrange(1000000)
    print(number)

    if TP == 'TP1':
        stop_loss_price = data_dic['entry_price']
        take_profit_price = data_dic['TP4']
        entry_price = data_dic['entry_price']
    elif TP == 'TP2':
        stop_loss_price = data_dic['entry_price']
        entry_price = data_dic['TP1']
        take_profit_price = data_dic['TP4']
    else:
        stop_loss_price = data_dic['entry_price']
        take_profit_price = data_dic['TP4']
        entry_price = data_dic['TP2']

    if data_dic['buy_sell'] == 'BUY':
        if data_dic['symbol'] == 'USD/JPY' or data_dic['symbol'] == 'GBP/JPY' or data_dic['symbol'] == 'NZD/JPY' or \
                data_dic['symbol'] == 'AUD/JPY' or data_dic['symbol'] == 'EUR/JPY' or data_dic['symbol'] == 'CAD/JPY':
            take_pips = int((take_profit_price - data_dic['entry_price']) * 1000)
            stop_pips = -(int((entry_price - stop_loss_price) * 1000))
        else:
            take_pips = int((take_profit_price - data_dic['TP4']) * 100000)
            stop_pips = -(int((entry_price - stop_loss_price) * 100000))
    else:
        if data_dic['symbol'] == 'USD/JPY' or data_dic['symbol'] == 'GBP/JPY' or data_dic['symbol'] == 'NZD/JPY' or \
                data_dic['symbol'] == 'AUD/JPY' or data_dic['symbol'] == 'EUR/JPY' or data_dic['symbol'] == 'CAD/JPY':
            take_pips = int((stop_loss_price - data_dic['entry_price']) * 1000)
            stop_pips = -(int((stop_loss_price - entry_price) * 1000))
        else:
            take_pips = int((stop_loss_price - data_dic['TP4']) * 100000)
            stop_pips = -(int((stop_loss_price - entry_price) * 100000))

    symbol = data_dic['symbol'].replace('/', '')

    number = randrange(1000000)
    print(number)
    myobj = {'signal_type': 'change_part', 'symbol': symbol, 'buy_sell': data_dic['buy_sell'],
             'take_profit': take_pips, 'stop_loss': stop_pips, 'provider': 1, 'number': number}
    x = requests.post(url, headers=headers, data=myobj)
    print(x.text)

def api_post_change_(TP,data_dic):
    url = 'http://127.0.0.1:8000/api/signals/?format=json'
    token = '73d46c9377145f87364876b276419206b17a2a7d'
    headers = {'Authorization': 'Token ' + token}
    number = randrange(1000000)
    print(number)

    if TP == 'TP1':
        stop_loss_price = data_dic['entry_price']
        take_profit_price = data_dic['TP4']
        entry_price = data_dic['TP1']
    elif TP == 'TP2':
        stop_loss_price = data_dic['TP1']
        entry_price = data_dic['TP2']
        take_profit_price = data_dic['TP4']
    else:
        stop_loss_price = data_dic['TP2']
        take_profit_price = data_dic['TP4']
        entry_price = data_dic['TP3']



    if data_dic['buy_sell'] == 'BUY':
        if data_dic['symbol'] == 'USD/JPY' or data_dic['symbol'] == 'GBP/JPY' or data_dic['symbol'] == 'NZD/JPY' or\
                data_dic['symbol'] == 'AUD/JPY' or data_dic['symbol'] == 'EUR/JPY' or data_dic['symbol'] == 'CAD/JPY':
            take_pips = int((take_profit_price - entry_price) * 1000)
            stop_pips = int((entry_price - stop_loss_price) * 1000)
        else:
            take_pips = int((take_profit_price - entry_price) * 100000)
            stop_pips = int((entry_price - stop_loss_price) * 100000)
    else:
        if data_dic['symbol'] == 'USD/JPY' or data_dic['symbol'] == 'GBP/JPY' or data_dic['symbol'] == 'NZD/JPY' or \
                data_dic['symbol'] == 'AUD/JPY' or data_dic['symbol'] == 'EUR/JPY' or data_dic['symbol'] == 'CAD/JPY':
            take_pips = int((entry_price - take_profit_price) * 1000)
            stop_pips = int((stop_loss_price - entry_price) * 1000)
        else:
            take_pips = int((entry_price - take_profit_price) * 100000)
            stop_pips = int((stop_loss_price - entry_price) * 100000)

    symbol = data_dic['symbol'].replace('/', '')

    number = randrange(1000000)
    print(number)
    myobj = {'signal_type': 'change_part','symbol': symbol, 'buy_sell': data_dic['buy_sell'],
             'take_profit': take_pips, 'stop_loss': stop_pips,'provider': 1, 'number': number}
    x = requests.post(url,headers=headers, data=myobj)
    print(x.text)



def api_post_change_keep(TP,data_dic):
    url = 'http://127.0.0.1:8000/api/signals/?format=json'
    token = '73d46c9377145f87364876b276419206b17a2a7d'
    headers = {'Authorization': 'Token ' + token}
    number = randrange(1000000)
    print(number)

    if TP == 'TP1':
        stop_loss_price = data_dic['entry_price']
        take_profit_price = data_dic['TP4']
        entry_price = data_dic['TP1']
    elif TP == 'TP2':
        stop_loss_price = data_dic['TP1']
        take_profit_price = data_dic['TP4']
        entry_price = data_dic['TP2']
    else:
        stop_loss_price = data_dic['TP2']
        take_profit_price = data_dic['TP4']
        entry_price = data_dic['TP3']

    if data_dic['buy_sell'] == 'BUY':
        if data_dic['symbol'] == 'USD/JPY' or data_dic['symbol'] == 'GBP/JPY' or data_dic['symbol'] == 'NZD/JPY' or \
                data_dic['symbol'] == 'AUD/JPY' or data_dic['symbol'] == 'EUR/JPY' or data_dic['symbol'] == 'CAD/JPY':
            take_pips = int((take_profit_price - entry_price) * 1000)
            stop_pips = int((entry_price - stop_loss_price) * 1000)
        else:
            take_pips = int((take_profit_price - entry_price) * 100000)
            stop_pips = int((entry_price - stop_loss_price) * 100000)
    else:
        if data_dic['symbol'] == 'USD/JPY' or data_dic['symbol'] == 'GBP/JPY' or data_dic['symbol'] == 'NZD/JPY' or \
                data_dic['symbol'] == 'AUD/JPY' or data_dic['symbol'] == 'EUR/JPY' or data_dic['symbol'] == 'CAD/JPY':
            take_pips = int((entry_price - take_profit_price) * 1000)
            stop_pips = int((stop_loss_price - entry_price) * 1000)
        else:
            take_pips = int((entry_price - take_profit_price) * 100000)
            stop_pips = int((stop_loss_price - entry_price) * 100000)

    symbol = data_dic['symbol'].replace('/', '')

    number = randrange(1000000)
    print(number)
    myobj = {'signal_type': 'change_keep', 'symbol': symbol, 'buy_sell': data_dic['buy_sell'],
             'take_profit': take_pips, 'stop_loss': stop_pips,'provider': 1, 'number': number}
    x = requests.post(url, headers=headers, data=myobj)
    print(x.text)

def TP1_action(subject_data,data):
    if data[3] == 'partially':
        symbol = subject_data[0]
        TP_dic = pickle_load_TP(symbol)
        print(len(TP_dic))
        if len(TP_dic) == 10:
            # change_trade_TP1(TP_dic)
            api_post_change_part('TP1', TP_dic)
        print('TP1    REACHED CLOSING PARTIALLY!!!!!')

    if data[2] == 'move':
        symbol = subject_data[0]
        TP_dic = pickle_load_TP(symbol)
        if len(TP_dic) == 10:
            api_post_change_keep('TP1', TP_dic)
        print('TP1    REACHED KEEP POSITION!!!!!')

    if len(re.findall('close', data[2], re.IGNORECASE)) != 0 and data[3] != 'partially':
        symbol = subject_data[0]
        TP_dic = pickle_load_TP(symbol)
        print(TP_dic)
        if len(TP_dic) == 10:
            api_post_close(TP_dic)
            close_trade(symbol)
        print('TP1       POSITION CLOSED')

def TP2_action(subject_data,data):
    if data[3] == 'partially':
        symbol = subject_data[0]
        TP_dic = pickle_load_TP(symbol)
        if len(TP_dic) == 10:
            api_post_change_part('TP2', TP_dic)
        print('TP2    REACHED CLOSING PARTIALLY!!!!!')

    if data[2] == 'move':
        symbol = subject_data[0]
        TP_dic = pickle_load_TP(symbol)
        if len(TP_dic) == 10:
            api_post_change_keep('TP2', TP_dic)
        print('TP2    REACHED KEEP POSITION!!!!!')

    if len(re.findall('close', data[2], re.IGNORECASE)) != 0 and data[3] != 'partially':
        symbol = subject_data[0]
        TP_dic = pickle_load_TP(symbol)
        if len(TP_dic) == 10:
            api_post_close(TP_dic)
            close_trade(symbol)
        print('TP2   POSITION CLOSED')

def TP3_action(subject_data,data):
    if data[3] == 'partially':
        symbol = subject_data[0]
        TP_dic = pickle_load_TP(symbol)
        if len(TP_dic) == 10:
            api_post_change_part('TP3', TP_dic)
        print('TP3    REACHED CLOSING PARTIALLY!!!!!')

    if data[2] == 'move':
        symbol = subject_data[0]
        TP_dic = pickle_load_TP(symbol)
        if len(TP_dic) == 10:
            api_post_change_keep('TP3', TP_dic)
        print('TP3    REACHED KEEP POSITION!!!!!')

    if len(re.findall('close', data[2], re.IGNORECASE)) != 0 and data[3] != 'partially':
        symbol = subject_data[0]
        TP_dic = pickle_load_TP(symbol)
        if len(TP_dic) == 10:
            api_post_close(TP_dic)
            close_trade(symbol)
        print('TP3   POSITION CLOSED')


def main_loop():
    service = gmail_connect()

    initial_message_list = ListMessagesWithLabels(service,'me',label_ids=['INBOX'])
    print(len(initial_message_list))

    while True:
        current_message_list = ListMessagesWithLabels(service,'me',label_ids=['INBOX'])
        #print(len(current_message_list), len(initial_message_list))

        if len(current_message_list) > len(initial_message_list):
            number_new_messages = len(current_message_list) - len(initial_message_list)

            for x in range(number_new_messages):
                print(x)

                message_id = current_message_list[x]['id']

                raw_message,msg_str = GetMimeMessage(service,'me',message_id)
                timestamp = int(raw_message['internalDate'][:10])
                dt_object = datetime.fromtimestamp(timestamp)
                print(dt_object)

                msg_subject = msg_str['Subject']
                subject_data = msg_subject.split(' ')
                print(msg_subject)
                print(subject_data)

                data = raw_message['snippet'].split(' ')
                print(data)
                print(len(data))
                if len(data) >= 24:
                    print(data[23])
                    if data[0] == 'Asset:' and subject_data[1] == 'Updated' and data[23] == 'Active':
                        symbol = subject_data[0]
                        data_dic = compose_data_dic(symbol,data,dt_object)
                        tradeID = random.randint(0,10000)############################
                        data_dic['tradeID'] = tradeID
                        pickle_append(data_dic)
                        api_post_entry(data_dic)
                        print('----------------------------------------------------------')


                    if len(re.findall('tp1',data[0],re.IGNORECASE)) != 0:
                        TP1_action(subject_data,data)
                        print('----------------------------------------------------------')


                    if len(re.findall('tp2',data[0],re.IGNORECASE)) != 0:
                        TP2_action(subject_data,data)
                        print('----------------------------------------------------------')


                    if len(re.findall('tp3',data[0],re.IGNORECASE)) != 0:
                        TP3_action(subject_data,data)
                        print('----------------------------------------------------------')


                    if len(re.findall('close',data[0],re.IGNORECASE)) != 0 and len(re.findall('manua',data[1],re.IGNORECASE)) != 0:
                        symbol = subject_data[0]
                        TP_dic = pickle_load_TP(symbol)
                        if len(TP_dic) == 10:
                            api_post_close(TP_dic)
                            close_trade(symbol)
                        print('CLOSED MANUALLY')
                        print('----------------------------------------------------------')

                    if len(re.findall('stop',data[23],re.IGNORECASE)) != 0 and len(re.findall('los',data[1],re.IGNORECASE)) != 0:
                        symbol = subject_data[0]
                        TP_dic = pickle_load_TP(symbol)
                        if len(TP_dic) == 10:
                            close_trade(symbol)
                        print('STOP  LOSS')
                        print('----------------------------------------------------------')
                    time.sleep(3)
            initial_message_list = current_message_list
        time.sleep(10)
        if len(initial_message_list) > len(current_message_list):
            initial_message_list = current_message_list
        if datetime.now().second == 0 and datetime.now().minute % 5 == 0:
            print(len(initial_message_list),len(current_message_list),datetime.now().time())
            print('-----------------')


def backtest():
    #pickle_create()
    service = gmail_connect()

    message_list = ListMessagesWithLabels(service,'me',label_ids=['INBOX'])
    print(len(message_list))


    for x in range(290,250,-1):
        print(x)
        message_id = message_list[x]['id']
        raw_message,msg_str = GetMimeMessage(service,'me',message_id)
        timestamp = int(raw_message['internalDate'][:10])
        dt_object = datetime.fromtimestamp(timestamp)
        print(dt_object)
        msg_subject = msg_str['Subject']
        subject_data = msg_subject.split(' ')
        print(msg_subject)
        print(subject_data)
        data = raw_message['snippet'].split(' ')
        print(data)
        print(len(data))
        if len(data) >= 24:
            print(data[23])
            if data[0] == 'Asset:' and subject_data[1] == 'Updated' and data[23] == 'Active':
                symbol = subject_data[0]
                data_dic = compose_data_dic(symbol,data,dt_object)
                tradeID = random.randint(0,10000)############################
                data_dic['tradeID'] = tradeID
                pickle_append(data_dic)
                api_post_entry(data_dic)

            if len(re.findall('tp1',data[0],re.IGNORECASE)) != 0:
                TP1_action(subject_data,data)
            if len(re.findall('tp2',data[0],re.IGNORECASE)) != 0:
                TP2_action(subject_data,data)
            if len(re.findall('tp3',data[0],re.IGNORECASE)) != 0:
                TP3_action(subject_data,data)

            if len(re.findall('close',data[0],re.IGNORECASE)) != 0 and len(re.findall('manua',data[1],re.IGNORECASE)) != 0:
                symbol = subject_data[0]
                TP_dic = pickle_load_TP(symbol)
                if len(TP_dic) == 10:
                    api_post_close(TP_dic)
                    close_trade(symbol)
                print('CLOSED MANUALLY')

            if len(re.findall('stop',data[23],re.IGNORECASE)) != 0 and len(re.findall('los',data[1],re.IGNORECASE)) != 0:
                symbol = subject_data[0]
                TP_dic = pickle_load_TP(symbol)
                if len(TP_dic) == 10:
                    close_trade(symbol)
                    api_post_close(TP_dic)
                print('STOP  LOSS')
        time.sleep(5)
        print('-----------------------------------------------------------------------------------------------')


while True:
    try:
        main_loop()
    except Exception as e:
        print(e)
        time.sleep(240)


