"""This module provides navigation to various domains that will be available is this software"""

import tkinter
import os
import HOME_ACC_MENU


def main_function():
    main_menu_root = tkinter.Tk()
    main_menu_root.minsize(400, 400)
    main_menu_root.resizable(False, False)
    main_menu_root.title("PERSONAL ACCOUNT KEEPER")
    main_menu_root.iconbitmap(os.path.join('FILES', 'icons', 'kit.ico'))

    def home_accounting():
        main_menu_root.destroy()
        HOME_ACC_MENU.main_function()
        main_function()

    home_accounting_icon = tkinter.PhotoImage(
        file=os.path.join('FILES', 'HOME_ACCOUNTING', 'icons', 'home_accounting_menu.png'))
    label_home_accounting = tkinter.Label(main_menu_root, text='HOME ACCOUNTING', font='TkDefaultFont 9 italic')
    label_home_accounting.place(relx=0.120, rely=0.52)
    label_home_accounting.bind("<Enter>",
                               lambda event=None: label_home_accounting.config(font='TkDefaultFont 9 italic underline',
                                                                               fg='DodgerBlue2'))
    label_home_accounting.bind("<Leave>", lambda event=None: label_home_accounting.config(font='TkDefaultFont 9 italic',
                                                                                          fg='SystemButtonText'))

    label_coming = tkinter.Label(main_menu_root, text="** COMING", font='TkDefaultFont 13 italic')
    label_soon = tkinter.Label(main_menu_root, text="SOON **", font='TkDefaultFont 13 italic')
    label_coming.place(relx=0.6, rely=0.25)
    label_soon.place(relx=0.62, rely=0.35)

    button_home_accounting = tkinter.Button(main_menu_root, image=home_accounting_icon, command=home_accounting, relief='groove')
    button_home_accounting.place(relx=0.1, rely=0.2)
    button_home_accounting.bind("<Enter>",
                                lambda event=None: label_home_accounting.config(font='TkDefaultFont 9 italic underline',
                                                                                fg='DodgerBlue2'))
    button_home_accounting.bind("<Leave>", lambda event=None: label_home_accounting.config(font='TkDefaultFont 9 italic',
                                                                                           fg='SystemButtonText'))
    label_home_accounting.bind("<Button-1>", lambda event=None: button_home_accounting.invoke())

    main_menu_root.mainloop()
