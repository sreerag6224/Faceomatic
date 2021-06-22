from face import app as web
from android import app as andro
from werkzeug.wsgi import DispatcherMiddleware
application = DispatcherMiddleware(web, {
    '/andro': andro
})
