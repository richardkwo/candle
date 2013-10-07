#-*-coding:utf-8-*-

import sys
import platform

system = platform.system()
is_64 = sys.maxsize > 2**32

if system == 'Darwin':
    from decrypt_mac import decrypt
elif system == 'Linux':
    if is_64:
        from decrypt_linux_64 import decrypt
    else:
        from decrypt_linux_32 import decrypt
