#-*-coding:utf-8-*-

import json
from render import generate_book
from decrypt import decrypt
from send_email import send_file_via_email

with open('data/e2432/data.txt') as fp:
    data = fp.read()

book_title, encrypted_content = data.split(':')[:2]
book_content_data = json.loads(decrypt(encrypted_content))
try:
    book_mobi_path = generate_book('e2432', book_title, book_content_data)
except RuntimeError as e:
    r = e.args[0]
    print r.std_out

send_file_via_email('wonderfuly@kindle.cn', book_mobi_path)
