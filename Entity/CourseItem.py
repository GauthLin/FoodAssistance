from Repository.CourseTypeRepository import CourseTypeRepository
from Repository.CourseItemRepository import CourseItemRepository


class CourseItem:
    def __init__(self, name, quantity, course_type):
        self.course_type_repository = CourseTypeRepository()
        self.course_item_repository = CourseItemRepository()

        self.id = 0
        self.name = name
        self.quantity = quantity
        self.course_type = self.course_type_repository.get_course_type_by_id(course_type)

    def save(self):
        """
        Saves the current CourseItem to the db:
            Creates a new entry if it does not exist
            Changes the entry if exists

        :return: the all CourseItem with his id
        """
        self.course_item_repository.save(self)

    def delete(self):
        """
        Deletes the current CourseItem from the db

        :return:
        """
        self.course_item_repository.delete(self)
