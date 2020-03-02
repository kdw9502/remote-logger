import asyncio
import tkinter as tk
import tkinter.ttk

import pygubu

from LogListener import LogListener
from UDPBroadCaster import UDPBroadCaster

TARGET_FPS = 60


class RemoteDebuggerApp:
    def __init__(self):
        self.builder = pygubu.Builder()
        self.top_level = None
        self.broad_caster = UDPBroadCaster()
        self.log_listener = LogListener(self.on_log_added)

    async def run(self):
        self._load_from_file()
        self._init_broad_caster()
        self._set_callbacks()

        asyncio.create_task(self.log_listener.listen())

        await self._run_async_mainloop()

    def _load_from_file(self):
        self.builder.add_from_file('pygubu-gui.ui')
        self.top_level = self.builder.get_object('TopLevel')

    def _set_callbacks(self):
        command_dict = {function_name: getattr(self, function_name) for function_name in dir(self)
                        if callable(getattr(self, function_name)) and not function_name.startswith("_")}

        self.builder.connect_callbacks(command_dict)

    def _init_broad_caster(self):
        my_ip = self.broad_caster.get_my_ip()

        var: tkinter.StringVar = self.builder.get_variable('ip_label_text')
        var.set(f"Local IP : {my_ip}")

    async def _run_async_mainloop(self):
        while True:
            await asyncio.sleep(1 / TARGET_FPS)
            try:
                self.top_level.update()
            except tk.TclError:
                break

    def on_log_added(self):
        print('aa')

    def on_log_type_changed(self):
        print('a')

    def on_click_clear(self):
        self.log_listener.clear()
