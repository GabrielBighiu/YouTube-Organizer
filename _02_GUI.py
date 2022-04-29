import tkinter as tk
from queue import Empty
from signal import signal,\
    SIGINT
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk, N, S, E, W, END
from threading import Thread

from _00_base import configure_logger_and_queue
from _01_py_yt_org import YTdownloader
from _00_config import possible_out_paths

class ConsoleUi(configure_logger_and_queue):
    """Poll messages from a logging queue and display them in a scrolled text widget"""

    def __init__(self, frame):

        super(ConsoleUi, self).__init__()

        self.frame = frame

        # add a button to clear the text
        self.button_just_add = ttk.Button(self.frame, text='CLEAR CONSOLE', command=self.clear_console)
        self.button_just_add.grid(column=0, row=0, sticky=W)

        # Create a ScrolledText wdiget
        self.scrolled_text = ScrolledText(frame, state='disabled', width=100, height=50)
        self.scrolled_text.grid(row=1, column=0, sticky=(N, S, W, E))
        self.scrolled_text.configure(font='TkFixedFont')
        self.scrolled_text.tag_config('INFO', foreground='black')
        self.scrolled_text.tag_config('DEBUG', foreground='gray')
        self.scrolled_text.tag_config('WARNING', foreground='orange')
        self.scrolled_text.tag_config('ERROR', foreground='red')
        self.scrolled_text.tag_config('CRITICAL', foreground='red', underline=1)

        # Start polling messages from the queue
        self.frame.after(100, self.poll_log_queue)

    def display(self, record):
        msg = self.queue_handler.format(record)
        self.scrolled_text.configure(state='normal')
        self.scrolled_text.insert(tk.END, msg + '\n', record.levelname)
        self.scrolled_text.configure(state='disabled')

        # Autoscroll to the bottom
        self.scrolled_text.yview(tk.END)

    def poll_log_queue(self):
        # Check every 100ms if there is a new message in the queue to display
        while True:
            try:
                record = self.log_queue.get(block=False)
            except Empty:
                break
            else:
                self.display(record)
        self.frame.after(100, self.poll_log_queue)

    def clear_console(self):
        self.scrolled_text.configure(state='normal')
        self.scrolled_text.delete('1.0', END)
        self.scrolled_text.configure(state='disabled')

class FormControls(YTdownloader,
                   configure_logger_and_queue):

    def __init__(self,
                 frame,
                 input_frame):
        super(FormControls, self).__init__()

        self.input_frame = input_frame

        self.frame = frame

        self.button_just_add = ttk.Button(self.frame, text='JUST ADD', command=self.just_add)
        self.button_just_add.grid(column=0, row=1, sticky=W)

        self.download_path = tk.StringVar()
        self.combobox_download_dir = ttk.Combobox(
            self.frame,
            textvariable=self.download_path,
            width=45,
            state='readonly',
            values=possible_out_paths
        )
        self.combobox_download_dir.current(0)
        self.combobox_download_dir.grid(column=1, row=2, sticky=(W))

        self.button_download = ttk.Button(self.frame, text='DOWNLOAD', command=self.download_master)
        self.button_download.grid(column=0, row=2, sticky=W)

        self.button_check_watched = ttk.Button(self.frame, text='CHECK WATCHED', command=self.check_watched)
        self.button_check_watched.grid(column=0, row=3, sticky=W)

    def just_add(self):
        self._log.info('##### Just adding to catalog... #####')
        self.get_input_links_from_GUI()
        self.analyze_input()
        self.save_on_disk()

    def check_watched(self):
        self._log.info('##### Checking watched... #####')
        self.get_input_links_from_GUI()
        self.analyze_input()

    def download_master(self):
        self._log.info('##### Downloading ... #####')
        t = Thread(target=self.download_slave, args=())
        t.start()

    def download_slave(self):

        self.get_input_links_from_GUI()
        self.analyze_input()

        download_status = self.download_unwatched_vids(download_path = self.download_path.get())
        if download_status == 'success':
            self.save_on_disk()
        else:
            downloaded_successfully = '\n'.join(download_status)
            self._log.error(f"I could only download:\n{downloaded_successfully}")

    def get_input_links_from_GUI(self):
        self.all_input_rows = list(filter(lambda x:x!='', [entry.strip() for entry in self.input_frame.return_input_data().split('\n')]))
        self.all_input_rows = [entry.split('&')[0] if '&' in entry else entry for entry in self.all_input_rows]

class FormInput():

    def __init__(self, frame):
        self.frame = frame

        self.scrolled_text_input_links = ScrolledText(self.frame, width=50, height=45)
        self.scrolled_text_input_links.grid(row=0, column=0, sticky=(N, S, W, E))
        self.scrolled_text_input_links.configure(font='TkFixedFont')

    def return_input_data(self):
        return self.scrolled_text_input_links.get("1.0", END)

class App():

    def __init__(self, root):
        self.root = root
        root.title('pyYoutube_dll')

        input_frame = ttk.Labelframe(text="Input")
        input_frame.grid(row=1, column=0, sticky="nsew")
        self.input_frame = FormInput(input_frame)

        controls_frame = ttk.Labelframe(text="Controls")
        controls_frame.grid(row=0, column=0, sticky="nsew")
        self.controls_frame = FormControls(controls_frame,
                                           self.input_frame)

        console_frame = ttk.Labelframe(text="Console")
        console_frame.grid(row=0, column=1, sticky="nsew", rowspan=2)
        self.console_frame = ConsoleUi(console_frame)

        self.root.protocol('WM_DELETE_WINDOW', self.quit)
        self.root.bind('<Control-q>', self.quit)
        signal(SIGINT, self.quit)

    def quit(self):
        self.root.destroy()

def main():
    root = tk.Tk()
    app = App(root)
    app.root.mainloop()

if __name__ == '__main__':
    main()