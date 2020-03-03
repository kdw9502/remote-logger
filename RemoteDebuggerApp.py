import asyncio
import tkinter as tk
import tkinter.ttk

import pygubu

from LogListener import LogListener, LogType
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

        self.is_show_debug: tk.BooleanVar = self.builder.get_variable('is_show_debug')
        self.is_show_warning: tk.BooleanVar = self.builder.get_variable('is_show_warning')
        self.is_show_error: tk.BooleanVar = self.builder.get_variable('is_show_error')

        self.is_show_debug.set(True)
        self.is_show_warning.set(True)
        self.is_show_error.set(True)

        self._set_callbacks()

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

    def on_log_added(self):
        log = self.log_listener.logs[-1]

        if self._is_enabled_log(log):
            self.log_listbox.insert(self.log_listbox.size() + 1, log.message)

    def on_log_type_changed(self):
        logs = self._get_filtered_logs()
        self._set_listbox_with_logs(logs)

    def _get_filtered_logs(self):
        logs = []
        for log in self.log_listener.logs:
            if self._is_enabled_log(log):
                logs.append(log)

        return logs

    def _is_enabled_log(self, log):
        return log.log_type == LogType.DEBUG and self.is_show_debug.get() or \
               log.log_type == LogType.WARNING and self.is_show_warning.get() or \
               log.log_type == LogType.ERROR and self.is_show_error.get()

    def on_click_clear(self):
        self.log_listener.clear()
        self._clear_listbox()

    def on_listbox_select(self, event: tk.Event):
        widget = event.widget
        if len(widget.curselection()) > 0:
            index = widget.curselection()[0]
            message = self.log_listbox.get(index)
            log = self.log_listener.find_log_by_message(message)

            self.full_log_text.config(state=tk.NORMAL)
            self._change_log_text(str(log))

            # to readonly
            self.full_log_text.config(state=tk.DISABLED)

    def _change_log_text(self, text):

        self.full_log_text.delete('1.0', tk.END)
        self.full_log_text.insert('1.0', text)

    def _clear_listbox(self):
        self.log_listbox.delete(0, self.log_listbox.size())

    def _set_listbox_with_logs(self, logs):
        self._clear_listbox()
        for index, log in enumerate(logs):
            self.log_listbox.insert(index, log.message)
