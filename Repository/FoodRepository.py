from Manager.DBManager import DBManager


class FoodRepository:
    def __init__(self):
        self.db_manager = DBManager()

    def save(self, food):
        connection = self.db_manager.connect()
        try:
            with connection.cursor() as cursor:
                # Create a new record
                # if the food doesn't exist in the db
                if food.id == 0:
                    sql = "INSERT INTO food (name, quantity, measuring_units) VALUES (%s, %s, %s)"
                    cursor.execute(sql, (food.name, float(food.quantity), food.measuring_units))
                else:
                    sql = "UPDATE food SET name=%s, quantity=%s, measuring_units=%s WHERE id=%s"
                    cursor.execute(sql, (food.name, float(food.quantity), food.measuring_units, int(food.id)))

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()

            if food.id == 0:
                with connection.cursor() as cursor:
                    sql = "SELECT LAST_INSERT_ID()"
                    cursor.execute(sql)
                    result = cursor.fetchone()
                    food.id = result['LAST_INSERT_ID()']
        finally:
            connection.close()
