#-*-coding:utf-8-*-

import json
import logging
from render import generate_book
from decrypt import decrypt
from send_email import send_file_via_email

logging.basicConfig(filename='log/app.log', level=logging.DEBUG,
    format='%(asctime)-15s %(name)s.py <%(funcName)s> %(message)s')


def send_book_to_kindle(book_id, to_email):
    with open('data/%s/data.txt' % book_id) as fp:
        data = fp.read()

    book_title, encrypted_content = data.split(':')[:2]
    book_content_data = json.loads(decrypt(encrypted_content))
    try:
        book_mobi_path = generate_book(book_id, book_title, book_content_data)
    except RuntimeError as e:
        book_mobi_path = None

    send_file_via_email(to_email, book_mobi_path)


if __name__ == '__main__':
    send_book_to_kindle('e2432', 'wonderfuly@kindle.cn')
