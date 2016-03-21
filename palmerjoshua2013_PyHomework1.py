"""
Joshua Palmer
COP 4020
Python Homework 1
22 March 2016

This script runs the entire homework assignment plus the extra credit.

- Each function in this script answers one or more question.
- The question(s) that each function answers is written as a comment near the function header.
- Some helper functions were created to make the program's output a little nicer to read.
"""


# ============================= #
#            HELPERS            #
# ============================= #
import pprint
pp = pprint.PrettyPrinter(indent=4)  # makes dictionaries look nicer when printed to the console


def make_pretty(title):
    """This decorator is used to print a header and footer around my output. Instead of littering every
       function with the same prints, prepending them with this decorator will automatically add them for me.
       :param title - The title of the section that will be printed. Can be any string."""

    length = 20  # length of each side of the header
    symbol = "#"  # the symbol used to print the header
    bottom_length = 2 + 2*length + len(title)  # length of the footer

    def decorator(func):
        def wrapper():
            print(symbol*length, title, symbol*length)  # print header
            func()  # call original function
            print(symbol*bottom_length)  # print footer
            print()  # print blank line
        return wrapper
    return decorator

# ============================= #
#        MAIN ASSIGNMENT        #
# ============================= #
classes = {}
'''I made this global because I have to print its contents long after the function that mutates it has finished executing.
There's no good reason to make this variable global other than making it more convenient to create/mutate it in problem #9-11
and print it in problem #20-21.'''


@make_pretty("NAME STUFF")
def name_stuff():  # questions 1-4
    msg = "Hello World"
    print(msg)

    age = 25
    print("{hi}, I am {thismany} today.".format(hi=msg, thismany=age))
    print(msg.upper())


@make_pretty("CASTING STUFF")
def casting_stuff():  # questions 5-8
    a = 3.14
    b, c = int(a), str(a)
    for variable in (a, b, c):
        print("{:>4}    {}".format(variable, type(variable)))


@make_pretty("CONTAINER STUFF")
def container_stuff():  # questions 9-11
    global classes
    favorite = ("lettuce", "dirt")
    print(favorite)

    classes = {"Formal Languages": "Fernandez",
               "Data Communications": "Mahgoub",
               "Programming Languages": "Huang"}

    pp.pprint(classes)
    print(favorite)


@make_pretty("DIV LISTS")
def div_lists():  # questions 12-18
    whole_range = range(1, 101)
    div_range = range(2, 6)

    whole = [i for i in whole_range]
    div2, div3, div4, div5 = [], [], [], []

    div_list = [div2, div3, div4, div5]
    for i in whole_range:
        for j in div_range:
            if i % j == 0:
                div_list[j-2].append(i)
    '''
    # faster solution
    div2 = [i for i in range(2, 101, 2)]
    div3 = [i for i in range(3, 101, 3)]
    div4 = [i for i in range(4, 101, 4)]
    div5 = [i for i in range(5, 101, 5)]

    # same solution, just more compact using dictionaries
    div_key = "div{}"
    divs = {div_key.format(i): [j for j in range(i, 101, i)] for i in range(2, 6)}
    pp.pprint(divs)
    '''

    print(whole)
    for lst in div_list:
        print(lst)

    divOver5 = list(filter(lambda lst: not any(lst in div for div in div_list), whole))
    '''
        Here the filter() function is performed on the list named 'whole.' It applies the lambda function on each element in
        'whole,' and it creates a new list containing the elements for which the lambda function returns True. In this case,
        it checks whether each element was not in any existing div list.

        Because the filter() function returns a generator and not a list, we cast the results into a list using
        the list() function.
    '''
    print(divOver5)


def exp3(x):  # question 19
    """The homework said to define the function, but it did not say to use it anywhere.
    :param x - an integer that will be cubed"""
    return "{} is divisible by 3".format(x**3)


@make_pretty("PRINT CLASSES")
def print_classes():  # questions 20-21

    for course in classes.keys():
        print("Class:", course)

    for professor in classes.values():
        print("Professor:", professor)
    '''
    # my preferred method when I need to access both keys and values
    for course, professor in classes.items():
        print("Class: {}    Professor: {}".format(course, professor))
    '''


# ============================= #
#          EXTRA CREDIT         #
# ============================= #
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


@make_pretty("STUDENT DEMO")
def student_demo():
    student_data = [{"name": "Josh", "age": 25, "birth_month": "June"},
                    {"name": "John", "age": 24, "birth_month": "July"},
                    {"name": "Jack", "age": 23, "birth_month": "August"}]

    # pass the student data as keyword arguments, and create multiple students with a list comprehension
    students = [Student(**student) for student in student_data]

    print("Student 1 Name:", students[0].display_name())
    print("Student 2 Month:", students[1].display_birth_month())
    print("Student Count:", Student.count)


def main():
    name_stuff()
    casting_stuff()
    container_stuff()
    div_lists()
    print_classes()
    student_demo()


if __name__ == '__main__':
    main()
