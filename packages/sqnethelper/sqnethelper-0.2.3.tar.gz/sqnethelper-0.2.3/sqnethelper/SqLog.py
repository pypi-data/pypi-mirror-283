import sys
import datetime
import websockets
import asyncio
import threading
import enum

class LogLevel(enum.IntEnum):
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    CRITICAL = 4

class SqLog:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SqLog, cls).__new__(cls)
            cls._instance.initialize()
        return cls._instance

    def initialize(self):
        self.file = None
        self.websocket = None
        self.output_methods = set()
        self.log_level = LogLevel.INFO  # 默认日志等级为 INFO

    def set_file_output(self, filename):
        self.file = open(filename, 'a', encoding='utf-8')
        self.output_methods.add('file')

    def set_console_output(self):
        self.output_methods.add('console')

    def set_websocket_output(self, host='localhost', port=8765):
        self.websocket_url = f"ws://{host}:{port}"
        self.output_methods.add('websocket')
        threading.Thread(target=self._run_websocket_server, daemon=True).start()

    def set_log_level(self, level):
        if isinstance(level, LogLevel):
            self.log_level = level
        elif isinstance(level, str):
            self.log_level = LogLevel[level.upper()]
        else:
            raise ValueError("Invalid log level")

    def _run_websocket_server(self):
        async def echo(websocket, path):
            self.websocket = websocket
            try:
                await websocket.wait_closed()
            finally:
                self.websocket = None

        asyncio.set_event_loop(asyncio.new_event_loop())
        start_server = websockets.serve(echo, "localhost", 8765)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

    async def _send_websocket(self, message):
        if self.websocket:
            await self.websocket.send(message)

    def _log(self, level, *args, **kwargs):
        if level.value < self.log_level.value:
            return

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"[{timestamp}] [{level.name}] " + " ".join(map(str, args))

        if 'console' in self.output_methods:
            print(message, **kwargs)

        if 'file' in self.output_methods and self.file:
            print(message, file=self.file, flush=True)

        if 'websocket' in self.output_methods:
            asyncio.get_event_loop().run_until_complete(self._send_websocket(message))

    def debug(self, *args, **kwargs):
        self._log(LogLevel.DEBUG, *args, **kwargs)

    def info(self, *args, **kwargs):
        self._log(LogLevel.INFO, *args, **kwargs)

    def warning(self, *args, **kwargs):
        self._log(LogLevel.WARNING, *args, **kwargs)

    def error(self, *args, **kwargs):
        self._log(LogLevel.ERROR, *args, **kwargs)

    def critical(self, *args, **kwargs):
        self._log(LogLevel.CRITICAL, *args, **kwargs)

    def close(self):
        if self.file:
            self.file.close()

SQLOG = SqLog()