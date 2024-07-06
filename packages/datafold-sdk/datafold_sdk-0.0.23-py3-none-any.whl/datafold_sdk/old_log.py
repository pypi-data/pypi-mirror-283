 # ...

# import time

# # Usage
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger()
# logger.addHandler(SDKLogHandler())
# logger.info('sfsihfiwifw')
# time.sleep(5)
# logger.info('sfssfsfw')
# logger.info('sfssfsfw')
# time.sleep(5)
# logger.info('sfssfsfw')
# logger.info('sfsihfiwifw')
# logger.info('sfssfsfw')

# import logging
# import threading
# import time
# from queue import Queue
# import queue
# import os
# import signal
# import socket
# import atexit
# class SDKLogHandler(logging.Handler):
#     log_queue = queue.Queue()
#     thread_created = False
#     shutdown_requested = False
#     shutdown_signal = threading.Event()

#     def __init__(self):
#         super().__init__()
#         if not SDKLogHandler.thread_created:
#             self.worker_thread = threading.Thread(target=self.send_logs)
#             self.worker_thread.daemon = True  # Daemon thread
#             self.worker_thread.start()
#             SDKLogHandler.thread_created = True

#             # Register signal handler for SIGINT (Ctrl+C)
#             signal.signal(signal.SIGINT, self.handle_shutdown_signal)
#             atexit.register(self.handle_normal_exit)

#     def emit(self, record):
#         message = self.format(record)
#         hostname = socket.gethostname()
#         filename = record.filename
#         line_no = record.lineno
#         level_no = record.levelno
#         level_name = record.levelname
#         func_name = record.funcName
#         created = record.created

#         log_data = {
#             'hostname': hostname,
#             'message': message,
#             'service': 'datafold-sdk',
#             'created': created,
#             'line_no': line_no,
#             'level_no': level_no,
#             'level_name': level_name,
#             'func_name': func_name,
#             'filename': filename
#         }

#         self.log_queue.put(log_data)

#     @classmethod
#     def send_logs(cls):
#         # print('outside')
#         while not cls.shutdown_signal.is_set():
#             # print('iterate')
#             batch = []
#             try:
#                 while True:
#                     log_message = cls.log_queue.get(timeout=2)
#                     batch.append(log_message)
#             except queue.Empty:
#                 if batch:
#                     cls.process_batch(batch)
#                 batch.clear()

#         # print('before inside second')
#         # Process remaining logs before exiting
#         while True:
#             # print('inside second')
#             try:
#                 log_message = cls.log_queue.get(timeout=1)
#                 batch.append(log_message)
#             except queue.Empty:
#                 break

#         if batch:
#             cls.process_batch(batch)
#             batch.clear()

#     @classmethod
#     def process_batch(cls, batch):
#         # Placeholder for batch processing logic
#         print(f"Processing batch of {len(batch)} log messages")
#         for log_message in batch:
#             print(log_message)  # Replace with actual processing logic

#     def handle_normal_exit(self):
#         # print('NORMAL EXIT REACHED')
#         self.shutdown_signal.set()
#         self.worker_thread.join()

#         # Process any remaining logs after thread shutdown
#         batch = []
#         while True:
#             try:
#                 log_message = self.log_queue.get(timeout=1)
#                 batch.append(log_message)
#             except queue.Empty:
#                 break

#         if batch:
#             self.process_batch(batch)
#             batch.clear()

#     def handle_shutdown_signal(self, signum, frame):
#         self.shutdown_requested = True
#         print("Shutdown signal received. Waiting for logs to be processed...")
#         self.shutdown_signal.set()

#         # Block until all logs are processed
#         self.worker_thread.join()

#         # Process any remaining logs after thread shutdown
#         batch = []
#         while True:
#             try:
#                 log_message = self.log_queue.get(timeout=0)
#                 batch.append(log_message)
#             except queue.Empty:
#                 break

#         if batch:
#             self.process_batch(batch)
#             batch.clear()

# logging.basicConfig(level=logging.INFO)

# logger = logging.getLogger()
# logger.addHandler(SDKLogHandler())
# logger.info('sfsihfiwifw')
# logger.info('sfssfsfw')
# time.sleep(10)
# print('his')
# logger.info('sfssfsfw')

# # time.sleep(3)


import logging
import threading
import time
from queue import Queue
import queue
import os
import signal
import socket
# class BatchLogHandler(logging.Handler):
#     def __init__(self):
#         super().__init__()
#         self.queue = Queue()
#         self.thread = threading.Thread(target=self._process_queue)
#         self.thread.daemon = True  # exit with the main thread
#         self.thread.start()

#     def _process_queue(self):
#         print('process queue')
#         while True:
#             try:
#                 records = []
#                 for _ in range(100):  # batch size
#                     print('inside for ')
#                     records.append(self.queue.get(timeout=1))
#                 self._print_records(records)
#             except queue.Empty:
#                 if not self.queue.empty():
#                     records = [self.queue.get() for _ in range(self.queue.qsize())]
#                     self._print_records(records)
#                 time.sleep(1)  # check again in 1 second

#     def _print_records(self, records):
#         print('inside print records')
#         for record in records:
#             print(self.format(record))

#     def emit(self, record):
#         self.queue.put(record)

#     def close(self):
#         self.thread.join()  # wait for the thread to finish
#         super().close()

# # Usage
# logger = logging.getLogger()
# logger.setLevel(logging.INFO)
# handler = BatchLogHandler()
# logger.addHandler(handler)

# # Log some messages
# logger.debug('This is a debug message')
# logger.info('This is an info message')
# logger.warning('This is a warning message')
# logger.error('This is an error message')

# # Wait for 5 seconds to see the batched logs
# time.sleep(5)

# import logging
# import socket
# import threading
# import queue
# import signal
# import time

# dataDogEndpoint = 'https://http-intake.logs.datadoghq.com/api/v2/logs'

class SDKLogHandler(logging.Handler):
    log_queue = queue.Queue()
    thread_created = False
    shutdown_requested = False
    shutdown_signal = threading.Event()

    def __init__(self):
        super().__init__()
        if not SDKLogHandler.thread_created:
            self.worker_thread = threading.Thread(target=self.send_logs)
            self.worker_thread.daemon = False  # Daemon thread
            self.worker_thread.start()
            SDKLogHandler.thread_created = True

            # Register signal handler for SIGINT (Ctrl+C)
            signal.signal(signal.SIGINT, self.handle_shutdown_signal)

    def emit(self, record):
        message = self.format(record)
        hostname = socket.gethostname()
        filename = record.filename
        line_no = record.lineno
        level_no = record.levelno
        level_name = record.levelname
        func_name = record.funcName
        created = record.created

        log_data = {
            'hostname': hostname,
            'message': message,
            'service': 'datafold-sdk',
            'created': created,
            'line_no': line_no,
            'level_no': level_no,
            'level_name': level_name,
            'func_name': func_name,
            'filename': filename
        }

        self.log_queue.put(log_data)

    @classmethod
    def send_logs(cls):
        while not cls.shutdown_signal.is_set():
            batch = []
            try:
                while True:
                    log_message = cls.log_queue.get(timeout=1)
                    batch.append(log_message)
            except queue.Empty:
                if batch:
                    cls.process_batch(batch)
                batch.clear()

        # Process remaining logs before exiting
        while True:
            try:
                log_message = cls.log_queue.get(timeout=1)
                batch.append(log_message)
            except queue.Empty:
                break

        if batch:
            cls.process_batch(batch)
            batch.clear()

    @classmethod
    def process_batch(cls, batch):
        # Placeholder for batch processing logic
        print(f"Processing batch of {len(batch)} log messages")
        for log_message in batch:
            print(log_message)  # Replace with actual processing logic

    def handle_shutdown_signal(self, signum, frame):
        self.shutdown_requested = True
        print("Shutdown signal received. Waiting for logs to be processed...")
        self.shutdown_signal.set()

        # Block until all logs are processed
        self.worker_thread.join()

        # Process any remaining logs after thread shutdown
        batch = []
        while True:
            try:
                log_message = self.log_queue.get(timeout=1)
                batch.append(log_message)
            except queue.Empty:
                break

        if batch:
            self.process_batch(batch)
            batch.clear()

#     def __enter__(self):
#         return self

#     def __exit__(self, exc_type, exc_val, exc_tb):
#         self.shutdown_requested = True
#         print("Exiting context manager. Waiting for logs to be processed...")
#         self.shutdown_signal.set()

#         # Block until all logs are processed
#         self.worker_thread.join()

#         # Process any remaining logs after thread shutdown
#         # batch = []
#         while True:
#             try:
#                 log_message = self.log_queue.get(timeout=1)
#                 batch.append(log_message)
#             except queue.Empty:
#                 break

#         if self.batch:
#             self.process_batch(self.batch)
#             self.batch.clear()

# # Example usage
# if __name__ == '__main__':
#     logging.basicConfig(level=logging.DEBUG)
#     logger = logging.getLogger(__name__)

#     with SDKLogHandler() as handler:
#         try:
#             for i in range(10):
#                 logger.debug(f"Logging message {i}")
#                 time.sleep(1)
#         except KeyboardInterrupt:
#             print("KeyboardInterrupt: Exiting program...")

#     print("Main program finished")


# # import logging
# import socket
# import threading
# import queue
# import requests
# import time
# import signal

# dataDogEndpoint = 'https://http-intake.logs.datadoghq.com/api/v2/logs'

# class SDKLogHandler(logging.Handler):
#     log_queue = queue.Queue()
#     thread_created = False
#     shutdown_requested = False
#     shutdown_signal = threading.Event()

#     def __init__(self):
#         super().__init__()
#         if not SDKLogHandler.thread_created:
#             self.worker_thread = threading.Thread(target=self.send_logs)
#             self.worker_thread.daemon = False
#             self.worker_thread.start()
#             SDKLogHandler.thread_created = True

#             # Register signal handler for SIGINT (Ctrl+C)
#             signal.signal(signal.SIGINT, self.handle_shutdown_signal)

#     def emit(self, record):
#         message = self.format(record)
#         hostname = socket.gethostname()
#         filename = record.filename
#         line_no = record.lineno
#         level_no = record.levelno
#         level_name = record.levelname
#         func_name = record.funcName
#         created = record.created

#         log_data = {
#             'hostname': hostname,
#             'message': message,
#             'service': 'datafold-sdk',
#             'created': created,
#             'line_no': line_no,
#             'level_no': level_no,
#             'level_name': level_name,
#             'func_name': func_name,
#             'filename': filename
#         }

#         self.log_queue.put(log_data)

#     @classmethod
#     def send_logs(cls):
#         while not cls.shutdown_signal.is_set():
#             batch = []
#             try:
#                 while True:
#                     log_message = cls.log_queue.get(timeout=5)
#                     batch.append(log_message)
#             except queue.Empty:
#                 if batch:
#                     cls.process_batch(batch)
#                 batch.clear()

#         # Process remaining logs before exiting
#         while True:
#             try:
#                 log_message = cls.log_queue.get(timeout=1)
#                 batch.append(log_message)
#             except queue.Empty:
#                 break

#         if batch:
#             cls.process_batch(batch)
#             batch.clear()

#     @classmethod
#     def process_batch(cls, batch):
#         # Placeholder for batch processing logic
#         print(f"Processing batch of {len(batch)} log messages")
#         for log_message in batch:
#             print(log_message)  # Replace with actual processing logic

#     def handle_shutdown_signal(self, signum, frame):
#         self.shutdown_requested = True
#         print("Shutdown signal received. Waiting for logs to be processed...")
#         self.shutdown_signal.set()
#         self.worker_thread.join()  # Wait for worker thread to complete

#         # Process any remaining logs after thread shutdown
#         batch = []
#         while True:
#             try:
#                 log_message = self.log_queue.get(timeout=1)
#                 batch.append(log_message)
#             except queue.Empty:
#                 break

#         if batch:
#             self.process_batch(batch)
#             batch.clear()

# # Example usage
# if __name__ == '__main__':
#     logging.basicConfig(level=logging.DEBUG)
#     logger = logging.getLogger(__name__)
#     handler = SDKLogHandler()
#     logger.addHandler(handler)

#     try:
#         # Simulate logging messages
#         for i in range(10):
#             logger.debug(f"Logging message {i}")
#             time.sleep(1)
#     except KeyboardInterrupt:
#         print("KeyboardInterrupt: Exiting program...")
#     finally:
#         # Allow the main program to finish without explicit shutdown call
#         pass

#     print("Main program finished")


# import requests
# import socket
# import logging
# import threading
# import queue
# from queue import Queue
# import time
# import signal

# dataDogEndpoint = 'https://http-intake.logs.datadoghq.com/api/v2/logs'

# class SDKLogHandler(logging.Handler):
#     log_queue = Queue() 
#     thread_created = False
#     shutdown_signal = threading.Event()

#     def __init__(self):
#         super().__init__()
#         if not SDKLogHandler.thread_created:
#             print('inside thread created')
#             self.worker_thread = threading.Thread(target=self.send_logs)
#             self.worker_thread.daemon = False
#             self.worker_thread.start()
#             SDKLogHandler.thread_created = True

#     def emit(self, record):
#         message = self.format(record)
#         hostname = socket.gethostname()
#         filename = record.filename
#         line_no = record.lineno
#         level_no = record.levelno
#         level_name = record.levelname
#         func_name = record.funcName
#         created = record.created
#        # print(type(message), type(hostname),type(line_no),type(level_no),type(level_name), type(filename), type(func_name))
#         log_data = {
#             'hostname': hostname,
#             'message': message,
#             'service': 'datafold-sdk',
#             'created': created,
#             'line_no' : line_no,
#             'level_no' : level_no,
#             'level_name' : level_name,
#             'func_name': func_name,
#             'filename': filename
#         }
#        # print(log_data)
#         self.log_queue.put(log_data)

#     @classmethod
#     def send_logs(cls):
#         while not cls.shutdown_signal.is_set():
#             batch = []
#             try:
#                 while True:
#                     log_message = cls.log_queue.get(timeout=5)
#                     batch.append(log_message)
#             except queue.Empty:
#                 if batch:
#                     cls.process_batch(batch)
#                 batch.clear()

#         # Process remaining logs before exiting
#         while True:
#             try:
#                 log_message = cls.log_queue.get(timeout=1)
#                 batch.append(log_message)
#             except queue.Empty:
#                 break

#         if batch:
#             cls.process_batch(batch)
#             batch.clear()
#     @classmethod
#     def process_batch(cls, batch):
#         # Placeholder for batch processing logic
#         print(f"Processing batch of {len(batch)} log messages")
#         for log_message in batch:
#             print(log_message)  # Replace with actual processing logic

#     @classmethod
#     def shutdown(cls):
#         self.shutdown_signal.set()
#         if self.worker_thread:
#             self.worker_thread.join()  # Wait for the thread to exit gracefully
#     @classmethod
#     def __del__(cls):
#         # Ensure all logs are processed before deleting the handler
#         print('deleting')
#         cls.thread_created = False  # Signal send_logs thread to finish
#         cls.worker_thread.join()  # Wait for the thread to complete processing




    # @classmethod
    # def send_logs(cls):
    #     while True:
    #         batch = []
    #         try:
    #             while True:
    #                 log_message = cls.log_queue.get(timeout=3)
    #                 batch.append(log_message)
    #         except queue.Empty:
    #             pass
    #         # f = open("demofile2.txt", "a")
    #         # f.write(f"Now the file has more content! {len(batch)}")
    #         # f.close()

    #         # print('BATCH LENGTH')
    #         if batch:
    #             print(len(batch))
    #             requests.get('https://google.com')
    #             # print('inside batch')
    #             # f = open("demofile2.txt", "a")
    #             # f.write(f"Now the file has more content! {len(batch)}")
    #             # f.close()
    #         #     headers = {
    #         #         'Content-Type': 'application/json',
    #         #         'Authorization': f'Key 001b5afb0639ab44aa3a36b77de2d56f'
    #         #     }
    #         #     response = requests.post(dataDogEndpoint, json=batch, headers=headers)
    #         #     # You may want to handle response here if needed

# def signal_handler(sig, frame):
#     print('Ctrl+C detected. Shutting down gracefully...')
#     SDKLogHandler.shutdown()
#     sys.exit(0)

# # Register signal handler for SIGINT (Ctrl+C)
# signal.signal(signal.SIGINT, signal_handler)


logging.basicConfig(level=logging.INFO)

logger = logging.getLogger()
logger.addHandler(SDKLogHandler())
logger.info('sfsihfiwifw')
logger.info('sfssfsfw')

print('his')

# time.sleep(10)
logger.info('sfssfsfw')

# time.sleep(3)





# import logging
# import asyncio
# import threading
# import queue
# import signal
# import socket
# import atexit
# import sys
# import time

# class SDKLogHandler(logging.Handler):
#     def __init__(self):
#         super().__init__()
#         atexit.register(self.handle_normal_exit)
#         self.log_queue = queue.Queue()
#         self.shutdown_requested = False
#         self.shutdown_signal = threading.Event()
#         self.worker_thread = threading.Thread(target=self.run_async)
#         self.worker_thread.start()

#         # Register signal handler for SIGINT (Ctrl+C)
#         signal.signal(signal.SIGINT, self.handle_shutdown_signal)

#         # Register atexit handler for normal program exit
        

#     def emit(self, record):
#         message = self.format(record)
#         hostname = socket.gethostname()
#         filename = record.filename
#         line_no = record.lineno
#         level_no = record.levelno
#         level_name = record.levelname
#         func_name = record.funcName
#         created = record.created

#         log_data = {
#             'hostname': hostname,
#             'message': message,
#             'service': 'datafold-sdk',
#             'created': created,
#             'line_no': line_no,
#             'level_no': level_no,
#             'level_name': level_name,
#             'func_name': func_name,
#             'filename': filename
#         }

#         self.log_queue.put(log_data)

#     async def send_logs(self):
#         batch = []
#         while not self.shutdown_requested:
#             # print('hi')
#             try:
                
#                 # while True:
#                 log_message = self.log_queue.get(timeout=1)
#                 # print(log_message)
#                 batch.append(log_message)
#                 # continue
#             except queue.Empty:
#                 if batch:
#                     await self.process_batch(batch)
#                     batch.clear()

#         # Process remaining logs before exiting
#         batch = []
#         while True:
#             try:
#                 log_message = self.log_queue.get(timeout=1)
#                 batch.append(log_message)
#             except queue.Empty:
#                 break

#         if batch:
#             await self.process_batch(batch)

#     async def process_batch(self, batch):
#         # Placeholder for batch processing logic (make this asynchronous if actual processing is IO-bound)
#         print(f"Processing batch of {len(batch)} log messages")
#         for log_message in batch:
#             print(log_message)  # Replace with actual processing logic

#     def run_async(self):
#         try:
#             asyncio.run(self.send_logs())
#         except asyncio.CancelledError:
#             pass  # Handle cancellation gracefully if needed

#     def handle_shutdown_signal(self, signum, frame):
#         if not self.shutdown_requested:
#             self.shutdown_requested = True
#             print("Shutdown signal received. Waiting for logs to be processed...")
#             self.shutdown_signal.set()

#             # Exit the program after shutdown
#             self.shutdown_complete()

#     def shutdown_complete(self):
#         print("Shutdown complete.")
#         # Exit the worker thread explicitly if it's still running
#         if self.worker_thread.is_alive():
#             self.worker_thread.join(timeout=2)  # Wait for the worker thread to finish

#         # No need to close asyncio event loop here

#     def handle_normal_exit(self):
#         print('DETECTED NORMAL EXIT')
#         if not self.shutdown_requested:
#             print("Normal program exit detected. Waiting for logs to be processed...")
#             self.shutdown_requested = True
#             self.shutdown_signal.set()

#             # Exit the program after shutdown
#             self.shutdown_complete()


# # Example usage:
# if __name__ == "__main__":
#     logging.basicConfig(level=logging.DEBUG)
#     handler = SDKLogHandler()
#     logger = logging.getLogger(__name__)
#     logger.addHandler(handler)

#     # Example log messages
#     logger.debug("Debug message 1")
#     logger.info("Info message 1")
#     time.sleep(1)
#     logger.warning("Warning message 1")
#     # sys.exit(0)
#     # asyncio.get_event_loop().close()
#     # try:
#     #     # Simulate program running
#     #     while True:
#     #         pass  # Replace with actual program logic
#     # except KeyboardInterrupt:
#     #     print("\nCtrl+C pressed. Exiting program...")
