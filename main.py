from ast import Div
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
from selenium.common.exceptions import NoSuchElementException
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime 


class Tracker:

    def __init__(self,name) :

        self.name = name 

        options = Options()
        options.binary_location = r'C:\\Program Files\\Mozilla Firefox\\firefox.exe'
        driver = webdriver.Firefox(executable_path="D:\PROJECTS\Tracker\geckodriver.exe", options=options)

        driver.get("https://web.whatsapp.com/")
        driver.maximize_window()
        driver.implicitly_wait(40)
        search_bar = driver.find_element_by_class_name("_13NKt")
    
        self.driver = driver 
        self.search_bar = search_bar

        self.connect_Sheet()
        self.check()

    def connect_Sheet(self):
        scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',
                 "https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

        creds = ServiceAccountCredentials.from_json_keyfile_name("db.json",scope)
        client = gspread.authorize(creds)
        sheet = client.open("Tracker_Whatsapp").sheet1
        self.sheet = sheet 
        return None 

    def load_Browser(self):

        self.search_bar.clear()
        self.search_bar.click()
        self.search_bar.send_keys(self.name)
        self.search_bar.send_keys(u'\ue007')
        return None 

    def update_Online_Time(self,state):
        dt = datetime.datetime.now()
        lis = [dt.strftime( "%d-%m-%Y"), state , dt.strftime("%H - %M - %S")]
        self.sheet.append_row(lis)
        return None 
    

    def check(self):

        self.load_Browser()

        count = 0
        state = 'off' 

        while(True):
            # Count is to refresh the page for every 3 iteration - To Find accurate status 
            count += 1
            try:
                status = self.driver.find_element_by_class_name("zzgSd").text
                if state == 'off' and status == 'online' : 
                    state = 'on'  
                time.sleep(15)

            except NoSuchElementException:
                
                if state == 'hold':
                    state = 'off'
                    self.update_Online_Time("OFF-Line")

            if state == 'on' :
                self.update_Online_Time("ON-Line")
                state = 'hold'

            if count == 3:
                    self.load_Browser()
                    count = 0
           
member = Tracker("") #Phone Number 