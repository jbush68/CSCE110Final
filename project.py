import csv as csv
import matplotlib as p_lib
from statistics import mean as avg
from typing import TypedDict


# Create custom dictionary class to pass to classroom class
class StudentDict(TypedDict):
    uin: str
    labs: list[float]
    quizzes: list[float]
    readings: list[float]
    exams: list[float]
    project: float


# Function to create student dictionary class based on user input, validate user input
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


# Define custom student class
class Student:
    # Initialize values of student properties based on input of student dictionary
    def __init__(self, student_data: StudentDict):
        self.uin = student_data["uin"]
        self.labs = student_data["labs"]
        self.quizzes = student_data["quizzes"]
        self.readings = student_data["readings"]
        self.exams = student_data["exams"]
        self.project = student_data["project"]
        self.total = None

    # Run analysis of student, generate report
    def analyze(self, class_d: "ClassSet"):
        means = [avg(self.exams), avg(self.labs), avg(self.quizzes), avg(self.readings), self.project]
        score = sum([m * w for m, w in zip(means, class_d.weights)])
        self.total = score

        if score >= 90:
            let = 'A'
        elif score >= 80:
            let = 'B'
        elif score >= 70:
            let = 'C'
        elif score >= 60:
            let = 'D'
        else:
            let = 'F'

        with open(f'{self.uin}.txt', 'w') as file_report:
            file_report.write(f"""Exams mean: {means[0]:.1f}
Labs mean: {means[1]:.1f}
Quizzes mean: {means[2]:.1f}
Reading activities mean: {means[3]:.1f}
Score: {score:.1f}%
Letter grade: {let}
""")


# Define custom classroom class
class ClassSet:
    # Initialize properties of the classroom class
    def __init__(self, weights: tuple[float, float, float, float, float]):
        self.students = None
        self.num_students = None
        self.weights = weights

    # Populate Class by reading series of csv rows and creating student objects
    def populate_class(self) -> None:
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
        self.num_students = len(self.students)


# Define menu printing and user selection, validate user input
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


# Main driver of the code, calls all functions from here and passes class object to whichever function requires it
def main() -> None:
    csce_class = ClassSet((0.15, 0.25, 0.10, 0.10, 0.10))
    while csce_class:
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
