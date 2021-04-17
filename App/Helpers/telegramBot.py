#import time
#import schedule
import requests
import os

class telegramBot():
    # Here will be the instance stored.
    __instance = None
    
    def __init__(self):
        self.__botToken = str(os.getenv('BOT_TOKEN'))
        self.__botChatID = str(os.getenv('BOT_CHAT_ID'))
        self.__domain = str(os.getenv('BOT_DOMAIN'))
        
        """ Virtually private constructor. """
        if telegramBot.__instance != None:
            pass
        else:
            telegramBot.__instance = self
    
    @staticmethod
    def getInstance():
        """ Static access method. """
        if telegramBot.__instance == None:
            telegramBot()
        return telegramBot.__instance
    
        
    def telegramBotSendText(self, message):
        send_text = self.__domain + self.__botToken + '/sendMessage?chat_id=' + self.__botChatID + '&parse_mode=Markdown&text=' + message
        response = requests.get(send_text)
    
        return response.json()


