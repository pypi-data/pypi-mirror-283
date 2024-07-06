import queue
import threading
import time
import logging
import concurrent.futures
import socket
import atexit
import os
import requests
from typing import Dict
import pydantic

# from datafold_sdk.cli.context import DATAFOLD_HOST, DATAFOLD_API_KEY, DATAFOLD_APIKEY

DF_HOST = 'https://app.datafold.com'
# DF_API_KEY = os.environ.get(DATAFOLD_API_KEY) or os.environ.get(DATAFOLD_APIKEY)

DF_API_KEY = ';'
# override_host = os.environ.get(DATAFOLD_HOST)
# if override_host:
#     DF_HOST = override_host

SDK_LOGS_ENDPOINT = '{}/api/internal/sdk/log'.format(DF_HOST.rstrip('/'))

class SDKLog(pydantic.BaseModel):
    message: str
    created: float
    line_no: int
    level_no: int
    level_name: str
    func_name: str
    filename: str

class SDKLogHandler(logging.Handler):
    log_queue = queue.Queue()
    thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=1)
    thread_created_lock = threading.Lock()  # Lock to ensure thread creation is synchronized
    thread_created = False

    def __init__(self):
        super().__init__()
        with SDKLogHandler.thread_created_lock:
            if not SDKLogHandler.thread_created:
                print('NEW THREAD CREATED')
                SDKLogHandler.thread_created = True
                self.batch = []
                self.worker_thread = threading.Thread(target=self.send_logs)
                self.worker_thread.daemon = True
                self.worker_thread.start()

                atexit.register(self.handle_normal_exit)

    def emit(self, record) -> None:
        message = self.format(record)
        filename = record.filename
        line_no = record.lineno
        level_no = record.levelno
        level_name = record.levelname
        func_name = record.funcName
        created = record.created

        log_data = SDKLog(message=message,
            created=created,
            line_no=line_no,
            level_no=level_no,
            level_name=level_name,
            func_name=func_name,
            filename=filename
        )

        self.log_queue.put(log_data)

    def send_logs(self) -> None:
        print('send logs')
        while True:
            print('iteration')
            try:
                log_data = self.log_queue.get(timeout=3)
                self.batch.append(log_data.dict())
                print(len(self.batch))
            except queue.Empty:
                if self.batch:
                    self.process_batch()
                    self.batch = []
            except Exception as e:
                pass
    @staticmethod
    def process_logs(batch) -> None:
        print('PROCESS LOGS')
        try:
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Key {DF_API_KEY}'
            }
            log_data = {'hostname': socket.gethostname(), 'service' : 'datafold-sdk', 'logs': batch}
            # print(log_data)
            response = requests.post(SDK_LOGS_ENDPOINT, json=log_data, headers=headers, timeout=5)
            request = response.request
            # batch = []

            # print(f"Request URL: {request.url}")
            # print(f"Request Method: {request.method}")
            # print(f"Request Headers:")
            # for header, value in request.headers.items():
            #     print(f"    {header}: {value}")
            print(f"Request Body:")
            print(request.body.decode('utf-8')) 
        except Exception as e:
            print(str(e))
            pass


    def process_batch(self) -> None:
        print('CALL PROCESS BATCH')
        self.thread_pool.submit(self.process_logs, self.batch)
        # self.batch = []

    def handle_normal_exit(self) -> None:
        leftover = []
        while not self.log_queue.empty():
            log_data = self.log_queue.get(timeout=0.1)
            self.batch.append(log_data.dict())

        if self.batch:
            self.process_logs(self.batch)
        self.thread_pool.shutdown(wait=True)
   
