import tkinter as tk
from queue import Empty
from signal import signal, \
    SIGINT
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk, N, S, E, W, END
from threading import Thread
from CustomTkinter.customtkinter.windows.ctk_tk import CTk
from CustomTkinter.customtkinter.widgets.ctk_button import CTkButton
from CustomTkinter.customtkinter.widgets.ctk_label import CTkLabel
from _00_base import configure_logger_and_queue
from _01_py_yt_org import YTdownloader
from _00_config import possible_out_paths
from PIL import Image, ImageTk


class ConsoleUi(configure_logger_and_queue):
    """Poll messages from a logging queue and display them in a scrolled text widget"""

    BTN_IMG_SIZE = 20

    def __init__(self, frame):

        super(ConsoleUi, self).__init__()

        self.frame = frame

        # add a button to clear the text

        self.button_clear_console = CTkButton(self.frame, text='CLEAR CONSOLE', fg_color=("gray75", "gray30"),
                                              pady=10, padx=20, command=self.clear_console)
        self.button_clear_console.grid(column=0, row=0, sticky=W)

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
    BTN_IMG_SIZE = 20

    def __init__(self,
                 frame,
                 input_frame):
        super(FormControls, self).__init__()

        self.input_frame = input_frame

        self.frame = frame

        add_image = ImageTk.PhotoImage(
            Image.open("icons/add-icon.png").resize((self.BTN_IMG_SIZE, self.BTN_IMG_SIZE), Image.ANTIALIAS))

        download_image = ImageTk.PhotoImage(
            Image.open("icons/download-icon.png").resize((self.BTN_IMG_SIZE, self.BTN_IMG_SIZE), Image.ANTIALIAS))

        check_image = ImageTk.PhotoImage(
            Image.open("icons/check-icon.png").resize((self.BTN_IMG_SIZE, self.BTN_IMG_SIZE), Image.ANTIALIAS))

        self.button_just_add = CTkButton(self.frame, text='JUST ADD', fg_color=("gray75", "gray30"),
                                         command=self.just_add, image=add_image)

        self.button_just_add.grid(column=0, row=1, pady=10, padx=20, sticky=W)

        self.download_path = tk.StringVar()
        self.combobox_download_dir = ttk.Combobox(
            self.frame,
            textvariable=self.download_path,
            width=45,
            state='readonly',
            values=possible_out_paths
        )
        self.combobox_download_dir.current(0)
        self.combobox_download_dir.grid(column=1, row=2, pady=10, padx=20, sticky=W)

        self.button_download = CTkButton(self.frame, text='DOWNLOAD', fg_color=("gray75", "gray30"),
                                         command=self.download_master, image=download_image)

        self.button_download.grid(column=0, row=2, pady=10, padx=20, sticky=W)

        self.button_check_watched = CTkButton(self.frame, text='CHECK WATCHED', fg_color=("gray75", "gray30"),
                                              command=self.check_watched, image=check_image)

        self.button_check_watched.grid(column=0, row=3, pady=10, padx=20, sticky=W)

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

        download_status = self.download_unwatched_vids(download_path=self.download_path.get())
        if download_status == 'success':
            self.save_on_disk()
        else:
            downloaded_successfully = '\n'.join(download_status)
            self._log.error(f"I could only download:\n{downloaded_successfully}")

    def get_input_links_from_GUI(self):
        self.all_input_rows = list(
            filter(lambda x: x != '', [entry.strip() for entry in self.input_frame.return_input_data().split('\n')]))
        self.all_input_rows = [entry.split('&')[0] if '&' in entry else entry for entry in self.all_input_rows]


class FormInput:

    def __init__(self, frame):
        self.frame = frame

        self.scrolled_text_input_links = ScrolledText(self.frame, width=50, height=45)
        self.scrolled_text_input_links.grid(row=0, column=0, sticky=(N, S, W, E))
        self.scrolled_text_input_links.configure(font='TkFixedFont')

    def return_input_data(self):
        return self.scrolled_text_input_links.get("1.0", END)


class App:
    WIDTH = 1300
    HEIGHT = 920

    def __init__(self, root):
        self.root = root
        root.title('Youtube Organizer')
        root.iconbitmap(r'icons\icon_yt.ico')

        ws = root.winfo_screenwidth()
        hs = root.winfo_screenheight()
        x = (ws / 2) - (self.WIDTH / 2)
        y = (hs / 2) - (self.HEIGHT / 2) - 40

        root.geometry('%dx%d+%d+%d' % (self.WIDTH, self.HEIGHT, x, y))
        root.resizable(False, False)

        input_frame = CTkLabel(master=root, text="Input", text_font=("Roboto Medium", -18))
        input_frame.grid(row=1, column=0, sticky="nsew")
        self.input_frame = FormInput(input_frame)

        controls_frame = CTkLabel(master=root, text="Controls", text_font=("Roboto Medium", -18))
        controls_frame.grid(row=0, column=0, sticky="nsew")
        self.controls_frame = FormControls(controls_frame,
                                           self.input_frame)

        console_frame = CTkLabel(master=root, text="Log", text_font=("Roboto Medium", -18))
        console_frame.grid(row=0, column=1, sticky="nsew", rowspan=2)
        self.console_frame = ConsoleUi(console_frame)

        self.root.protocol('WM_DELETE_WINDOW', self.quit)
        self.root.bind('<Control-q>', self.quit)
        signal(SIGINT, self.quit)

    def quit(self):
        self.root.destroy()


def main():
    root = CTk()

    app = App(root)
    app.root.mainloop()


if __name__ == '__main__':
    main()
