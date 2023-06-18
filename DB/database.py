import sqlite3


# функция регистрации нового пользователя
def register_user(id: int, bilet: str = "None") -> None:
    try:
        conn = sqlite3.connect("DB/Users.db")
        cur = conn.cursor()
        cur.execute("SELECT id FROM User WHERE id = ?", (id,))
        data = cur.fetchone()
        if data is None:
            cur.execute(
                "INSERT INTO User(id, bilet) VALUES(?, ?);",
                (
                    id,
                    bilet,
                ),
            )
            conn.commit()

        cur.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)

    finally:
        if conn:
            conn.close()


# функция обновления информации о пользователи
def update_user_data(id: int, bilet: str) -> None:
    try:
        conn = sqlite3.connect("DB/Users.db")
        cur = conn.cursor()
        cur.execute(
            "UPDATE User SET bilet = ? where id = ?",
            (
                bilet,
                id,
            ),
        )
        conn.commit()
        cur.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)

    finally:
        if conn:
            conn.close()


# получение билета по айди пользователя
def get_bilet(id: int) -> str:
    try:
        conn = sqlite3.connect("DB/Users.db")
        cur = conn.cursor()
        cur.execute("SELECT bilet FROM User WHERE id = ?", (id,))
        data = cur.fetchone()[0]
        cur.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)

    finally:
        if conn:
            conn.close()
            return data
