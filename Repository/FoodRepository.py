from Entity.Food import Food
from Manager.DBManager import DBManager


class FoodRepository:
    def __init__(self):
        self.db_manager = DBManager()

    def save(self, food):
        """
            Sauve l'objet food dans la base de données. Si l'objet existe déjà alors crée une nouvelle entrée
            sinon modifie l'entrée existante
        """
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

    def get_foods(self):
        """
        :return: foods: liste de nourritures
        """
        connection = self.db_manager.connect()
        foods = []

        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM food"
                cursor.execute(sql)
                for row in cursor.fetchall():
                    print(row['name'], row['quantity'], row['measuring_units'])
                    food = Food(row['name'], row['quantity'], row['measuring_units'])
                    food.id = row['id']
                    foods.append(food)
        finally:
            connection.close()

        return foods
