#-*-coding:utf-8-*-

from flask import Flask, request
from rq import Queue
from redis import Redis
from task import send_book_to_kindle

redis_conn = Redis()
q = Queue(connection=redis_conn, async=True)

app = Flask(__name__)

@app.route('/')
def index():
    return 'index'

@app.route('/send', methods=['POST'])
def send():
    book_id = request.form['book_id']
    book_data = request.form['book_data']
    to_email = request.form['to_email']
    q.enqueue(send_book_to_kindle, book_id, book_data, to_email)
    return 'ok'


if __name__ == '__main__':
    app.run(debug=True)
