#In student_data.py, complete:


#1.add_student(): Collects student name, age, and grade.

#Create an input that asks for student details
student_name = input('What is your name: ')
age = int(input('What is your age: '))
grade = int(input('What is your grade: '))

#This empty list stores the student details
students = []

#FUNCTION TO PASS STUDENT DETAILS
def add_student(student_name, age, grade):
    student_information = {
        'name': student_name,
        'age': age,
        'grade': grade
    }
    return student_information


 

#Save function into a variable
student = add_student(student_name, age, grade)

#Finally append variable into earlier empty list
students.append(student)




#2. view_students(): Displays all added students.

#Create a function view_students
def view_students():
    #Loop through the list created.
    print("\nAll students in the list:")
    for stu in students:
        print(stu) 

print("Student added:", student)


view_students()

#get_average_grade(): Calculates the average of all grades.
#In main.py, call the functions using a simple menu system.

def get_average_grade():
    if not students:
        return 0  # or None if you prefer, when no students exist
    total = sum(st['grade'] for st in students)
    average = total / len(st)
    return average




