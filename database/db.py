import sqlite3


class Database:
    def __init__(self, db_file):
        self.con = sqlite3.connect(db_file)
        self.cur = self.con.cursor()

    # ЗАПРОСЫ БД, КОТОРЫЕ СВЯЗАНЫ С ПОЛЬЗОВАТЕЛЯМИ
    # Нахождение пользователя по id
    def user_exists(self, user_id):
        with self.con:
            result = self.cur.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchmany(1)
            return bool(len(result))

    # Добавление пользователя
    def add_user(self, user_id, tag_name, full_name):
        with self.con:
            return self.cur.execute(
                f"INSERT INTO users (id, tag_name, full_name, isActive) VALUES ({user_id}, '{tag_name}', '{full_name}', 1)")

    # Установка активности пользователя
    def set_active(self, user_id, isActive):
        with self.con:
            return self.cur.execute("UPDATE users SET isActive = ? WHERE id = ?", (isActive, user_id,))

    # Закрепление номера заказа
    def set_order(self, user_id, order_number):
        with self.con:
            return self.cur.execute("UPDATE users SET order_number = ? WHERE id = ?", (order_number, user_id,))

    # Закрепление номера заказа
    def get_order(self, user_id):
        with self.con:
            return self.cur.execute("SELECT order_number FROM users where id = ?", (user_id,)).fetchmany(1)

    # Получение пользователей
    def get_users(self):
        with self.con:
            return self.cur.execute("SELECT id, tag_name, full_name, isActive FROM users").fetchall()

    # Создание заказа
    def add_order(self, id_order, perf_id, order_summ, materials_summ, garantiy):
        with self.con:
            return self.cur.execute(
                f"INSERT INTO orders (id, perf_id, order_summ, materials_summ, garantiy) VALUES ({id_order}, {perf_id}, {order_summ}, {materials_summ}, {garantiy})")

    # Нахождение заказа
    def order_exists(self, order_id):
        with self.con:
            result = self.cur.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchmany(1)
            return bool(len(result))

    # Получение заказа
    def get_orders(self, perf_id):
        with self.con:
            return self.cur.execute("SELECT id, perf_id FROM orders where perf_id = ?", (perf_id,)).fetchall()
