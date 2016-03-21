"""
Joshua Palmer
COP 4020
Python Homework 1
22 March 2016

This is the extra credit assignment. It contains the Student class and a demonstration function.

This script may be run directly, but only the extra credit assignment will run. To view the entire homework assignment including
the extra credit, run palmerjoshua2013_PyHomework1.py.
"""


class Student:
    count = 0  # static variable to count number of Student instances

    def __init__(self, name="", age=0, birth_month=""):
        """Create student data, either from parameters or by getting keyboard input from the user.
        :param name - name of the student. If omitted, the user will be asked to provide a value using the keyboard.
        :param age - age of the student; if omitted, the user will be asked to provide a value using the keyboard.
        :param birth_month - birth month of the student. If omitted, the user will be asked to provide a value using the keyboard.
        """
        Student.count += 1
        self.name = name or input("Enter name for student #{}: ".format(Student.count))
        self.age = age or Student._get_age()
        self.birth_month = birth_month or input("Enter birth month for student #{}: ".format(Student.count))

    def display_name(self):
        """Although the homework asks us to use the word 'display' in our function names, the homework also says the functions
        should just return the values and not print the values or display them in any other way."""
        return self.name

    def display_birth_month(self):
        return self.birth_month

    @staticmethod
    def _get_age():
        """Used to get an integer from keyboard input. If the input cannot be cast to an integer, the user is asked to re-enter
        the input until it can be cast to an integer."""
        age = None
        while not age:
            try:
                age = int(input("Enter age for student #{}: ".format(Student.count)))
            except ValueError:
                print("Invalid value for student age. Please enter an integer.")
        return age


def do_demo():
    student_data = [{"name": "Josh", "age": 25, "birth_month": "June"},
                    {"name": "John", "age": 24, "birth_month": "July"},
                    {"name": "Jack", "age": 23, "birth_month": "August"}]

    # pass the student data as keyword arguments, and create multiple students with a list comprehension
    students = [Student(**student) for student in student_data]

    print("Student 1 Name:", students[0].display_name())
    print("Student 2 Month:", students[1].display_birth_month())
    print("Student Count:", Student.count)


if __name__ == '__main__':
    do_demo()
    print()
    msg = "Note: You have only run the extra credit demo.\n" \
          "If you're looking for the entire homework assignment, please run palmerjoshua2013_PyHomework1.py."
    print(msg)
