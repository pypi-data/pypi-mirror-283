import time
from pathlib import Path

from ajsonrpc.core import JSONRPC20DispatchException

from zhixin.compat import aio_get_running_loop
from zhixin.home.rpc.handlers.base import BaseRPCHandler


class IDERPC(BaseRPCHandler):
    COMMAND_TIMEOUT = 1.5  # in seconds

    def __init__(self):
        self._ide_queue = []
        self._cmd_queue = {}

    async def listen_commands(self):
        f = aio_get_running_loop().create_future()
        self._ide_queue.append(f)
        self._process_commands()
        return await f

    async def send_command(self, command, params=None):
        cmd_id = f"ide-{command}-{time.time()}"
        self._cmd_queue[cmd_id] = {
            "method": command,
            "params": params,
            "time": time.time(),
            "future": aio_get_running_loop().create_future(),
        }
        self._process_commands()
        # in case if IDE agent has not been started
        aio_get_running_loop().call_later(
            self.COMMAND_TIMEOUT + 0.1, self._process_commands
        )
        return await self._cmd_queue[cmd_id]["future"]

    def on_command_result(self, cmd_id, value):
        if cmd_id not in self._cmd_queue:
            return False
        if self._cmd_queue[cmd_id]["method"] == "get_zx_project_dirs":
            value = [str(Path(p).resolve()) for p in value]
        self._cmd_queue[cmd_id]["future"].set_result(value)
        del self._cmd_queue[cmd_id]
        return True

    def _process_commands(self):
        for cmd_id in list(self._cmd_queue):
            cmd_data = self._cmd_queue[cmd_id]
            if cmd_data["future"].done():
                del self._cmd_queue[cmd_id]
                continue

            if (
                not self._ide_queue
                and (time.time() - cmd_data["time"]) > self.COMMAND_TIMEOUT
            ):
                cmd_data["future"].set_exception(
                    JSONRPC20DispatchException(
                        code=4005, message="ZX Home IDE agent is not started"
                    )
                )
                continue

            while self._ide_queue:
                self._ide_queue.pop().set_result(
                    {
                        "id": cmd_id,
                        "method": cmd_data["method"],
                        "params": cmd_data["params"],
                    }
                )
