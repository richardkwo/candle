#-*-coding:utf-8-*-

import platform

system = platform.system()

if system == 'Darwin':
    from decrypt_mac import decrypt
elif system == 'Linux':
    from decrypt_linux import decrypt
