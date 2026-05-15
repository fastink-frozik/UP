import sqlite3
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox as mb

id_tekushego_polzovatelya = None
log = 2
conn = sqlite3.connect('magaz.db')
cursor = conn.cursor()
root = Tk()
root.geometry("300x300")
root.title("Авторизация")
cursor.execute("select vid from user")
roli = cursor.fetchall()


def save():
    conn = sqlite3.connect('magaz.db')
    cursor = conn.cursor()
    log = entrylogin.get()
    password = entrypass.get()
    vid = 1
    cursor.execute("SELECT user_id FROM user WHERE log = ?", (log,))
    if log == "":
        mb.showerror("Ошибка",
                     "Заполните все поля")
    elif cursor.fetchone():
        mb.showerror("Ошибка",
                     "Данный пользователь уже зарегистрирован")
    else:
        cursor.execute('INSERT INTO user (log, password, vid) VALUES (?, ?, ?)', (log, password, vid))
        conn.commit()
        conn.close()
        reg.destroy()


def izmenit_status(tree):
    vybrannoe = tree.selection()
    if not vybrannoe:
        mb.showwarning("Внимание", "Выберите заказ")
        return

    id_polzovatelya = tree.item(vybrannoe[0])['values'][0]
    okno_roli = tk.Toplevel()
    okno_roli.title("Изменение статуса")
    okno_roli.geometry("250x150")
    tk.Label(okno_roli, text="Новый статус:").pack(pady=10)
    peremennaya_roli = tk.StringVar(value="Статус")
    spisok_rolej = ttk.Combobox(okno_roli, textvariable=peremennaya_roli, values=["ожидание", "отказ", "принятие"], state="readonly")
    spisok_rolej.pack(pady=10)

    def sohranit_status():
        novaya_rol = peremennaya_roli.get()
        conn = sqlite3.connect('magaz.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE list_order SET status = ? WHERE id_order = ?", (novaya_rol, id_polzovatelya))
        conn.commit()
        conn.close()
        okno_roli.destroy()
        obnovit_order(tree)
    tk.Button(okno_roli, text="Сохранить", command=sohranit_status).pack(pady=10)


def obnovit_order(tree):
    for element in tree.get_children():
        tree.delete(element)
    conn = sqlite3.connect('magaz.db')
    cursor = conn.cursor()
    for znacheniya in cursor.execute("SELECT * FROM order_view"):
        tree.insert("", END, values=znacheniya)
    conn.close()


def izmenit_roli(tree):
    vybrannoe = tree.selection()
    if not vybrannoe:
        mb.showwarning("Внимание", "Выберите пользователя")
        return
    id_polzovatelya = tree.item(vybrannoe[0])['values'][0]
    okno_roli = tk.Toplevel()
    okno_roli.title("Изменение Роли")
    okno_roli.geometry("250x150")
    tk.Label(okno_roli, text="Новая роль:").pack(pady=10)
    peremennaya_roli = tk.StringVar(value="Роль")
    spisok_rolej = ttk.Combobox(okno_roli, textvariable=peremennaya_roli, values=[1, 2, 3], state="readonly")
    spisok_rolej.pack(pady=10)

    def sohranit_roli():
        novaya_rol = peremennaya_roli.get()
        conn = sqlite3.connect('magaz.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE user SET vid = ? WHERE user_id = ?", (novaya_rol, id_polzovatelya))
        conn.commit()
        conn.close()
        okno_roli.destroy()
        obnovit_roli(tree)
    tk.Button(okno_roli, text="Сохранить", command=sohranit_roli).pack(pady=10)


def delit_user(tree):
    selected = tree.selection()
    if not selected:
        mb.showwarning("Предупреждение", "Сначала выберите пользователя для удаления")
        return

    if not mb.askyesno("Подтверждение", "Вы уверены, что хотите удалить выбраного пользователя?"):
        return

    user_id = tree.item(selected[0])['values'][0]
    user_name = tree.item(selected[0])['values'][1]


    conn = sqlite3.connect('magaz.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM user WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

    mb.showinfo("Успех", f"Аккаунт под логином '{user_name}' удалён. Спасибо за вашу работу")
    obnovit_roli(tree)


def obnovit_roli(tree):
    for element in tree.get_children():
        tree.delete(element)
    conn = sqlite3.connect('magaz.db')
    cursor = conn.cursor()
    for znacheniya in cursor.execute("SELECT * FROM user"):
        tree.insert("", END, values=znacheniya)
    conn.close()


def regist():
    global entrylogin, entrypass, reg
    reg = Tk()
    reg.title("Регистрация")
    reg.geometry("300x150")

    frame = ttk.Frame(reg, padding="20")
    frame.pack(fill=tk.BOTH, expand=True)

    ttk.Label(frame, text="Логин").grid(row=0, column=0, sticky=tk.W, pady=5)
    entrylogin = tk.Entry(frame, width=30)
    entrylogin.grid(row=0, column=1, pady=5, padx=(10, 0))

    ttk.Label(frame, text="Пароль").grid(row=1, column=0, sticky=tk.W, pady=5)
    entrypass = tk.Entry(frame, show="*", width=30)
    entrypass.grid(row=1, column=1, pady=5, padx=(10, 0))

    btn_reg = ttk.Button(frame, text="Регистрация", command=save)
    btn_reg.grid(row=3, column=0, columnspan=2, pady=20)
    reg.mainloop()


def orderes():
    orderes_window = tk.Tk()
    orderes_window.title("Магазин игр Доски & кубики")
    orderes_window.geometry("250x400")
    frame = ttk.Frame(orderes_window, padding="20")
    frame.pack(fill=tk.BOTH, expand=True)
    conn = sqlite3.connect('magaz.db')
    cursor = conn.cursor()
    columns = ('id_order', 'DATA', 'status', 'user_id')
    tree = ttk.Treeview(frame, columns=columns, show="headings")
    tree.place(x=0, y=5)
    tree.heading("id_order", text="Айди заказа")
    tree.heading("DATA", text="Дата")
    tree.heading("status", text="Статус")
    tree.heading("user_id", text="Логин")

    tree.column("#1", stretch=NO, width=50)
    tree.column("#2", stretch=NO, width=50)
    tree.column("#3", stretch=NO, width=60)
    tree.column("#4", stretch=NO, width=50)
    for valuse in cursor.execute("""SELECT * FROM order_view """):
        tree.insert("", END, values=valuse)
    scrollbar = ttk.Scrollbar(frame, orient=VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.place(x=213, y=15)
    tk.Button(frame, text="Изменить статуса", command=lambda: izmenit_status(tree)).place(x=0, y=240, height=40, width=190)


def add_igri(tree):
    add_window = Toplevel()
    add_window.title("Добавить игру")
    add_window.geometry("400x400")

    Label(add_window, text="Название игры:").pack(pady=5)
    name_entry = Entry(add_window, width=40)
    name_entry.pack()

    Label(add_window, text="Описание:").pack(pady=5)
    desc_text = Text(add_window, height=5, width=40)
    desc_text.pack()

    Label(add_window, text="Оценка:").pack(pady=5)
    rating_entry = Entry(add_window, width=40)
    rating_entry.pack()

    Label(add_window, text="Цена:").pack(pady=5)
    price_entry = Entry(add_window, width=40)
    price_entry.pack()

    def save_game():
        name = name_entry.get().strip()
        opisanie = desc_text.get("1.0", tk.END).strip()
        ocenka = rating_entry.get().strip()
        price = price_entry.get().strip()

        # Простая валидация
        if not name:
            mb.showerror("Ошибка", "Название игры обязательно")
            return

        try:
            ocenka_val = float(ocenka) if ocenka else None
            price_val = float(price) if price else None
        except ValueError:
            mb.showerror("Ошибка", "Оценка и цена должны быть числами")
            return

        conn = sqlite3.connect('magaz.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Igri (Name, opisanie, ocenka, price)
            VALUES (?, ?, ?, ?)
        ''', (name, opisanie, ocenka_val, price_val))
        conn.commit()
        conn.close()

        mb.showinfo("Успех", f"Игра '{name}' добавлена")
        add_window.destroy()
        refresh_tree(tree)

    Button(add_window, text="Сохранить", command=save_game).pack(pady=20)


def edit_igri(tree):
    selected = tree.selection()
    if not selected:
        mb.showwarning("Предупреждение", "Сначала выберите игру для редактирования")
        return

    game_id = tree.item(selected[0])['values'][0]

    conn = sqlite3.connect('magaz.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Igri WHERE id = ?", (game_id,))
    game = cursor.fetchone()

    if not game:
        mb.showerror("Ошибка", "Игра не найдена")
        return

    edit_window = tk.Toplevel()
    edit_window.title("Редактировать игру")
    edit_window.geometry("400x400")

    Label(edit_window, text="Название игры:").pack(pady=5)
    name_entry = Entry(edit_window, width=40)
    name_entry.insert('0', game[1])
    name_entry.pack()

    Label(edit_window, text="Описание:").pack(pady=5)
    desc_text = Text(edit_window, height=5, width=40)
    desc_text.insert('1.0', game[2])
    desc_text.pack()

    Label(edit_window, text="Оценка (1-100):").pack(pady=5)
    rating_entry = Entry(edit_window, width=40)
    rating_entry.insert(0, str(game[3]))
    rating_entry.pack()

    Label(edit_window, text="Цена:").pack(pady=5)
    price_entry = Entry(edit_window, width=40)
    price_entry.insert(0, str(game[4]))
    price_entry.pack()
    conn.close()

    def update_game():
        name = name_entry.get().strip()
        opisanie = desc_text.get("1.0", tk.END).strip()
        ocenka = rating_entry.get().strip()
        price = price_entry.get().strip()

        if not name:
            mb.showerror("Ошибка", "Название игры обязательно")
            return

        try:
            ocenka_val = float(ocenka) if ocenka else None
            price_val = float(price) if price else None
        except ValueError:
            mb.showerror("Ошибка", "Оценка и цена должны быть числами")
            return

        conn = sqlite3.connect('magaz.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE Igri 
            SET Name = ?, opisanie = ?, ocenka = ?, price = ?
            WHERE id = ?
        ''', (name, opisanie, ocenka_val, price_val, game_id))
        conn.commit()
        conn.close()

        mb.showinfo("Успех", f"Игра '{name}' обновлена")
        edit_window.destroy()
        refresh_tree(tree)

    Button(edit_window, text="Обновить", command=update_game).pack(pady=20)


def delit_igri(tree):
    selected = tree.selection()
    if not selected:
        mb.showwarning("Предупреждение", "Сначала выберите игру для удаления")
        return

    if not mb.askyesno("Подтверждение", "Вы уверены, что хотите удалить выбранную игру?"):
        return

    game_id = tree.item(selected[0])['values'][0]
    game_name = tree.item(selected[0])['values'][1]


    conn = sqlite3.connect('magaz.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Igri WHERE id = ?", (game_id,))
    conn.commit()
    conn.close()

    mb.showinfo("Успех", f"Игра '{game_name}' удалена")
    refresh_tree(tree)


def refresh_tree(tree):
    for item in tree.get_children():
        tree.delete(item)
    conn = sqlite3.connect('magaz.db')
    cursor = conn.cursor()
    for row in cursor.execute("SELECT * FROM Igri"):
        tree.insert("", tk.END, values=row)
    conn.close()


def corzina():
    global user_id

    corzin_window = tk.Toplevel()
    corzin_window.title("Корзина")
    corzin_window.geometry("600x400")
    frame = ttk.Frame(corzin_window, padding="20")
    frame.pack(fill=tk.BOTH, expand=True)

    conn = sqlite3.connect('magaz.db')
    cursor = conn.cursor()


    cursor.execute("""
        SELECT id_order FROM list_order 
        WHERE user_id = ? AND status = 'ожидание'
    """, (user_id,))
    existing_order = cursor.fetchone()

    if existing_order is None:
        from datetime import datetime
        current_date = datetime.now().strftime("%Y%m%d")

        cursor.execute('''
            INSERT INTO list_order (DATA, status, user_id) 
            VALUES (?, ?, ?)
        ''', (current_date, "ожидание", user_id))
        conn.commit()

        cursor.execute("SELECT last_insert_rowid()")
        order_id = cursor.fetchone()[0]
    else:
        order_id = existing_order[0]

    columns = ('id', 'Name', 'price')
    tree = ttk.Treeview(frame, columns=columns, show="headings")
    tree.pack(fill=tk.BOTH, expand=True)

    tree.heading("id", text="ID игры")
    tree.heading("Name", text="Наименование")
    tree.heading("price", text="Цена")

    tree.column("#1", width=50)
    tree.column("#2", width=300)
    tree.column("#3", width=100)

    cursor.execute("""
        SELECT Igri.id, Igri.Name, Igri.price 
        FROM korzina 
        JOIN Igri ON korzina.id = Igri.id 
        WHERE korzina.id_order = ?
    """, (order_id,))

    games = cursor.fetchall()
    total_price = 0

    for game in games:
        tree.insert("", tk.END, values=game)
        if game[2]:
            total_price += game[2]

    total_label = tk.Label(frame, text=f"Общая сумма: {total_price} руб.", font=("Arial", 12, "bold"))
    total_label.pack(pady=10)
    conn.close()

    def remove_from_cart():
        selected = tree.selection()
        if not selected:
            mb.showwarning("Внимание", "Выберите игру для удаления")
            return

        game_id = tree.item(selected[0])['values'][0]
        conn = sqlite3.connect('magaz.db')
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM korzina 
            WHERE id_order = ? AND id = ?
        """, (order_id, game_id))
        conn.commit()

        mb.showinfo("Удалено", "Игра удалена из корзины")
        conn.close()
        corzin_window.destroy()
        corzina()

    remove_btn = tk.Button(frame, text="Удалить из корзины", command=remove_from_cart, bg="red", fg="white")
    remove_btn.pack(pady=5)

    conn.close()


def add_to_cart(tree):
    selected = tree.selection()
    if not selected:
        mb.showwarning("Внимание", "Выберите игру для добавления в корзину")
        return

    game_name = tree.item(selected[0])['values'][0]

    conn = sqlite3.connect('magaz.db')
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM Igri WHERE Name = ?", (game_name,))
    game = cursor.fetchone()

    if not game:
        mb.showerror("Ошибка", "Игра не найдена")
        conn.close()
        return

    game_id = game[0]

    cursor.execute("""
        SELECT id_order FROM list_order 
        WHERE user_id = ? AND status = 'ожидание'
    """, (user_id,))
    existing_order = cursor.fetchone()

    if existing_order is None:
        from datetime import datetime
        current_date = datetime.now().strftime("%Y%m%d")
        cursor.execute('''
            INSERT INTO list_order (DATA, status, user_id) 
            VALUES (?, ?, ?)
        ''', (current_date, "ожидание", user_id))
        conn.commit()
        cursor.execute("SELECT last_insert_rowid()")
        order_id = cursor.fetchone()[0]
    else:
        order_id = existing_order[0]

    cursor.execute("""
        SELECT * FROM korzina 
        WHERE id_order = ? AND id = ?
    """, (order_id, game_id))

    cursor.execute("""
        INSERT INTO korzina (id_order, id) 
        VALUES (?, ?)
    """, (order_id, game_id))
    conn.commit()
    conn.close()

    mb.showinfo("Успех", f"Игра '{game_name}' добавлена в корзину")


def avtoriz():
    global ent, ent1, user_id
    if ent.get() == "" or ent1.get() == "":
        mb.showerror("Ошибка",
                     "Заполните все поля")
    else:
        try:
            login = ent1.get()
            password = ent.get()

            conn = sqlite3.connect('magaz.db')
            cursor = conn.cursor()

            cursor.execute("""SELECT user_id, log, vid, password FROM user WHERE log = ? AND password = ?""",
                           (login, password))

            user_id, log, vid, pas = cursor.fetchone()
            conn.close()
            main_widndow = tk.Tk()
            main_widndow.title("Магазин игр Доски & кубики")
            main_widndow.geometry("800x450")
            frame = ttk.Frame(main_widndow, padding="20")
            frame.pack(fill=tk.BOTH, expand=True)
            if vid == 3:
                user_info = tk.Label(main_widndow, text=f"День добрый, администратор", font=("Arial", 12), fg="gray")
                user_info.place(x=350, y=20)
                conn = sqlite3.connect('magaz.db')
                cursor = conn.cursor()
                columns = ('id', 'log', 'vid', 'password')
                tree = ttk.Treeview(frame, columns=columns, show="headings")
                tree.place(x=30, y=50)
                tree.heading("id", text="Айди пользователя")
                tree.heading("log", text="Логин")
                tree.heading("password", text="Роли")
                tree.heading("vid", text="Пороли")
                tree.column("#1", stretch=NO, width=30)
                tree.column("#2", stretch=NO, width=100)
                tree.column("#3", stretch=NO, width=100)
                tree.column("#4", stretch=NO, width=50)

                for valuse in cursor.execute("""SELECT * FROM user """):
                    tree.insert("", END, values=valuse)
                scrollbar = ttk.Scrollbar(frame, orient=VERTICAL, command=tree.yview)
                tree.configure(yscroll=scrollbar.set)
                scrollbar.place(x=314, y=45)
                rolis = tk.Button(frame, text="Изменние ролей", command=lambda: izmenit_roli(tree), bg="darkgrey")
                rolis.place(x=30, y=350, height=40, width=200)
                rolis = tk.Button(frame, text="Удаление аккаунта", command=lambda: delit_user(tree), bg="darkgrey")
                rolis.place(x=225, y=350, height=40, width=200)
                user_info = tk.Label(main_widndow, text=f"Напоминание про роли:", font=("Arial", 16))
                user_info.place(x=350, y=50)
                user_info = tk.Label(main_widndow, text=f"1 - это пользователь", font=("Arial", 16), fg="red")
                user_info.place(x=360, y=110)
                user_info = tk.Label(main_widndow, text=f"2 - это сотрудник", font=("Arial", 16), fg="DarkGoldenrod1")
                user_info.place(x=360, y=160)
                user_info = tk.Label(main_widndow, text=f"3 - это сам бог, администратор", font=("Arial", 16), fg="green")
                user_info.place(x=360, y=200)
            elif vid == 2:
                user_info = tk.Label(main_widndow, text=f"Время работать: {log}", font=("Arial", 12), fg="gray")
                user_info.place(x=350, y=20)
                conn = sqlite3.connect('magaz.db')
                cursor = conn.cursor()
                columns = ('id', 'Name', 'opisanie', 'ocenka', 'price')
                tree = ttk.Treeview(frame, columns=columns, show="headings")
                tree.place(x=30, y=50)
                tree.heading("id", text="Айди")
                tree.heading("Name", text="Наименование")
                tree.heading("opisanie", text="Описание")
                tree.heading("ocenka", text="Оценка")
                tree.heading("price", text="Цена")

                tree.column("#1", stretch=NO, width=35)
                tree.column("#2", stretch=NO, width=160)
                tree.column("#3", stretch=NO, width=425)
                tree.column("#4", stretch=NO, width=50)
                tree.column("#5", stretch=NO, width=40)

                for valuse in cursor.execute("""SELECT * FROM Igri """):
                    tree.insert("", END, values=valuse)
                scrollbar = ttk.Scrollbar(frame, orient=VERTICAL, command=tree.yview)
                tree.configure(yscroll=scrollbar.set)
                scrollbar.place(x=745, y=45)
                orders = tk.Button(frame, text="Заказы", command=orderes, bg="darkgrey")
                orders.place(x=300, y=360, height=40, width=200)
                orders = tk.Button(frame, text="Удалить", command=lambda: delit_igri(tree), bg="darkgrey")
                orders.place(x=100, y=320, height=40, width=200)
                orders = tk.Button(frame, text="Изменить", command=lambda: edit_igri(tree), bg="darkgrey")
                orders.place(x=300, y=320, height=40, width=200)
                orders = tk.Button(frame, text="Добавить", command=lambda: add_igri(tree), bg="darkgrey")
                orders.place(x=500, y=320, height=40, width=200)
            elif vid == 1:
                user_info = tk.Label(main_widndow, text=f"Вы вошли как: {log}", font=("Arial", 12), fg="gray")
                user_info.place(x=350, y=20)
                conn = sqlite3.connect('magaz.db')
                cursor = conn.cursor()
                columns = ('Name', 'opisanie', 'price')
                tree = ttk.Treeview(frame, columns=columns, show="headings")
                tree.place(x=30, y=50)
                tree.heading("Name", text="Наименование")
                tree.heading("price", text="Цена")
                tree.heading("opisanie", text="Описание")

                tree.column("#1", stretch=NO, width=150)
                tree.column("#2", stretch=NO, width=425)
                tree.column("#3", stretch=NO, width=35)

                for valuse in cursor.execute("""SELECT Name, opisanie, price FROM Igri """):
                    tree.insert("", END, values=valuse)
                corzin = tk.Button(frame, text="Корзина", command=corzina, bg="darkgrey")
                corzin.place(x=300, y=350, height=40, width=200)
                add_to_cart_btn = tk.Button(frame, text="Добавить в корзину",
                                            command=lambda: add_to_cart(tree),
                                            bg="darkgrey")
                add_to_cart_btn.place(x=500, y=350, height=40, width=200)
            main_widndow.mainloop()
        except TypeError:
            mb.showerror('Ошибка',
                         'Возможно вы не авторизованны или вы не правильно ввели свой логин/пароль')

button = ttk.Button(text="Регистрация", command=regist)
button.place(x=30, y=200)
button = ttk.Button(text="Авторизация", command=avtoriz)
button.place(x=180, y=200)
leb = ttk.Label(text='Доски & кубики', font='Arial 14')
leb.place(x=75, y=40)
ent = ttk.Entry(show="*", width=30)
ent.place(x=70, y=155)
ent1 = ttk.Entry(width=30)
ent1.place(x=70, y=130)
root.mainloop()
