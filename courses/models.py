import copy
import datetime


# class Singleton:
#     def __new__(cls, *args, **kwargs):
#         if not hasattr(cls, 'instance'):
#             cls.instance = super(Singleton, cls).__new__(cls)
#         return cls.instance

class MetaSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Logger:

    def log(self, msg: str):
        print(f'{self.file_name}: {msg}')
        with open(self.file_name, 'a', encoding='utf-8') as file:
            file.write(f'{datetime.datetime.now()}: {msg}\n')


class ModelLogger(Logger, metaclass=MetaSingleton):
    file_name = 'static/model.log'


class ViewLogger(Logger, metaclass=MetaSingleton):
    file_name = 'static/view.log'


class Person:
    pass


class Student(Person):
    courses = list()


class Teacher(Person):
    courses = list()


class PersonFactory:
    _data = {
        'student': Student,
        'teacher': Teacher,
    }

    @classmethod
    def make(cls, data_type):
        return _data[data_type]()


class CoursePrototype:
    def clone(self):
        return copy.deepcopy(self)


class CourseCategory(CoursePrototype):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f'{self.name}'


class Course(CoursePrototype):
    def __init__(self, name, category=None):
        self.name = name
        self.category = category

    def __str__(self):
        return f'Course: {self.name}'
