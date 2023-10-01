import logging
import os
import sys
import tornado
from tornado_swagger.setup import setup_swagger

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../")
from Imunoshield.web.request_handlers import DebugHandler
from Imunoshield.utils.utils import setup_logging

SERVER_NAME = "IMMUNOSHIELD"
SERVER_PORT = 4050


def _make_app():
    logging.info("Initiating Making of Application")
    root = os.path.dirname(__file__)
    _routes = [
        tornado.web.url(r"/index/(.*)", tornado.web.StaticFileHandler, {"path": root, "default_filename": "html/index.html"}),
        tornado.web.url(r"/REST/debug", DebugHandler)
    ]

    application = tornado.web.Application(_routes)
    port = SERVER_PORT
    logging.info(f"Listening on {port}")
    application.listen(port)
    logging.info("Application Successfully created")
    return application


def _setup_logging():
    log_path = "./" + SERVER_NAME + ".log"
    setup_logging(filepath=log_path)


if __name__ == "__main__":
    _setup_logging()
    app = _make_app()

    logging.info("Sever preparation finished")
    logging.info(f"Starting {SERVER_NAME} web server")
    tornado.ioloop.IOLoop.current().start()
    logging.info(f"{SERVER_NAME} successfully started on port {SERVER_PORT}")
