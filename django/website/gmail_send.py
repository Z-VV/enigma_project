from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from email.mime.text import MIMEText
import base64
import os
import pickle
import os.path
import email
import time
from django.contrib.auth.models import User



def gmail_connect():
    global service

    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    SCOPES = ['https://www.googleapis.com/auth/gmail.send',
              'https://www.googleapis.com/auth/gmail.compose','https://www.googleapis.com/auth/gmail.readonly']

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle3'):
        with open('token.pickle3', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'C:\\Users\master\desktop\Plan_B\website\\new_cred.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle3', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    return service


def create_message(sender, to, subject, message_text):

  message = MIMEText(message_text)
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}

def send_message(service, message):


  message = (service.users().messages().send(userId='me', body=message).execute())
  print('Message Id: %s' % message['id'])
  print(message)
  return message


def compose_and_send(sender,to,subject,message_text):
    service = gmail_connect()
    message = create_message(sender,to,subject,message_text)
    send_message(service,message)

def gmail_first_message(user_id,trial_token):
    user = User.objects.get(pk=user_id)
    message_string = 'Hello ' + user.first_name +'.\n'+'Welcome to the jungle.\nYour one week trial Token is\ntoken:'+str(trial_token)+\
                     '\nEnjoy!\nThank you.'
    compose_and_send('Enigma-lab',user.email,'Welcome',message_string)


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


def ListMessages(service, user_id, query=''):

    response = service.users().messages().list(userId=user_id,
                                               q=query).execute()
    messages = []
    if 'messages' in response:
      messages.extend(response['messages'])

    while 'nextPageToken' in response:
      page_token = response['nextPageToken']
      response = service.users().messages().list(userId=user_id, q=query,
                                         pageToken=page_token).execute()
      messages.extend(response['messages'])
    return messages



def GetMimeMessage(service, user_id, msg_id):

    message = service.users().messages().get(userId=user_id, id=msg_id,
                                             format='raw').execute()


    print('Message snippet: %s' % message['snippet'])
    print(message['snippet'].split(' '))
    msg_str = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))



    #mime_msg = email.message_from_string(msg_str)

    return msg_str



#service = gmail_connect()
#message_list = ListMessagesWithLabels(service,'me',label_ids=['INBOX'])
##print(message_list)
#message_id = message_list[0]['id']
##print(message_id)
#msg_string = GetMimeMessage(service,'me',message_id)
#
#splited = str(msg_string).split('*Asset:*')
#info = splited[1].split('All Active Forex')[0]
#info = info.replace('\\r\\n','')
#info = info.split('   ')
#print(info)
#print(info[1],info[5],info[7],info[9],info[11],info[13],info[15])
#






