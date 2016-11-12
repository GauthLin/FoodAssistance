from Repository.FoodRepository import FoodRepository


class Food:
    def __init__(self, name, quantity, measuring_units):
        self.id = 0
        self.name = name
        self.quantity = quantity
        self.measuring_units = measuring_units

        self.food_repository = FoodRepository()

    def save(self):
        self.food_repository.save(self)
