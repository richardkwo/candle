#-*-coding:utf-8-*-

import json
from decrypt import decrypt
from render import render_html
from send_email import send_file_via_email

def gen_mobi():
    pass

with open('data/encrypted.txt') as fp:
    encrypted_str = fp.read()
decrypted_str = decrypt(encrypted_str)
data = json.loads(decrypted_str)
html = render_html(data)
print html.encode('utf-8')
