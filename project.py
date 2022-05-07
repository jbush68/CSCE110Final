import csv as csv

import numpy
import numpy as np
from matplotlib import pyplot as plt
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
        labs = [float(_) for _ in student[1:7]]
        quizzes = [float(_) for _ in student[7:13]]
        readings = [float(_) for _ in student[13:19]]
        exams = [float(_) for _ in student[19:22]]
        project = float(student[22])
    except ValueError:
        print(f'Invalid student in file')
        return None

    return StudentDict(uin=uin,
                       labs=labs,
                       quizzes=quizzes,
                       readings=readings,
                       exams=exams,
                       project=project)


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
        self.letter = None

    def student_graphs(self):
        for attr, val in self.__dict__.items():
            if attr in ['uin', 'project', 'total', 'letter']:
                continue

            attr = str(attr)
            attr = attr.capitalize()

            x = numpy.arange(len(val))
            width = 0.5
            fig, ax = plt.subplots()
            ax.set_xticks(x)
            ax.set_title(attr)
            ax.set_ylabel("Score")
            ax.set_xlabel(f'{attr[0:-1]}')
            data = ax.bar(x - width / 2, val, width, label=attr)
            for i in data:
                height = i.get_height()
                ax.annotate('{}'.format(height),
                            xy=(i.get_x() + i.get_width() / 2, height),
                            xytext=(0, 2),
                            textcoords="offset points",
                            ha='center', va='bottom')

            plt.show()

    # Run analysis of student, generate report (aka menu option 2)
    def analyze(self, class_d: "ClassSet", to_print: bool):
        means = [avg(self.exams), avg(self.labs), avg(self.quizzes), avg(self.readings), self.project]
        self.total = sum([m * w for m, w in zip(means, class_d.weights)])

        if self.total >= 90:
            let = 'A'
        elif self.total >= 80:
            let = 'B'
        elif self.total >= 70:
            let = 'C'
        elif self.total >= 60:
            let = 'D'
        else:
            let = 'F'

        self.letter = let

        if to_print:
            with open(f'{self.uin}.txt', 'w') as file_report:
                file_report.write(f"""Exams mean: {means[0]:.1f}
    Labs mean: {means[1]:.1f}
    Quizzes mean: {means[2]:.1f}
    Reading activities mean: {means[3]:.1f}
    Score: {self.total:.1f}%
    Letter grade: {let}
    """)


# Define custom classroom class
class ClassSet:
    # Initialize properties of the classroom class
    def __init__(self, weights: tuple[float, float, float, float, float]):
        self.students = None
        self.num_students = None
        self.weights = weights

    # Populate Class by reading series of csv rows and creating student objects (aka menu option 1)
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

    def find_student(self) -> "Student":
        search_uin = str(input('Enter student uin: '))
        if not (search_uin.isnumeric() and len(search_uin) == 10):
            print('Invalid UIN, please try again...')
            return self.find_student()
        else:
            for student in self.students:
                if student.uin == search_uin:
                    return student
            else:
                print('Invalid UIN, please try again...')
                return self.find_student()

    def class_analysis(self):
        for student in self.students:
            if not student.total:
                student.analyze(self, False)

        class_grades = [student.total for student in self.students]

        grades_list = f"""Total number of students: {self.num_students}
Minimum score: {min(class_grades)}
Maximum score: {max(class_grades)}
Median score: {np.median(class_grades)}
Mean score: {avg(class_grades)}
Standard deviation: {np.std(class_grades)}"""

        with open('report.txt', 'w') as class_report:
            class_report.write(grades_list)

    def class_graphs(self):
        let_list = []

        for student in self.students:
            if not student.letter:
                student.analyze(self, False)
            else:
                let_list.append(student.letter)

        final_grade_counts = [let_list.count('A'), let_list.count('B'),
                              let_list.count('C'),
                              let_list.count('D'), let_list.count('F')]
        x = np.arange(len(final_grade_counts))
        width = 0.5
        fig, ax = plt.subplots()
        ax.set_title("Class Letter Grades")
        ax.set_ylabel("Number of Students")
        ax.set_xlabel("Letter Grade")
        a = ax.get_xticks().tolist()
        a[1] = 'A'
        a[2] = 'B'
        a[3] = 'C'
        a[4] = 'D'
        a[5] = 'F'
        ax.set_xticklabels(a)
        data = ax.bar(x, final_grade_counts, width)
        counter = 0
        for i in data:
            y_pos = i.get_height()
            ax.annotate(str(f'{final_grade_counts[counter]}').format(y_pos),
                        xy=(i.get_x() + i.get_width() / 2, y_pos),
                        xytext=(0, 5),
                        textcoords="offset points",
                        ha='center', va='bottom')
            counter += 1
        plt.show()
        
    def class_pie(self):
        let_list = []
        for student in self.students:
            if not student.letter:
                student.analyze(self, False)
            else:
                let_list.append(student.letter)
                
        final_grade_counts = [let_list.count('A'), let_list.count('B'),
                              let_list.count('C'),
                              let_list.count('D'), let_list.count('F')]
        y = np.array(final_grade_counts)
        labels = ["A", "B", "C", "D", "F"]
        print(final_grade_counts)
        plt.pie(y, labels=labels, autopct='%.2f%%')
        plt.title('Class Letter Grades')
        plt.show()


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
    csce_class = ClassSet((0.45, 0.25, 0.10, 0.10, 0.10))
    while csce_class:
        choice = menu()
        match choice:
            case 1:
                csce_class.populate_class()
                continue
            case 2:
                analysis_student = csce_class.find_student()
                analysis_student.analyze(csce_class, True)
                continue
            case 3:
                chart_student = csce_class.find_student()
                chart_student.student_graphs()
                continue
            case 4:
                csce_class.class_analysis()
            case 5:
                csce_class.class_graphs()
                csce_class.class_pie()
            case 6:
                return
            case _:
                print('Invalid input \n')
                continue


main()
