import asyncio
import tkinter as tk
import tkinter.ttk

import pygubu

from LogListener import LogListener
from UDPBroadCaster import UDPBroadCaster

TARGET_FPS = 30


class RemoteDebuggerApp:
    def __init__(self):
        self.builder = pygubu.Builder()

        self.top_level = None
        self._load_from_file()

        self.log_listbox: tk.Listbox = self.builder.get_object('LogListBox')
        self.full_log_text: tk.Text = self.builder.get_object('LogText')

        self.broad_caster = UDPBroadCaster()
        self._init_broad_caster()

        self.log_listener = LogListener.create_with_new_log_callback(self.on_log_added)

        self._set_callbacks()

        self.is_show_debug = None
        self.is_show_warning = None
        self.is_show_error = None

    async def run(self):
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
        asyncio.create_task(self.broad_caster.start_broadcast())
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

    def _set_tk_vars(self):
        self.is_show_debug = self.builder.get_variable('is_show_debug')
        self.is_show_warning = self.builder.get_variable('is_show_warning')
        self.is_show_error = self.builder.get_variable('is_show_error')

    def on_log_added(self):
        self.log_listbox.insert(self.log_listbox.size() + 1, self.log_listener.logs[-1].message)

    def on_log_type_changed(self):
        print('a')

    def on_click_clear(self):
        self.log_listener.clear()
        self.log_listbox.delete(0, self.log_listbox.size())

    def on_listbox_select(self, event: tk.Event):
        widget = event.widget
        if len(widget.curselection()) > 0:
            index = widget.curselection()[0]

            self.full_log_text.config(state=tk.NORMAL)

            self.full_log_text.delete('1.0', tk.END)
            self.full_log_text.insert('1.0', self.log_listener.logs[index].to_json())

            # to readonly
            self.full_log_text.config(state=tk.DISABLED)
