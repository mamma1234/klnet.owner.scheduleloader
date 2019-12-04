import os, sys
import time

def getSize(filename):
    if os.path.isfile(filename): 
        st = os.stat(filename)
        return st.st_size
    else:
        return -1

def wait_download(file_path):
    current_size = getSize(file_path)
    print("File size", current_size)
    while current_size !=getSize(file_path) or getSize(file_path)==0:
        current_size =getSize(file_path)
        print("current_size:"+str(current_size))
        time.sleep(1)# wait download
    print("Downloaded")