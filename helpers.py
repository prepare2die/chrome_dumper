

import sys
import urllib.request
import os
import zipfile

import win32com.client 
import requests


def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))

def get_os_version():
    os_version = OSVERSIONINFOEXW()
    os_version.dwOSVersionInfoSize = sizeof(os_version)
    retcode = windll.Ntdll.RtlGetVersion(byref(os_version))
    if retcode != 0:
        return False
    return '%s.%s' % (str(os_version.dwMajorVersion.real), str(os_version.dwMinorVersion.real))


def checkurl(url):
    try:
        urllib.request.urlopen(url)
        return True
    except Exception as e:
        return False


def check_exists(file):
    if os.path.exists(file):
        return True
    else:
        return False


def lnktrgt(lnk):
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(lnk)
    return(shortcut.Targetpath)