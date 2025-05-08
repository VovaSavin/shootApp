import psycopg2

CONNECT_DATA = {
    'NAME': 'hows',
    'USER': 'postgres',
    'PASSWORD': '123456',
    'HOST': 'localhost',
    'PORT': '5432',
}


class DBWorker:
    """
    Підключення до Postgresql
    """

    def __init__(self, c_data: dict):

        self.host = c_data["HOST"]
        self.name = c_data["NAME"]
        self.user = c_data["USER"]
        self.password = c_data["PASSWORD"]
        self.port = c_data["PORT"]
        self.connect = None
        self.check = False
        self.error = None
        self.check_connect_to_db()

    def check_connect_to_db(self, ):
        """
        Перевірка підключення до БД
        :return:
        """
        try:
            self.connect = psycopg2.connect(
                host=self.host,
                database=self.name,
                user=self.user,
                password=self.password,
                port=self.port
            )
            cursor = self.connect.cursor()
            cursor.execute(
                "SELECT version();"
            )
            cursor.fetchone()
            cursor.close()
            self.check = True
        except psycopg2.Error as er:
            self.error = f"WOW!!! We have exeption: {er}"
            print(self.error)
        finally:
            # Забезпечуємо закриття з'єднання, навіть якщо сталася помилка
            if self.connect:
                self.connect.close()

    def get_columns(self, ):
        """
        Отримує список для колонок в таблиці
        :return:
        """
        pass

    def get_data(self, tb_name: str, fields: tuple | list) -> list[dict] | None:
        """
        Вибирає дані з таблиці.

        :param tb_name: Назва таблиці.
        :param fields: Список полів, які треба вивести.
        :return:
        """
        if self.check:
            str_fields = ", ".join(fields)
            with psycopg2.connect(
                    host=self.host,
                    database=self.name,
                    user=self.user,
                    password=self.password,
                    port=self.port
            ) as connect:
                with connect.cursor() as cr:
                    cr.execute(
                        f"""
                        SELECT {str_fields}
                        FROM public."{tb_name}";
                        """
                    )
                    rows = cr.fetchall()
                    col_names = [col[0] for col in cr.description]
                    data = [dict(zip(col_names, row)) for row in rows]
                    return data
        else:
            print(self.error)
            return None


def connector() -> DBWorker:
    """
    Повертає об'єкт для підключення до БД
    :return:
    """
    conn = DBWorker(
        CONNECT_DATA
    )
    return conn


# c = DBWorker(
#     {
#         'NAME': 'hows',
#         'USER': 'postgres',
#         'PASSWORD': '123456',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# )
#
# c = connector()
# print(
#     c.get_data(
#         "hw_listheadtable",
#         ("id", "names",)
#     )
# )
