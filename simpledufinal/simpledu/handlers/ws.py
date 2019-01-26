from flask import Blueprint
import redis
import gevent
import json

ws = Blueprint('wd', __name__, url_prefix='/ws')


redis = redis.from_url('redis://127.0.0.1:6379')


class Chatroom(object):
    def __init__(self):
        self.clients = []
        self.pubsub = redis.pubsub()
        self.pubsub.subscribe('chat')

    def register(self, client):
        self.clients.append(client)

    def send(self, client, data):
        try:
            client.send(data.decode('utf-8'))
        except:
            self.clients.remove(client)
    
    def run(self):
        for message in self.pubsub.listen():
            if message['type'] == 'message':
                data = message.get('data')
                for client in self.clients:
                    gevent.spawn(self.send, client, data)

    def start(self):
        gevent.spawn(self.run)

chat = Chatroom()
chat.start()

@ws.route('/send')
def inbox(ws):
    # 使用flask-sockets, ws链接对象会被自动注入到路由处理函数， 该处理函数用来处理前端发过来的消息
    
    while not ws.closed:
        message = ws.receive()
        gevent.sleep(0.1) 
        if message:
            redis.publish('chat', message)

@ws.route('/recv')
def outbox(ws):
    # 该函数用来注册客户端连接， 并在Chatroom中将从其它客户端接收到的消息发送给这些客户端
    chat.register(ws)
    redis.publish('chat', json.dumps(dict(username='New user come in, people count', text=len(chat.clients))))
    while not ws.closed:
        gevent.sleep(0.1) 