import csv as csv
import matplotlib as p_lib
from typing import TypedDict


class StudentDict(TypedDict):
    uin: str
    labs: list[float]
    quizzes: list[float]
    readings: list[float]
    exams: list[float]
    project: float


def cast_student_dict(student) -> StudentDict or None:
    try:
        uin = str(student[0])
        labs = [float(_) for _ in student[1:6]]
        quizzes = [float(_) for _ in student[7:12]]
        readings = [float(_) for _ in student[13:18]]
        exams = [float(_) for _ in student[19:21]]
        project = float(student[23])
    except ValueError:
        print(f'Invalid student in file')
        return None

    return StudentDict(uin=uin, labs=labs, quizzes=quizzes, readings=readings, exams=exams, project=project)


class Student:
    def __init__(self, student_data: StudentDict):
        self.uin = student_data["uin"]
        self.labs = student_data["labs"]
        self.quizzes = student_data["quizzes"]
        self.readings = student_data["readings"]
        self.exams = student_data["exams"]
        self.project = student_data["project"]


class ClassSet:
    def __init__(self):
        self.students = list[Student]
        self.num_students = len(self.students)

    def populate_class(self):
        file_path = str(input('Enter file path: '))
        students = []
        with open(file_path, newline='') as class_file:
            student_list = csv.reader(class_file, delimiter=',')
            for index, row in enumerate(student_list):
                if index == 0:
                    continue
                data = cast_student_dict(row)
                if not data:
                    continue
                else:
                    students.append(Student(data))

        self.students = students


def menu() -> int:
    print("""*******************Main Menu*****************
1. Read CSV file of grades
2. Generate student report file
3. Generate student report charts
4. Generate class report file
5. Generate class report charts
6. Quit
************************************************\n""")
    try:
        return int(input('Enter option: '))
    except ValueError:
        print('Invalid input \n')
        menu()


def main() -> None:
    choice = menu()
    match choice:
        case 1:
            pass
        case 2:
            pass
        case 3:
            pass
        case 4:
            pass
        case 5:
            pass
        case 6:
            return
        case _:
            print('Invalid input \n')
            main()


main()
