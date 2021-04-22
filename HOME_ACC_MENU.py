"""This menu provides the navigation to different 'HOME ACCOUNTING' windows"""
import tkinter
import os
import HOME_ACC_EXP_ENTRY
import HOME_ACC_EXP_HISTORY
import HOME_ACC_BACKUP


def main_function():
    root = tkinter.Tk()
    root.minsize(400, 400)
    root.title("HOME ACCOUNTING")
    root.iconbitmap(os.path.join('FILES', 'HOME_ACCOUNTING', 'icons', 'home_accounting.ico'))

    def exp_entry():
        root.destroy()
        HOME_ACC_EXP_ENTRY.main_function()

    def exp_history():
        root.destroy()
        HOME_ACC_EXP_HISTORY.main_function()

    def backup():
        root.destroy()
        HOME_ACC_BACKUP.main_function()

    home_acc_exp_entry = tkinter.PhotoImage(
        file=os.path.join('FILES', 'HOME_ACCOUNTING', 'icons', 'home_acc_exp_entry.png'))
    home_acc_exp_history = tkinter.PhotoImage(
        file=os.path.join('FILES', 'HOME_ACCOUNTING', 'icons', 'home_acc_exp_history.png'))
    backup_img = tkinter.PhotoImage(file=os.path.join('FILES', 'icons', 'backup.png'))

    button_exp_entry = tkinter.Button(root, image=home_acc_exp_entry, relief='groove', command=exp_entry)
    button_exp_entry.place(relx=0.1, rely=0.1)
    label_exp_entry = tkinter.Label(root, text="EXPENDITURE ENTRY", font='TkDefaultFont 9 italic')
    label_exp_entry.place(relx=0.1, rely=0.44)
    label_exp_entry.bind("<Button-1>", lambda event=None: button_exp_entry.invoke())
    button_exp_entry.bind("<Enter>",
                          lambda event=None: label_exp_entry.config(font='TkDefaultFont 9 italic underline',
                                                                    fg='DodgerBlue2'))
    button_exp_entry.bind("<Leave>",
                          lambda event=None: label_exp_entry.config(font='TkDefaultFont 9 italic',
                                                                    fg='SystemButtonText'))
    label_exp_entry.bind("<Enter>",
                         lambda event=None: label_exp_entry.config(font='TkDefaultFont 9 italic underline',
                                                                   fg='DodgerBlue2'))
    label_exp_entry.bind("<Leave>",
                         lambda event=None: label_exp_entry.config(font='TkDefaultFont 9 italic',
                                                                   fg='SystemButtonText'))

    button_exp_history = tkinter.Button(root, image=home_acc_exp_history, relief='groove', command=exp_history)
    button_exp_history.place(relx=0.55, rely=0.1)
    label_exp_history = tkinter.Label(root, text="EXPENDITURE HISTORY", font='TkDefaultFont 9 italic')
    label_exp_history.place(relx=0.52, rely=0.44)
    label_exp_history.bind("<Button-1>", lambda event=None: button_exp_history.invoke())
    button_exp_history.bind("<Enter>",
                            lambda event=None: label_exp_history.config(font='TkDefaultFont 9 italic underline',
                                                                        fg='DodgerBlue2'))
    button_exp_history.bind("<Leave>",
                            lambda event=None: label_exp_history.config(font='TkDefaultFont 9 italic',
                                                                        fg='SystemButtonText'))
    label_exp_history.bind("<Enter>",
                           lambda event=None: label_exp_history.config(font='TkDefaultFont 9 italic underline',
                                                                       fg='DodgerBlue2'))
    label_exp_history.bind("<Leave>",
                           lambda event=None: label_exp_history.config(font='TkDefaultFont 9 italic',
                                                                       fg='SystemButtonText'))

    button_backup = tkinter.Button(root, image=backup_img, relief='groove', command=backup)
    button_backup.place(relx=0.29, rely=0.55)
    label_backup = tkinter.Label(root, text="BACKUP", font='TkDefaultFont 9 italic')
    label_backup.place(relx=0.38, rely=0.89)
    label_backup.bind("<Button-1>", lambda event=None: button_backup.invoke())
    button_backup.bind("<Enter>",
                       lambda event=None: label_backup.config(font='TkDefaultFont 9 italic underline',
                                                              fg='DodgerBlue2'))
    button_backup.bind("<Leave>",
                       lambda event=None: label_backup.config(font='TkDefaultFont 9 italic',
                                                              fg='SystemButtonText'))
    label_backup.bind("<Enter>",
                      lambda event=None: label_backup.config(font='TkDefaultFont 9 italic underline',
                                                             fg='DodgerBlue2'))
    label_backup.bind("<Leave>",
                      lambda event=None: label_backup.config(font='TkDefaultFont 9 italic',
                                                             fg='SystemButtonText'))

    root.mainloop()
