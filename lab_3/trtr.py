# продукт пользователь заказ ,
# продукт название цена количесство на складе,
# пользователь имя почта список товаров в корзине,
# заказ инфа о покупателе списке товаров и общей стоимости,
# класс про радиофизика
class Student():
    def __init__(self, name, group, average_grade):
        self.name = name
        self.group = group
        self.average_grade = average_grade
        self.subjects = []

    def add_subject(self, subject):
        self.subjects.append(subject)
        print(f"{self.name} добавил предмет: {subject}")

    def show_info(self):
        print(f"Студент: {self.name}, Группа: {self.group}, Средний балл: {self.average_grade}")

    def show_subjects(self):
        if self.subjects:
            print(f"Предметы {self.name}: {', '.join(self.subjects)}")
        else:
            print(f"У {self.name} нет предметов")

    def __str__(self):
        return f"{self.name} (группа: {self.group})"


class Curator:
    def __init__(self, name, department):
        self.name = name
        self.department = department
        self.students = []

    def add_student(self, student):
        self.students.append(student)
        print(f"{student.name} добавлен к куратору {self.name}")

    def show_all_students(self):
        print(f"\nСтуденты куратора {self.name}:")
        for student in self.students:
            student.show_info()

    def find_student_by_name(self, name):
        for student in self.students:
            if student.name.lower() == name.lower():
                return student
        return None

    def get_best_student(self):
        return max(self.students, key=lambda x: x.average_grade)


def main():
    print("Система студентов и кураторов")

    curator_name = input("Введите имя куратора: ")
    curator_department = input("Введите отделение куратора: ")
    curator = Curator(curator_name, curator_department)
    print(f"Создан куратор: {curator.name} ({curator.department})")

    while True:
        try:
            print("\n1 - Добавить студента")
            print("2 - Показать всех студентов")
            print("3 - Найти студента")
            print("4 - Показать лучшего студета")
            print("5 - Выйти")

            choice = input("Выберите действие: ")

            if choice == "1":
                name = input("Введите имя студента: ")
                if not name.strip():
                    raise ValueError("Имя студента не может быть пустым")
                group = input("Введите группу студента: ")
                average_grade = float(input("Введите средний балл студента: "))
                if average_grade < 0 or average_grade > 10:
                    raise ValueError("Средний балл должен быть от 0 до 10")

                student = Student(name, group, average_grade)

                while True:
                    subject = input("Введите предмет (или 'стоп' чтобы закончить): ")
                    if subject.lower() == 'стоп':
                        break
                    student.add_subject(subject)

                curator.add_student(student)

            elif choice == "2":
                curator.show_all_students()

            elif choice == "3":
                name = input("Введите имя студента для поиска: ")
                found_student = curator.find_student_by_name(name)
                if found_student:
                    print("Найден студент:")
                    found_student.show_info()
                    found_student.show_subjects()
                else:
                    print("Студент не найден")
            elif choice == "4":
                if curator.students:
                    best_student = curator.get_best_student()
                    print("Лучший студент:")
                    best_student.show_info()
                else:
                    print("Нет студентов")
            elif choice == "5":
                print("Выход из программы")
                break
            else:
                print("Неверный выбор")
        except ValueError as e:
            print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()