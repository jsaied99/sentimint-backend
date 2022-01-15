from api import app
from gevent.pywsgi import WSGIServer


if __name__ == '__main__':
    #path = '/etc/letsencrypt/live/jamalsaied.net'
    path= './'
    http_server = WSGIServer(
                        ('', 8888), app, keyfile=path + 'privkey.pem', certfile=path + 'fullchain.pem')
    http_server.serve_forever()
