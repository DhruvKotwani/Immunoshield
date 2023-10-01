import subprocess
import os
import time
import psutil
import sys
import threading
import traceback
import tornado.web
import json
import logging
from tornado import gen

# START_TIME = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(psutil.Process.(os.getpid()).create_time()))

class BaseHandler(tornado.web.RequestHandler):
    @staticmethod
    def get_value_with_default(o, key, default=None):
        return o[key] if key in o else default

class StreamHandler(BaseHandler):

    @gen.coroutine
    def get(self, name=None):
        """
        ---
        tags :
        - Immunoshield
        summary: say hello!
        description: server welcome page
        produces:
        - application/json
        responses:
            200:
                description: welcome message
                schema:
                    type: string
        :param name:
        :return:
        """

        logging.info("Start get request...")
        self.write({"message": "Welcome to our page"})

    @gen.coroutine
    def put(self, name):
        logging.info("Start put request...")
        data = json.load(self.request.body)


class DebugHandler(BaseHandler):
    def _thread_dump(self):
        code = []
        threads = [(thread.name, thread.is_alive()) for thread in threading.enumerate()]
        for threadID, stack in sys._current_frames().items():
            code.append(f"\n# ThreadID : {threadID}")
            for filename, lineno, name, line in traceback.extract_stack(stack):
                code.append(f"File : {filename}, line: {str(lineno)}, in {name}")
                if line:
                    code.append("  %s" % (line.strip()))
        return {"threads": threads, "stacktrace": code}


class StatusHandler(BaseHandler):

    @gen.coroutine
    def get(self):
        self.write({
            "status": "Running",
            "image_tag": "Local",
            "sever_name": "IMMUNOSHIELD",
            "server_port": 4050,
            "start_time": None
        })
