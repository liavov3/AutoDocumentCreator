from utils_refactor import *


class ProgressBar():
    def __init__(self, total_tasks: list):
        self.total_tasks = sum(len(sublist) for sublist in total_tasks)

        self.top_level = Toplevel()
        self.top_level.title = "Progress"
        self.top_level.geometry('400x150')

        self.frame = Frame(self.top_level)   #, padx=10, pady=10)
        self.frame.pack(fill=BOTH, expand=True)

        self.progress_var = IntVar()
        self.progress_bar = Progressbar(self.frame, orient="horizontal", length=300,
                                        mode="determinate", variable=self.progress_var)
        self.progress_bar.pack(pady=10)

        self.progress_label = Label(self.frame, text="Progress: 0%")
        self.progress_label.pack()

    def update_progress(self, index):
        progress = int((index + 1) / self.total_tasks * 100)
        self.progress_var.set(progress)
        self.progress_label.config(text=f"Progress: {progress}%")
        self.top_level.update_idletasks()

    def close(self):
        self.top_level.destroy()

    # def get_len_tasks(self):
    #     tasks_amount = sum(len(sublist) for sublist in self.total_tasks)
    #     self.total_tasks = tasks_amount
