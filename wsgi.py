from api import app
from gevent.pywsgi import WSGIServer
import sys 

if __name__ == '__main__':
    running = sys.argv[1] if len(sys.argv) > 1 else 'server'
    print('Running in {} mode'.format(running))
    if running == 'server':
        path = 'auth/'
        port = 5000
    
        http_server = WSGIServer(
                        ('', port), app, keyfile=path + 'privkey.pem', certfile=path + 'fullchain.pem')
        http_server.serve_forever()
    elif running == 'test':
        http_server = WSGIServer(
                        ('', 5000), app, keyfile=None, certfile=None)
        http_server.serve_forever()
        print('Server running on port 5000')
