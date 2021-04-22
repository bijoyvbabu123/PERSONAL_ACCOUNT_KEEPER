"""This module is to enter the home expenditure records"""
import tkinter
import os
from ttkwidgets import autocomplete
from tkinter import ttk
import tkcalendar


def main_function():
    root = tkinter.Tk()
    root.minsize(width=1150, height=660)
    root.title('EXPENDITURE ENTRY')
    root.iconbitmap(os.path.join('FILES', 'HOME_ACCOUNTING', 'icons', 'home_acc_exp_entry.ico'))
    root.focus_force()

    style = ttk.Style()
    style.theme_use("clam")  # default is vista
    style.configure("Treeview", background='white', fieldbackground='white', rowheight=25,
                    font='TkDefaultFont 9 italic')
    style.configure("Treeview.Heading", font='TkDefaultFont 10 bold')
    style.map("Treeview", background=[('selected', 'RoyalBlue3')])

    date_picker = tkcalendar.DateEntry(root, date_pattern='dd/mm/yyyy')
    date_picker.place(relx=0.02, rely=0.0256, relwidth=0.15)
    date_picker.focus_set()

    label_item = tkinter.Label(root, text='Item', font='TkDefaultFont 10 italic')
    label_item.place(relx=0.02, rely=0.0256 * 4 - 0.0065)
    item_entry = autocomplete.AutocompleteEntry(root, completevalues=[])
    item_entry.place(relx=0.02, rely=0.0256 * 5, relwidth=0.15)

    label_category = tkinter.Label(root, text='Category', font='TkDefaultFont 10 italic')
    label_category.place(relx=0.02, rely=0.0256 * 8 - 0.0065)
    category_entry = autocomplete.AutocompleteEntry(root, completevalues=[])
    category_entry.place(relx=0.02, rely=0.0256 * 9, relwidth=0.15)

    label_mode = tkinter.Label(root, text='Mode Of Payment', font='TkDefaultFont 10 italic')
    label_mode.place(relx=0.02, rely=0.0256 * 12 - 0.0065)
    mode_entry = autocomplete.AutocompleteEntry(root, completevalues=[])
    mode_entry.place(relx=0.02, rely=0.0256 * 13, relwidth=0.15)

    label_unit = tkinter.Label(root, text='Unit (Quantity Description)', font='TkDefaultFont 10 italic')
    label_unit.place(relx=0.02, rely=0.0256 * 16 - 0.0065)
    unit_entry = autocomplete.AutocompleteEntry(root, completevalues=[])
    unit_entry.place(relx=0.02, rely=0.0256 * 17, relwidth=0.15)

    label_quantity = tkinter.Label(root, text='Quantity', font='TkDefaultFont 10 italic')
    label_quantity.place(relx=0.02, rely=0.0256 * 20 - 0.0065)
    quantity_entry = tkinter.Entry(root)
    quantity_entry.place(relx=0.02, rely=0.0256 * 21, relwidth=0.15)

    label_rate = tkinter.Label(root, text='Rate', font='TkDefaultFont 10 italic')
    label_rate.place(relx=0.02, rely=0.0256 * 24 - 0.0065)
    rate_entry = tkinter.Entry(root)
    rate_entry.place(relx=0.02, rely=0.0256 * 25, relwidth=0.15)

    label_dis_all = tkinter.Label(root, text='Dis. Allowed', font='TkDefaultFont 10 italic')
    label_dis_all.place(relx=0.02, rely=0.0256 * 28 - 0.0065)
    dis_all_entry = tkinter.Entry(root)
    dis_all_entry.place(relx=0.02, rely=0.0256 * 29, relwidth=0.07)

    label_dis_rec = tkinter.Label(root, text='Dis. Received', font='TkDefaultFont 10 italic')
    label_dis_rec.place(relx=0.02 + 0.07 + 0.01, rely=0.0256 * 28 - 0.0065)
    dis_rec_entry = tkinter.Entry(root)
    dis_rec_entry.place(relx=0.02 + 0.07 + 0.01, rely=0.0256 * 29, relwidth=0.07)

    label_net = tkinter.Label(root, text='Net Price', font='TkDefaultFont 10 italic')
    label_net.place(relx=0.02, rely=0.0256 * 32 - 0.0065)
    net_entry = tkinter.Entry(root)
    net_entry.place(relx=0.02, rely=0.0256 * 33, relwidth=0.15)

    button_add_done = tkinter.Button(root, text='ADD',  relief='groove', font='TkDefaultFont 11 bold italic')
    button_add_done.place(relx=0.045, rely=0.0256 * 36, relheight=0.0256 * 2, relwidth=0.10)

    button_save_exit = tkinter.Button(root, text='SAVE and EXIT', relief='groove', font='TkDefaultFont 11 bold italic')
    button_save_exit.place(relwidth=0.15, relheight=0.0256 * 3, relx=0.425, rely=0.870)

    button_no_save_exit = tkinter.Button(root, text='EXIT without SAVING', relief='groove', font='TkDefaultFont 11 bold italic')
    button_no_save_exit.place(relwidth=0.15, relheight=0.0256 * 3, relx=0.615, rely=0.870)

    button_edit = tkinter.Button(root, text='Edit', state=tkinter.DISABLED, relief='groove')
    button_edit.place(relwidth=0.07, relheight=0.0256 * 2, rely=0.79, relx=0.47)

    button_delete = tkinter.Button(root, text='Delete', state=tkinter.DISABLED, relief='groove')
    button_delete.place(relwidth=0.07, relheight=0.0256 * 2, rely=0.79, relx=0.56)

    button_clear_selection = tkinter.Button(root, text='Clear Selection', state=tkinter.DISABLED, relief='groove')
    button_clear_selection.place(relwidth=0.07, relheight=0.0256 * 2, rely=0.79, relx=0.65)

    button_item_list = tkinter.Button(root, text='..', font='TkDefaultFont 11 bold italic')
    button_item_list.place(relx=0.18, rely=0.0256 * 5, height=21, relwidth=0.02)

    button_category_list = tkinter.Button(root, text='..', font='TkDefaultFont 11 bold italic')
    button_category_list.place(relx=0.18, rely=0.0256 * 9, height=21, relwidth=0.02)

    button_mode_list = tkinter.Button(root, text='..', font='TkDefaultFont 11 bold italic')
    button_mode_list.place(relx=0.18, rely=0.0256 * 13, height=21, relwidth=0.02)

    button_unit_list = tkinter.Button(root, text='..', font='TkDefaultFont 11 bold italic')
    button_unit_list.place(relx=0.18, rely=0.0256 * 17, height=21, relwidth=0.02)

    label_number_of_entries = tkinter.Label(root, text='No. of entries = 0', font='TkDefaultFont 10 italic')
    label_number_of_entries.place(relx=0.22, rely=0.73)

    label_total_gross = tkinter.Label(root, text='Total Gross = 0.00', font='TkDefaultFont 10 italic')
    label_total_gross.place(relx=0.63, rely=0.73)

    label_total_net = tkinter.Label(root, text='Total Net = 0.00', font='TkDefaultFont 10 italic')
    label_total_net.place(relx=0.865, rely=0.73)

    tree_scroll = tkinter.Scrollbar(root, orient=tkinter.VERTICAL)
    tree_scroll.place(relheight=0.7, relx=0.97, rely=0.03)

    tree = ttk.Treeview(root, show=['headings'], yscrollcommand=tree_scroll.set, selectmode='browse')
    tree.place(relwidth=0.75, relheight=0.7, relx=0.22, rely=0.03)
    tree_scroll.config(command=tree.yview)

    tree['columns'] = ('date', 'item', 'cat', 'mode', 'unit', 'qty', 'rate', 'da', 'dr', 'net')
    root.update()
    tree.update()
    tree.column('date', anchor=tkinter.CENTER, width=int(tree.winfo_width() / 10))
    tree.column('item', anchor=tkinter.W, width=int(tree.winfo_width() / 8))
    tree.column('cat', anchor=tkinter.W, width=int(tree.winfo_width() / 7.5))
    tree.column('mode', anchor=tkinter.W, width=int(tree.winfo_width() / 9))
    tree.column('unit', anchor=tkinter.W, width=int(tree.winfo_width() / 12))
    tree.column('qty', anchor=tkinter.E, width=int(tree.winfo_width() / 11))
    tree.column('rate', anchor=tkinter.E, width=int(tree.winfo_width() / 11))
    tree.column('da', anchor=tkinter.E, width=int(tree.winfo_width() / 13))
    tree.column('dr', anchor=tkinter.E, width=int(tree.winfo_width() / 13))
    tree.column('net', anchor=tkinter.E, width=int(tree.winfo_width() / 8.5))
    tree.heading('date', text='Date')  # , anchor=tkinter.W
    tree.heading('item', text='Item')
    tree.heading('cat', text='Category')
    tree.heading('mode', text='Mode')
    tree.heading('unit', text='Unit')
    tree.heading('qty', text='Quantity')
    tree.heading('rate', text='Rate')
    tree.heading('da', text='Dis. All')
    tree.heading('dr', text='Dis. Rec')
    tree.heading('net', text='Net Price')
    tree.tag_configure('odd', background="light sky blue")

    root.mainloop()
