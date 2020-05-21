from abc import ABC, abstractmethod


class Department:
    def __init__(self, name, code):
        self.name = name
        self.code = code

    def get_hours(self):
        return 8


class Employee(ABC):
    def __init__(self, code, name, salary):
        self.code = code
        self.name = name
        self.salary = salary

    @abstractmethod
    def calc_bonus(self):
        pass

    @abstractmethod
    def get_hours(self):
        return 8


class Manager(Employee):
    def __init__(self, code, name, salary):
        super().__init__(code, name, salary)
        self.__department = Department('managers', 1)

    def calc_bonus(self):
        return self.salary * 0.15

    def set_department(self, department):
        self.__department.name = department

    def get_departament(self):
        return self.__department.name

    def get_hours(self):
        return 8

class Seller(Employee):
    def __init__(self, code, name, salary):
        super().__init__(code, name, salary)
        self.__department = Department('sellers', 2)
        self.__sales = 0

    def put_sales(self, value):
        self.__sales += value

    def get_sales(self):
        return self.__sales

    def calc_bonus(self):
        return self.__sales * 0.15

    def get_hours(self):
        return 8

    def set_department(self, department):
        self.__department.name = department

    def get_departament(self):
        return self.__department.name