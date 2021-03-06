"""This module is to enter the home expenditure records"""
import tkinter
import os
from ttkwidgets import autocomplete
from tkinter import ttk
from tkinter import messagebox
import tkcalendar
import sqlite3
import re
import datetime


def main_function():
    root = tkinter.Tk()
    root.minsize(width=1150, height=660)
    root.title('EXPENDITURE ENTRY')
    root.iconbitmap(os.path.join('FILES', 'HOME_ACCOUNTING', 'icons', 'home_acc_exp_entry.ico'))
    root.focus_force()

    # creating folder, database file and required tables initially if not existing
    def file_initialisation():

        if not os.path.exists(os.path.join('FILES', 'HOME_ACCOUNTING', 'DATA')):
            os.mkdir(os.path.join('FILES', 'HOME_ACCOUNTING', 'DATA'))

        db_connection = sqlite3.connect(os.path.join('FILES', 'HOME_ACCOUNTING', 'DATA', 'home_accounting.db'))
        db_cursor = db_connection.cursor()

        # table for storing current entries and clearing if any previous exists
        db_cursor.execute("""CREATE TABLE IF NOT EXISTS entries (
            date TEXT,
            item TEXT,
            category TEXT,
            mode TEXT,
            unit TEXT,
            quantity REAL,
            rate REAL,
            da REAL,
            dr REAL,
            net REAL)""")
        db_connection.commit()
        db_cursor.execute("""DELETE FROM entries""")
        db_connection.commit()

        # tables for storing the defaults
        db_cursor.execute("""CREATE TABLE IF NOT EXISTS item (item TEXT)""")
        db_connection.commit()
        db_cursor.execute("""CREATE TABLE IF NOT EXISTS category (category TEXT)""")
        db_connection.commit()
        db_cursor.execute("""CREATE TABLE IF NOT EXISTS mode (mode TEXT)""")
        db_connection.commit()
        db_cursor.execute("""CREATE TABLE IF NOT EXISTS unit (unit TEXT)""")
        db_connection.commit()
        db_cursor.execute("""CREATE TABLE IF NOT EXISTS pair (item TEXT, category TEXT)""")
        db_connection.commit()

        db_connection.close()

    # function for setting the auto complete values for the auto complete widgets .. accepts a tuple with widget and name
    def set_auto_completion(field):
        db_connection = sqlite3.connect(os.path.join('FILES', 'HOME_ACCOUNTING', 'DATA', 'home_accounting.db'))
        db_cursor = db_connection.cursor()

        data = db_cursor.execute("SELECT * FROM " + field[1]).fetchall()

        l = []
        for x in range(len(data)):
            l.append(data[x][0])

        field[0].set_completion_list(l)

    # function for validating the input as only numeric
    def only_numeric(letter):
        if bool(re.match('\d*\.\d*$', letter)):
            return True
        if letter.isdigit():
            return True
        if letter == '':
            return True
        else:
            return False

    # function to facilitate Return for going to next widget
    def next_widget_on_return(event):
        x = event.widget.tk_focusNext()
        x.focus()
        if x != button_add_done:
            x.select_range(0, tkinter.END)
        return "break"

    # validation of date picker entry as date only on focus out
    def date_only(event):
        if not bool(re.match('\d\d\/\d\d\/\d\d\d\d', date_picker.get())):
            messagebox.showerror('INVALID VALUE', "Please enter a valid date in the format dd/mm/yyyy")
            date_picker.focus_set()
            date_picker.select_range(0, tkinter.END)
        else:
            try:
                datetime.datetime.strptime(date_picker.get(), "%d/%m/%Y").date()
            except ValueError:
                messagebox.showerror('INVALID VALUE', "Please enter a valid date in the format dd/mm/yyyy")
                date_picker.focus_set()
                date_picker.select_range(0, tkinter.END)

    # capitalizing the text entries
    def capitalize_words(event, widget):
        x = ''
        if event is not None:
            x = event.widget.get().strip()
        elif widget is not None:
            x = widget.get().strip()
        if x != '':
            x = x[0].upper() + x[1:]
            if event is not None:
                event.widget.delete(0, tkinter.END)
                event.widget.insert(0, x)
            elif widget is not None:
                widget.delete(0, tkinter.END)
                widget.insert(0, x)

    # function for auto filling of category
    def category_auto_fill(event):
        capitalize_words(event, None)

        if item_entry.get() != '':
            db_connection = sqlite3.connect(os.path.join('FILES', 'HOME_ACCOUNTING', 'DATA', 'home_accounting.db'))
            db_cursor = db_connection.cursor()

            db_cursor.execute("SELECT category FROM pair WHERE item='" + item_entry.get() + "' COLLATE NOCASE")
            data = db_cursor.fetchall()

            if bool(data):
                category_entry.delete(0, tkinter.END)
                category_entry.insert(0, data[0][0])
                category_entry.config(state='disabled')
                mode_entry.focus_set()
            else:
                category_entry.config(state='normal')
                category_entry.focus_set()
                category_entry.select_range(0, tkinter.END)

    # function for formatting the numerical inputs in various fields accordingly
    def format_numerals(event, widget):
        if event is not None:
            if event.widget.get() != '':
                x = float(event.widget.get())
                event.widget.delete(0, tkinter.END)

                if x != 0 and event.widget == quantity_entry:
                    event.widget.insert(0, "{:.3f}".format(x))
                elif x != 0 and event.widget == rate_entry:
                    event.widget.insert(0, "{:.2f}".format(x))
                elif event.widget in [dis_all_entry, dis_rec_entry, net_entry]:
                    event.widget.insert(0, "{:.2f}".format(x))
        elif widget is not None:
            if widget.get() != '':
                x = float(widget.get())
                widget.delete(0, tkinter.END)

                if x != 0 and widget == quantity_entry:
                    widget.insert(0, "{:.3f}".format(x))
                elif x != 0 and widget == rate_entry:
                    widget.insert(0, "{:.2f}".format(x))
                elif widget in [dis_all_entry, dis_rec_entry, net_entry]:
                    widget.insert(0, "{:.2f}".format(x))

    # function to calculate the net price after leaving the dis rec entry if possible
    def net_price_if_possible(event):
        format_numerals(event, None)
        empty = 0
        for i in [quantity_entry, rate_entry, dis_all_entry, dis_rec_entry]:
            if i.get() == '':
                empty = empty + 1
        if not empty:
            net = (float(quantity_entry.get()) * float(rate_entry.get())) + float(dis_all_entry.get()) - float(
                dis_rec_entry.get())
            net_entry.delete(0, tkinter.END)
            net_entry.insert(0, "{:.2f}".format(net))

    # function to calculate numeral value if a single numeral field other than net is left at last
    def single_empty_numeral(event):
        format_numerals(event, None)
        empty = 0
        for i in [quantity_entry, rate_entry, dis_all_entry, dis_rec_entry, net_entry]:
            if i.get() == '':
                empty = empty + 1
        if empty == 1:
            if quantity_entry.get() == '':
                qty = (float(net_entry.get()) - float(dis_all_entry.get()) + float(dis_rec_entry.get())) / float(
                    rate_entry.get())
                quantity_entry.delete(0, tkinter.END)
                quantity_entry.insert(0, "{:.3f}".format(qty))
            elif rate_entry.get() == '':
                r = (float(net_entry.get()) - float(dis_all_entry.get()) + float(dis_rec_entry.get())) / float(
                    quantity_entry.get())
                rate_entry.delete(0, tkinter.END)
                rate_entry.insert(0, "{:.2f}".format(r))
            elif dis_all_entry.get() == '':
                da = float(net_entry.get()) + float(dis_rec_entry.get()) - (
                        float(quantity_entry.get()) * float(rate_entry.get()))
                dis_all_entry.delete(0, tkinter.END)
                dis_all_entry.insert(0, "{:.2f}".format(da))
            elif dis_rec_entry.get() == '':
                dr = (float(quantity_entry.get()) * float(rate_entry.get())) + float(dis_all_entry.get()) - float(
                    net_entry.get())
                dis_rec_entry.delete(0, tkinter.END)
                dis_rec_entry.insert(0, "{:.2f}".format(dr))
            elif net_entry.get() == '':
                net = (float(quantity_entry.get()) * float(rate_entry.get())) + float(dis_all_entry.get()) - float(
                    dis_rec_entry.get())
                net_entry.delete(0, tkinter.END)
                net_entry.insert(0, "{:.2f}".format(net))
        elif empty > 1:
            messagebox.showwarning("UNKNOWN QUANTITY LIMIT EXCEEDED",
                                   "Please do not leave more than one among Quantity, Rate, Dis. Allowed, Dis. Received and Net Price as empty")
            if quantity_entry.get() == '':
                quantity_entry.focus_set()
            elif rate_entry.get() == '':
                rate_entry.focus_set()
            elif dis_all_entry.get() == '':
                dis_all_entry.focus_set()
            elif dis_rec_entry.get() == '':
                dis_rec_entry.focus_set()

    # function to execute on add OR done
    def add_or_done():

        capitalize_words(None, item_entry)
        category_auto_fill(None)
        for i in [category_entry, mode_entry, unit_entry]:
            capitalize_words(None, i)
        for i in [quantity_entry, rate_entry, dis_all_entry, dis_rec_entry]:
            format_numerals(None, i)
        net_price_if_possible(None)
        format_numerals(None, net_entry)
        single_empty_numeral(None)

        empty = 0
        for i in [date_picker, item_entry, category_entry, mode_entry, unit_entry, quantity_entry, rate_entry,
                  dis_all_entry, dis_rec_entry, net_entry]:
            if i.get() == '':
                empty = empty + 1

        if empty != 0:
            messagebox.showerror('EMPTY FIELDS NOT PERMITTED', 'Please do not leave any of the fields empty')
            for i in [date_picker, item_entry, category_entry, mode_entry, unit_entry, quantity_entry, rate_entry,
                      dis_all_entry, dis_rec_entry, net_entry]:
                if i.get() == '':
                    i.focus_set()
                    break
        else:
            db_connection = sqlite3.connect(os.path.join('FILES', 'HOME_ACCOUNTING', 'DATA', 'home_accounting.db'))
            db_cursor = db_connection.cursor()

            date = to_year_month_day(date_picker.get())
            item = item_entry.get()
            category = category_entry.get()
            mode = mode_entry.get()
            unit = unit_entry.get()
            quantity = float(quantity_entry.get())
            rate = float(rate_entry.get())
            da = float(dis_all_entry.get())
            dr = float(dis_rec_entry.get())
            net = float(net_entry.get())

            if button_add_done.cget('text') == 'ADD':
                db_cursor.execute("""INSERT INTO entries VALUES (?,?,?,?,?,?,?,?,?,?)""",
                                  (date, item, category, mode, unit, quantity, rate, da, dr, net))
                db_connection.commit()
                db_connection.close()
            elif button_add_done.cget('text') == 'DONE':
                row = int(tree.selection()[0])
                db_cursor.execute(
                    """UPDATE entries SET date=?, item=?, category=?, mode=?, unit=?, quantity=?, rate=?, da=?, dr=?, net=? WHERE rowid=""" + str(
                        row),
                    (date, item, category, mode, unit, quantity, rate, da, dr, net))
                db_connection.commit()
                db_connection.close()

            button_add_done.config(text='ADD')
            category_entry.config(state='normal')
            for i in [net_entry, dis_all_entry, dis_rec_entry, rate_entry, quantity_entry, category_entry, item_entry, unit_entry]:
                i.delete(0, tkinter.END)
            for i in [net_entry, dis_all_entry, dis_rec_entry, rate_entry]:
                i.insert(0, '0.00')
            quantity_entry.insert(0, '0.000')
            update_tree()
            item_entry.focus_set()

    # function to convert date to year/month/day format
    def to_year_month_day(d):
        return d[6:] + '/' + d[3:5] + '/' + d[:2]

    # function to convert date to day/month/year
    def to_day_month_year(d):
        return d[8:] + '/' + d[5:7] + '/' + d[:4]

    # function to update the tree whenever needed
    def update_tree():
        tree.delete(*tree.get_children())

        db_connection = sqlite3.connect(os.path.join('FILES', 'HOME_ACCOUNTING', 'DATA', 'home_accounting.db'))
        db_cursor = db_connection.cursor()

        num_of_entries = 0
        db_cursor.execute("SELECT COUNT(*) FROM entries")
        num_of_entries = db_cursor.fetchall()[0][0]

        total_net = 0
        db_cursor.execute("SELECT SUM(net) FROM entries")
        total_net = db_cursor.fetchall()[0][0]
        if total_net is None:
            total_net = 0

        db_cursor.execute("SELECT quantity FROM entries")
        quantities = db_cursor.fetchall()

        db_cursor.execute("SELECT rate FROM entries")
        rates = db_cursor.fetchall()

        total_gross = 0
        for i in range(num_of_entries):
            total_gross += (quantities[i][0] * rates[i][0])

        label_number_of_entries.config(text='No. of entries = ' + str(num_of_entries))
        label_total_gross.config(text='Total Gross = ' + "{:.2f}".format(total_gross))
        label_total_net.config(text='Total Net = ' + "{:.2f}".format(total_net))

        db_cursor.execute("SELECT * FROM entries")
        the_entries = db_cursor.fetchall()
        for i in range(num_of_entries):
            row = []
            date = to_day_month_year(the_entries[i][0])
            item = the_entries[i][1]
            category = the_entries[i][2]
            mode = the_entries[i][3]
            unit = the_entries[i][4]
            quantity = "{:.3f}".format(the_entries[i][5])
            rate = "{:.2f}".format(the_entries[i][6])
            da = "{:.2f}".format(the_entries[i][7])
            dr = "{:.2f}".format(the_entries[i][8])
            net = "{:.2f}".format(the_entries[i][9])
            for j in [date, item, category, mode, unit, quantity, rate, da, dr, net]:
                row.append(j)

            if i % 2 == 0:
                tree.insert(parent='', index='end', iid=i + 1, values=row)
            else:
                tree.insert(parent='', index='end', iid=i + 1, values=row, tags=('odd',))

        db_connection.close()

        check_tree_selection(None)

    # function to check if any selection is made in the tree and change state of the three buttons
    def check_tree_selection(event):
        if tree.selection():
            button_edit.config(state=tkinter.NORMAL)
            button_delete.config(state=tkinter.NORMAL)
            button_clear_selection.config(state=tkinter.NORMAL)
        else:
            button_edit.config(state=tkinter.DISABLED)
            button_delete.config(state=tkinter.DISABLED)
            button_clear_selection.config(state=tkinter.DISABLED)

    # function to be called on 'edit' button
    def edit_entry():
        row = int(tree.selection()[0])
        button_edit.config(state='disabled')
        button_delete.config(state='disabled')
        button_clear_selection.config(state='disabled')
        button_add_done.config(text='DONE')

        for i in [date_picker, item_entry, category_entry, mode_entry, unit_entry, quantity_entry, rate_entry,
                  dis_all_entry, dis_rec_entry, net_entry]:
            i.delete(0, tkinter.END)

        db_connection = sqlite3.connect(os.path.join('FILES', 'HOME_ACCOUNTING', 'DATA', 'home_accounting.db'))
        db_cursor = db_connection.cursor()

        db_cursor.execute("SELECT * FROM entries WHERE rowid=" + str(row))
        data_to_edit = db_cursor.fetchall()
        date_picker.insert(0, to_day_month_year(data_to_edit[0][0]))
        item_entry.insert(0, data_to_edit[0][1])
        category_entry.insert(0, data_to_edit[0][2])
        mode_entry.insert(0, data_to_edit[0][3])
        unit_entry.insert(0, data_to_edit[0][4])
        quantity_entry.insert(0, "{:.3f}".format(data_to_edit[0][5]))
        rate_entry.insert(0, "{:.2f}".format(data_to_edit[0][6]))
        dis_all_entry.insert(0, "{:.2f}".format(data_to_edit[0][7]))
        dis_rec_entry.insert(0, "{:.2f}".format(data_to_edit[0][8]))
        net_entry.insert(0, "{:.2f}".format(data_to_edit[0][9]))

        date_picker.focus_set()

    # function for clearing the selection made in the tree
    def clear_selection():
        update_tree()

    # theme setting of ttk widgets
    style = ttk.Style()
    style.theme_use("clam")  # default is vista
    style.configure("Treeview", background='white', fieldbackground='white', rowheight=25,
                    font='TkDefaultFont 9 italic')
    style.configure("Treeview.Heading", font='TkDefaultFont 10 bold')
    style.map("Treeview", background=[('selected', 'RoyalBlue3')])

    # calling the function to initially check the existence of files and creating it if not existing
    file_initialisation()

    date_picker = tkcalendar.DateEntry(root, date_pattern='dd/mm/yyyy')
    date_picker.place(relx=0.02, rely=0.0256, relwidth=0.15)
    date_picker.focus_set()
    date_picker.bind("<Return>", next_widget_on_return)
    date_picker.bind("<FocusOut>", date_only)

    label_item = tkinter.Label(root, text='Item', font='TkDefaultFont 10 italic')
    label_item.place(relx=0.02, rely=0.0256 * 4 - 0.0065)
    item_entry = autocomplete.AutocompleteEntry(root, completevalues=[])
    item_entry.place(relx=0.02, rely=0.0256 * 5, relwidth=0.15)
    item_entry.bind("<Return>", next_widget_on_return)
    item_entry.bind("<FocusOut>", category_auto_fill)

    label_category = tkinter.Label(root, text='Category', font='TkDefaultFont 10 italic')
    label_category.place(relx=0.02, rely=0.0256 * 8 - 0.0065)
    category_entry = autocomplete.AutocompleteEntry(root, completevalues=[])
    category_entry.place(relx=0.02, rely=0.0256 * 9, relwidth=0.15)
    category_entry.bind("<Return>", next_widget_on_return)
    category_entry.bind("<FocusOut>", lambda event, widget=None: capitalize_words(event, widget))

    label_mode = tkinter.Label(root, text='Mode Of Payment', font='TkDefaultFont 10 italic')
    label_mode.place(relx=0.02, rely=0.0256 * 12 - 0.0065)
    mode_entry = autocomplete.AutocompleteEntry(root, completevalues=[])
    mode_entry.place(relx=0.02, rely=0.0256 * 13, relwidth=0.15)
    mode_entry.bind("<Return>", next_widget_on_return)
    mode_entry.bind("<FocusOut>", lambda event, widget=None: capitalize_words(event, widget))

    label_unit = tkinter.Label(root, text='Unit (Quantity Description)', font='TkDefaultFont 10 italic')
    label_unit.place(relx=0.02, rely=0.0256 * 16 - 0.0065)
    unit_entry = autocomplete.AutocompleteEntry(root, completevalues=[])
    unit_entry.place(relx=0.02, rely=0.0256 * 17, relwidth=0.15)
    unit_entry.bind("<Return>", next_widget_on_return)
    unit_entry.bind("<FocusOut>", lambda event, widget=None: capitalize_words(event, widget))

    label_quantity = tkinter.Label(root, text='Quantity', font='TkDefaultFont 10 italic')
    label_quantity.place(relx=0.02, rely=0.0256 * 20 - 0.0065)
    quantity_entry = tkinter.Entry(root)
    quantity_entry.place(relx=0.02, rely=0.0256 * 21, relwidth=0.15)
    quantity_entry.config(validate='all', validatecommand=(root.register(only_numeric), '%P'))
    quantity_entry.insert(0, '0.000')
    quantity_entry.bind("<Return>", next_widget_on_return)
    quantity_entry.bind("<FocusOut>", lambda event, widget=None: format_numerals(event, widget))

    label_rate = tkinter.Label(root, text='Rate', font='TkDefaultFont 10 italic')
    label_rate.place(relx=0.02, rely=0.0256 * 24 - 0.0065)
    rate_entry = tkinter.Entry(root)
    rate_entry.place(relx=0.02, rely=0.0256 * 25, relwidth=0.15)
    rate_entry.config(validate='all', validatecommand=(root.register(only_numeric), '%P'))
    rate_entry.insert(0, '0.00')
    rate_entry.bind("<Return>", next_widget_on_return)
    rate_entry.bind("<FocusOut>", lambda event, widget=None: format_numerals(event, widget))

    label_dis_all = tkinter.Label(root, text='Dis. Allowed', font='TkDefaultFont 10 italic')
    label_dis_all.place(relx=0.02, rely=0.0256 * 28 - 0.0065)
    dis_all_entry = tkinter.Entry(root)
    dis_all_entry.place(relx=0.02, rely=0.0256 * 29, relwidth=0.07)
    dis_all_entry.config(validate='all', validatecommand=(root.register(only_numeric), '%P'))
    dis_all_entry.insert(0, '0.00')
    dis_all_entry.bind("<Return>", next_widget_on_return)
    dis_all_entry.bind("<FocusOut>", lambda event, widget=None: format_numerals(event, widget))

    label_dis_rec = tkinter.Label(root, text='Dis. Received', font='TkDefaultFont 10 italic')
    label_dis_rec.place(relx=0.02 + 0.07 + 0.01, rely=0.0256 * 28 - 0.0065)
    dis_rec_entry = tkinter.Entry(root)
    dis_rec_entry.place(relx=0.02 + 0.07 + 0.01, rely=0.0256 * 29, relwidth=0.07)
    dis_rec_entry.config(validate='all', validatecommand=(root.register(only_numeric), '%P'))
    dis_rec_entry.insert(0, '0.00')
    dis_rec_entry.bind("<Return>", next_widget_on_return)
    dis_rec_entry.bind("<FocusOut>", net_price_if_possible)

    label_net = tkinter.Label(root, text='Net Price', font='TkDefaultFont 10 italic')
    label_net.place(relx=0.02, rely=0.0256 * 32 - 0.0065)
    net_entry = tkinter.Entry(root)
    net_entry.place(relx=0.02, rely=0.0256 * 33, relwidth=0.15)
    net_entry.config(validate='all', validatecommand=(root.register(only_numeric), '%P'))
    net_entry.insert(0, '0.00')
    net_entry.bind("<Return>", next_widget_on_return)
    net_entry.bind("<FocusOut>", single_empty_numeral)

    button_add_done = tkinter.Button(root, text='ADD', relief='groove', font='TkDefaultFont 11 bold italic',
                                     command=add_or_done)
    button_add_done.place(relx=0.045, rely=0.0256 * 36, relheight=0.0256 * 2, relwidth=0.10)
    button_add_done.bind("<Return>", lambda event=None: button_add_done.invoke())

    button_save_exit = tkinter.Button(root, text='SAVE and EXIT', relief='groove', font='TkDefaultFont 11 bold italic')
    button_save_exit.place(relwidth=0.15, relheight=0.0256 * 3, relx=0.425, rely=0.870)
    button_save_exit.bind("<Return>", lambda event=None: button_save_exit.invoke())

    button_no_save_exit = tkinter.Button(root, text='EXIT without SAVING', relief='groove',
                                         font='TkDefaultFont 11 bold italic')
    button_no_save_exit.place(relwidth=0.15, relheight=0.0256 * 3, relx=0.615, rely=0.870)
    button_no_save_exit.bind("<Return>", lambda event=None: button_no_save_exit.invoke())

    button_edit = tkinter.Button(root, text='Edit', state=tkinter.DISABLED, relief='groove', command=edit_entry)
    button_edit.place(relwidth=0.07, relheight=0.0256 * 2, rely=0.79, relx=0.47)
    button_edit.bind("<Return>", lambda event=None: button_edit.invoke())

    button_delete = tkinter.Button(root, text='Delete', state=tkinter.DISABLED, relief='groove')
    button_delete.place(relwidth=0.07, relheight=0.0256 * 2, rely=0.79, relx=0.56)
    button_delete.bind("<Return>", lambda event=None: button_delete.invoke())

    button_clear_selection = tkinter.Button(root, text='Clear Selection', state=tkinter.DISABLED, relief='groove', command=clear_selection)
    button_clear_selection.place(relwidth=0.07, relheight=0.0256 * 2, rely=0.79, relx=0.65)
    button_clear_selection.bind("<Return>", lambda event=None: button_clear_selection.invoke())

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
    tree.bind('<FocusIn>', check_tree_selection)
    tree.bind('<ButtonRelease-1>', check_tree_selection)
    tree.bind('<KeyRelease>', check_tree_selection)

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

    # calling function to initially set the auto completion values for different fields
    for i in [(item_entry, 'item'), (category_entry, 'category'), (mode_entry, 'mode'), (unit_entry, 'unit')]:
        set_auto_completion(i)

    root.mainloop()
