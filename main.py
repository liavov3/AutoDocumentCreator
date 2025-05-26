from DataManager_refactor import *

root = None
path, save_path = None, None
clicked_select, clicked_save = False, False
submit_btn = None


def main_gui():
    '''
    collected all the relevant data by the user
    and calling the function in DataManager
    '''
    global root, submit_btn
    root = Tk()
    root.geometry('240x160')

    path_button = Button(root, text='Select experiment', command=path_to_data)
    save_button = Button(root, text='Save document', command=path_to_save)

    def submit():
        global path, save_path, clicked_select, clicked_save
        main(path, save_path)

    submit_btn = Button(root, text='Submit', command=submit, state=DISABLED)

    path_button.grid(row=4, columnspan=3, padx=2, pady=2)
    save_button.grid(row=5, columnspan=3, padx=2, pady=2)
    submit_btn.grid(row=6, columnspan=3, padx=2, pady=2)

    root.mainloop()


def path_to_data():
    global path, clicked_select
    path = filedialog.askdirectory()
    if path is not None:
        clicked_select = True
    check()


def path_to_save():
    global save_path, clicked_save
    save_path = filedialog.askdirectory()
    if save_path is not None:
        clicked_save = True
    check()


def check():
    global submit_btn, clicked_save, clicked_select
    if clicked_save is True and clicked_select is True:
        submit_btn["state"] = "enable"


if __name__ == "__main__":
    main_gui()


