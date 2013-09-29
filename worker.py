#-*-coding:utf-8-*-

import os
import json
import logging
from render import generate_book
from decrypt import decrypt
from send_email import send_file_via_email

logging.basicConfig(filename='log/app.log', level=logging.DEBUG,
    format='%(asctime)-15s %(name)s.py <%(funcName)s> %(message)s')

logger = logging.getLogger(__name__)

def parse_book_data(book_data_str):
    tmp = book_data_str.split(':')
    data = dict(zip(['title', 'encrypted_content', 'purchase_time', 
        'is_sample', 'is_gift', 'has_formula', 'has_added', 'price'], tmp))
    for key in ['is_sample', 'is_gift', 'has_formula', 'has_added']:
        data[key] = data[key] == '1'
    return data


def send_book_to_kindle(book_id, book_data_str, to_email):
    need_generate = True
    book_dir = 'data/%s' % book_id
    book_mobi_path = '%s/%s.mobi' % (book_dir, book_id)
    book_data = parse_book_data(book_data_str)

    # 是不是不需要新生成
    if not book_data['is_sample'] and os.path.exists(book_mobi_path):
        with open('%s/data.txt' % book_dir) as fp:
            old_book_data_str = fp.read().decode('utf-8')
        if old_book_data_str == book_data_str:
            need_generate = False

    logger.info('book %s need generate? : %s', book_id, need_generate)

    if need_generate:
        if not os.path.isdir(book_dir):
            os.mkdir(book_dir)
        with open('%s/data.txt' % book_dir, 'w') as fp:
            fp.write(book_data_str.encode('utf-8'))
        book_content_data_str = decrypt(book_data['encrypted_content'])
        book_content_data = json.loads(book_content_data_str)
        logger.info('decrypt successful for %s', book_id)
        book_title = book_data['title']
        try:
            book_mobi_path = generate_book(book_id, book_title, book_content_data)
        except RuntimeError:
            book_mobi_path = None

    if book_mobi_path:
        send_file_via_email(to_email, book_mobi_path)


if __name__ == '__main__':
    with open('data/e2432/data.txt') as fp:
        book_data_str = fp.read()
    send_book_to_kindle('e2432', book_data_str, 'wonderfuly@kindle.cn')
