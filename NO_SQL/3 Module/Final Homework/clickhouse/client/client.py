#!/usr/bin/env python3
from clickhouse_driver import Client
from tabulate import tabulate
from colorama import init, Fore, Style
import time
import os

init(autoreset=True)


class UniversityDBClient:
    def __init__(self, host='localhost', port=9000, database='university'):
        self.host = host
        self.port = port
        self.database = database
        self.client = None
        self.connect()

    def connect(self):
        try:
            self.client = Client(
                host=self.host,
                port=self.port,
                database=self.database,
                settings={'use_numpy': True,
                          'distributed_product_mode': 'allow'}
            )
            self.client.execute('SELECT 1')
            print(f"{Fore.GREEN}Подключено к {self.host}:{self.port}/{self.database}")
        except Exception as e:
            print(f"{Fore.RED}Ошибка подключения: {e}")
            self.client = None

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_header(self, title):
        print(f"\n{Fore.CYAN}{'=' * 60}")
        print(f"{Fore.YELLOW}{title:^60}")
        print(f"{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}\n")

    def print_menu(self):
        self.clear_screen()
        self.print_header("База данных университета")

        print(f"{Fore.WHITE}Студенты:")
        print(f"   {Fore.GREEN}1. {Fore.WHITE}Показать всех студентов")
        print(f"   {Fore.GREEN}2. {Fore.WHITE}Найти студента по ID или email")
        print(f"   {Fore.GREEN}3. {Fore.WHITE}Топ студентов по GPA")
        print(f"   {Fore.GREEN}4. {Fore.WHITE}Статистика по факультетам")

        print(f"\n{Fore.WHITE}Оценки:")
        print(f"   {Fore.GREEN}5. {Fore.WHITE}Показать оценки студента")
        print(f"   {Fore.GREEN}6. {Fore.WHITE}Статистика успеваемости по предметам")
        print(f"   {Fore.GREEN}7. {Fore.WHITE}Распределение оценок")

        print(f"\n{Fore.WHITE}Преподаватели:")
        print(f"   {Fore.GREEN}8. {Fore.WHITE}Список преподавателей")
        print(f"   {Fore.GREEN}9. {Fore.WHITE}Нагрузка преподавателей")

        print(f"\n{Fore.WHITE}Расписание:")
        print(f"   {Fore.GREEN}10. {Fore.WHITE}Расписание для группы")
        print(f"   {Fore.GREEN}11. {Fore.WHITE}Расписание преподавателя")

        print(f"\n{Fore.WHITE}Аналитика:")
        print(f"   {Fore.GREEN}12. {Fore.WHITE}Общая статистика БД")
        print(f"   {Fore.GREEN}13. {Fore.WHITE}Распределение по шардам")
        print(f"   {Fore.GREEN}14. {Fore.WHITE}Сложные запросы (JOIN)")

        print(f"\n{Fore.WHITE}Управление:")
        print(f"   {Fore.GREEN}15. {Fore.WHITE}Добавить студента")
        print(f"   {Fore.GREEN}16. {Fore.WHITE}Добавить оценку")
        print(f"   {Fore.GREEN}17. {Fore.WHITE}Обновить GPA студента")

        print(f"\n   {Fore.RED}0. {Fore.WHITE}Выход")
        print(f"{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}")

    def run(self):
        if not self.client:
            print(f"{Fore.RED}Нет подключения к БД. Завершение работы.")
            return

        while True:
            self.print_menu()
            choice = input(f"{Fore.YELLOW}Выберите опцию (0-17): {Style.RESET_ALL}")

            if choice == '1':
                self.show_all_students()
            elif choice == '2':
                self.find_student()
            elif choice == '3':
                self.top_students()
            elif choice == '4':
                self.faculty_stats()
            elif choice == '5':
                self.student_grades()
            elif choice == '6':
                self.course_stats()
            elif choice == '7':
                self.grade_distribution()
            elif choice == '8':
                self.show_teachers()
            elif choice == '9':
                self.teacher_workload()
            elif choice == '10':
                self.group_schedule()
            elif choice == '11':
                self.teacher_schedule()
            elif choice == '12':
                self.db_stats()
            elif choice == '13':
                self.shard_distribution()
            elif choice == '14':
                self.complex_queries()
            elif choice == '15':
                self.add_student()
            elif choice == '16':
                self.add_grade()
            elif choice == '17':
                self.update_gpa()
            elif choice == '0':
                print(f"\n{Fore.GREEN}До свидания!")
                break
            else:
                print(f"{Fore.RED}Неверный выбор!")

            input(f"\n{Fore.YELLOW}Нажмите Enter для продолжения...{Style.RESET_ALL}")

    def show_all_students(self, limit=20):
        self.print_header("Список студентов")

        query = """
        SELECT 
            student_id,
            full_name,
            faculty_code,
            group_code,
            enrollment_year,
            status,
            gpa
        FROM students
        ORDER BY faculty_code, group_code, full_name
        LIMIT %(limit)s
        """

        try:
            result = self.client.execute(query, {'limit': limit})
            if result:
                headers = ['ID', 'ФИО', 'Факультет', 'Группа', 'Год', 'Статус', 'GPA']
                print(tabulate(result, headers=headers, tablefmt='grid', numalign='center'))
                print(f"\n{Fore.GREEN}Показано {len(result)} из {self.get_count('students')} студентов")
            else:
                print(f"{Fore.YELLOW}Нет данных")
        except Exception as e:
            print(f"{Fore.RED}Ошибка: {e}")

    def find_student(self):
        self.print_header("Поиск студента")

        search_type = input("Искать по (1 - ID, 2 - Email): ")

        if search_type == '1':
            student_id = input("Введите ID студента (например STU1001): ")
            query = "SELECT * FROM students WHERE student_id = %(id)s"
            params = {'id': student_id}
        elif search_type == '2':
            email = input("Введите email: ")
            query = "SELECT * FROM students WHERE email LIKE %(email)s"
            params = {'email': f'%{email}%'}
        else:
            print(f"{Fore.RED}Неверный выбор")
            return

        try:
            result = self.client.execute(query, params)
            if result:
                self.print_student_details(result[0])
            else:
                print(f"{Fore.YELLOW}Студент не найден")
        except Exception as e:
            print(f"{Fore.RED}Ошибка: {e}")

    def print_student_details(self, student):
        print(f"\n{Fore.CYAN}Детальная информация:")
        print(f"   ID: {Fore.WHITE}{student[0]}")
        print(f"   ФИО: {Fore.WHITE}{student[1]}")
        print(f"   Дата рождения: {Fore.WHITE}{student[2]}")
        print(f"   Email: {Fore.WHITE}{student[3]}")
        print(f"   Факультет: {Fore.WHITE}{student[4]}")
        print(f"   Группа: {Fore.WHITE}{student[5]}")
        print(f"   Год поступления: {Fore.WHITE}{student[6]}")
        print(f"   Статус: {Fore.WHITE}{student[7]}")
        print(f"   GPA: {Fore.WHITE}{student[8]}")

    def top_students(self):
        self.print_header("Топ студентов по GPA")
        limit = input("Сколько показать? (по умолчанию 10): ") or "10"

        query = """
        SELECT 
            s.full_name,
            s.faculty_code,
            s.group_code,
            s.gpa,
            COUNT(g.grade) as grades_count
        FROM students s
        LEFT JOIN grades g ON s.student_id = g.student_id
        WHERE s.status = 'active'
        GROUP BY s.full_name, s.faculty_code, s.group_code, s.gpa
        ORDER BY s.gpa DESC
        LIMIT %(limit)s
        """

        try:
            result = self.client.execute(query, {'limit': int(limit)})
            if result:
                headers = ['ФИО', 'Факультет', 'Группа', 'GPA', 'Оценок']
                print(tabulate(result, headers=headers, tablefmt='grid', floatfmt='.2f'))
            else:
                print(f"{Fore.YELLOW}Нет данных")
        except Exception as e:
            print(f"{Fore.RED}Ошибка: {e}")

    def faculty_stats(self):
        self.print_header("Статистика по факультетам")

        query = """
        SELECT 
            faculty_code,
            count() as student_count,
            countIf(status='active') as active_count,
            round(avg(gpa), 2) as avg_gpa,
            min(gpa) as min_gpa,
            max(gpa) as max_gpa
        FROM students
        GROUP BY faculty_code
        ORDER BY avg_gpa DESC
        """

        try:
            result = self.client.execute(query)
            if result:
                headers = ['Факультет', 'Всего', 'Активных', 'Ср. GPA', 'Мин', 'Макс']
                print(tabulate(result, headers=headers, tablefmt='grid', floatfmt='.2f'))
            else:
                print(f"{Fore.YELLOW}Нет данных")
        except Exception as e:
            print(f"{Fore.RED}Ошибка: {e}")

    def student_grades(self):
        self.print_header("Оценки студента")

        student_id = input("Введите ID студента (например STU1001): ")

        query = """
        SELECT 
            g.course_code,
            c.course_name,
            g.grade,
            g.grade_type,
            g.grade_date,
            g.semester,
            g.academic_year
        FROM grades g
        LEFT JOIN courses c ON g.course_code = c.course_code
        WHERE g.student_id = %(student_id)s
        ORDER BY g.grade_date DESC
        """

        try:
            result = self.client.execute(query, {'student_id': student_id})
            if result:
                headers = ['Курс', 'Название', 'Оценка', 'Тип', 'Дата', 'Семестр', 'Год']
                print(tabulate(result, headers=headers, tablefmt='grid'))

                # Средний балл
                avg_query = "SELECT round(avg(grade), 2) FROM grades WHERE student_id = %(student_id)s"
                avg = self.client.execute(avg_query, {'student_id': student_id})[0][0]
                print(f"\n{Fore.GREEN}Средний балл: {avg}")
            else:
                print(f"{Fore.YELLOW}Оценки не найдены")
        except Exception as e:
            print(f"{Fore.RED}Ошибка: {e}")

    def course_stats(self):
        self.print_header("Успеваемость по предметам")

        query = """
        SELECT 
            g.course_code,
            c.course_name,
            count() as grades_count,
            round(avg(g.grade), 2) as avg_grade,
            countDistinct(g.student_id) as students_count,
            countIf(g.grade = 5) as excellent,
            countIf(g.grade = 2) as failed
        FROM grades g
        LEFT JOIN courses c ON g.course_code = c.course_code
        GROUP BY g.course_code, c.course_name
        ORDER BY avg_grade DESC
        LIMIT 20
        """

        try:
            result = self.client.execute(query)
            if result:
                headers = ['Код', 'Название', 'Оценок', 'Ср. балл', 'Студентов', 'Отлично', 'Двоек']
                print(tabulate(result, headers=headers, tablefmt='grid', floatfmt='.2f'))
            else:
                print(f"{Fore.YELLOW}Нет данных")
        except Exception as e:
            print(f"{Fore.RED}Ошибка: {e}")

    def grade_distribution(self):
        self.print_header("Распределение оценок")

        query = """
        SELECT 
            grade,
            count() as count,
            round(count() * 100.0 / sum(count()) over(), 2) as percentage
        FROM grades
        GROUP BY grade
        ORDER BY grade
        """

        try:
            result = self.client.execute(query)
            if result:
                headers = ['Оценка', 'Количество', 'Процент']
                print(tabulate(result, headers=headers, tablefmt='grid', floatfmt='.2f'))

                print(f"\n{Fore.CYAN}Визуализация:")
                for row in result:
                    bar = '█' * int(row[2])
                    print(f"  {row[0]}: {bar} {row[2]}%")
            else:
                print(f"{Fore.YELLOW}Нет данных")
        except Exception as e:
            print(f"{Fore.RED}Ошибка: {e}")

    def show_teachers(self):
        self.print_header("Преподаватели")

        query = """
        SELECT 
            teacher_id,
            full_name,
            position,
            degree,
            hire_date,
            current_hours,
            max_hours
        FROM teachers
        ORDER BY position, full_name
        LIMIT 30
        """

        try:
            result = self.client.execute(query)
            if result:
                headers = ['ID', 'ФИО', 'Должность', 'Степень', 'Дата найма', 'Часов', 'Макс']
                print(tabulate(result, headers=headers, tablefmt='grid'))
            else:
                print(f"{Fore.YELLOW}Нет данных")
        except Exception as e:
            print(f"{Fore.RED}Ошибка: {e}")

    def teacher_workload(self):
        self.print_header("Нагрузка преподавателей")

        query = """
        SELECT 
            t.full_name,
            t.position,
            t.current_hours,
            t.max_hours,
            round(t.current_hours * 100.0 / t.max_hours, 1) as workload_percent,
            count(DISTINCT s.course_code) as courses_count
        FROM teachers t
        LEFT JOIN schedule s ON t.teacher_id = s.teacher_id
        GROUP BY t.full_name, t.position, t.current_hours, t.max_hours
        ORDER BY workload_percent DESC
        LIMIT 20
        """

        try:
            result = self.client.execute(query)
            if result:
                headers = ['ФИО', 'Должность', 'Часов', 'Макс', 'Загрузка %', 'Курсов']
                print(tabulate(result, headers=headers, tablefmt='grid', floatfmt='.1f'))
            else:
                print(f"{Fore.YELLOW}Нет данных")
        except Exception as e:
            print(f"{Fore.RED}Ошибка: {e}")

    def group_schedule(self):
        self.print_header("Расписание группы")

        group = input("Введите код группы (например FIT-21-1): ")

        query = """
        SELECT 
            day_of_week,
            pair_number,
            course_code,
            t.full_name as teacher,
            classroom,
            week_type
        FROM schedule s
        LEFT JOIN teachers t ON s.teacher_id = t.teacher_id
        WHERE group_code = %(group)s
        ORDER BY day_of_week, pair_number
        """

        days = {1: 'ПН', 2: 'ВТ', 3: 'СР', 4: 'ЧТ', 5: 'ПТ', 6: 'СБ'}

        try:
            result = self.client.execute(query, {'group': group})
            if result:
                current_day = 0
                for row in result:
                    if row[0] != current_day:
                        print(f"\n{Fore.CYAN}{days.get(row[0], 'День')}:")
                        current_day = row[0]
                    print(f"  {row[1]}-я пара: {row[2]} - {row[3]} ({row[4]}, {row[5]})")
            else:
                print(f"{Fore.YELLOW}Расписание не найдено")
        except Exception as e:
            print(f"{Fore.RED}Ошибка: {e}")

    def teacher_schedule(self):
        self.print_header("Расписание преподавателя")

        teacher = input("Введите ID преподавателя (например TCH001): ")

        query = """
        SELECT 
            s.group_code,
            s.course_code,
            s.day_of_week,
            s.pair_number,
            s.classroom,
            s.week_type
        FROM schedule s
        WHERE teacher_id = %(teacher)s
        ORDER BY day_of_week, pair_number
        """

        days = {1: 'ПН', 2: 'ВТ', 3: 'СР', 4: 'ЧТ', 5: 'ПТ', 6: 'СБ'}

        try:
            result = self.client.execute(query, {'teacher': teacher})
            if result:
                current_day = 0
                for row in result:
                    if row[2] != current_day:
                        print(f"\n{Fore.CYAN}{days.get(row[2], 'День')}:")
                        current_day = row[2]
                    print(f"  {row[3]}-я пара: Группа {row[0]}, {row[1]} ({row[4]}, {row[5]})")
            else:
                print(f"{Fore.YELLOW}Расписание не найдено")
        except Exception as e:
            print(f"{Fore.RED}Ошибка: {e}")

    def db_stats(self):
        self.print_header("Общая статистика БД")

        stats = []
        tables = ['students', 'teachers', 'courses', 'grades', 'schedule', 'departments']

        for table in tables:
            try:
                count = self.client.execute(f"SELECT count() FROM {table}")[0][0]
                stats.append([table, count])
            except:
                stats.append([table, 'Ошибка'])

        headers = ['Таблица', 'Количество записей']
        print(tabulate(stats, headers=headers, tablefmt='grid'))

        print(f"\n{Fore.CYAN}Дополнительная информация:")

        active = self.client.execute("SELECT count() FROM students WHERE status='active'")[0][0]
        print(f"  Активных студентов: {active}")

        avg_gpa = self.client.execute("SELECT round(avg(gpa), 2) FROM students WHERE status='active'")[0][0]
        print(f"  Средний GPA: {avg_gpa}")

        avg_grade = self.client.execute("SELECT round(avg(grade), 2) FROM grades")[0][0]
        print(f"  Средняя оценка: {avg_grade}")

    def shard_distribution(self):
        self.print_header("Распределение по шардам")

        ports = [9000, 9001, 9002]
        shard_data = []

        for port in ports:
            try:
                node_client = Client(host='localhost', port=port, database='university')
                host = node_client.execute("SELECT hostName()")[0][0]

                students = node_client.execute("SELECT count() FROM students_local")[0][0]
                grades = node_client.execute("SELECT count() FROM grades_local")[0][0]

                shard_data.append([host, port, students, grades])
            except Exception as e:
                shard_data.append([f"node:{port}", port, 'ERR', 'ERR'])

        headers = ['Шард', 'Порт', 'Студентов', 'Оценок']
        print(tabulate(shard_data, headers=headers, tablefmt='grid'))

    def complex_queries(self):
        self.print_header("Сложные запросы (JOIN)")

        print("1. Студенты и их средний балл с количеством оценок")
        print("2. Преподаватели и их предметы")
        print("3. Статистика по группам")
        print("4. Лучшие студенты на курсе")

        choice = input(f"\n{Fore.YELLOW}Выберите запрос (1-4): {Style.RESET_ALL}")

        if choice == '1':
            query = """
            SELECT 
                s.student_id,
                s.full_name,
                s.group_code,
                round(avg(g.grade), 2) as avg_grade,
                count(g.grade) as grades_count,
                s.gpa
            FROM students s
            JOIN grades g ON s.student_id = g.student_id
            GROUP BY s.student_id, s.full_name, s.group_code, s.gpa
            HAVING count(g.grade) > 5
            ORDER BY avg_grade DESC
            LIMIT 15
            """
            headers = ['ID', 'ФИО', 'Группа', 'Ср. балл', 'Оценок', 'GPA']
        elif choice == '2':
            query = """
            SELECT 
                t.full_name,
                t.position,
                count(DISTINCT s.course_code) as courses,
                count(DISTINCT s.group_code) as groups
            FROM teachers t
            JOIN schedule s ON t.teacher_id = s.teacher_id
            GROUP BY t.full_name, t.position
            ORDER BY courses DESC
            LIMIT 15
            """
            headers = ['Преподаватель', 'Должность', 'Курсов', 'Групп']
        elif choice == '3':
            query = """
            SELECT 
                s.group_code,
                count(DISTINCT s.student_id) as students,
                round(avg(g.grade), 2) as avg_grade,
                round(avg(s.gpa), 2) as avg_gpa
            FROM students s
            LEFT JOIN grades g ON s.student_id = g.student_id
            GROUP BY s.group_code
            HAVING count(DISTINCT s.student_id) > 0
            ORDER BY avg_grade DESC
            LIMIT 15
            """
            headers = ['Группа', 'Студентов', 'Ср. оценка', 'Ср. GPA']
        elif choice == '4':
            query = """
            WITH ranked AS (
                SELECT 
                    s.student_id,
                    s.full_name,
                    s.group_code,
                    g.course_code,
                    g.grade,
                    ROW_NUMBER() OVER (PARTITION BY g.course_code ORDER BY g.grade DESC) as rn
                FROM grades g
                JOIN students s ON g.student_id = s.student_id
            )
            SELECT course_code, full_name, group_code, grade
            FROM ranked
            WHERE rn <= 3
            ORDER BY course_code, rn
            LIMIT 30
            """
            headers = ['Курс', 'Студент', 'Группа', 'Оценка']
        else:
            print(f"{Fore.RED}Неверный выбор")
            return

        try:
            result = self.client.execute(query)
            if result:
                print(tabulate(result, headers=headers, tablefmt='grid'))
            else:
                print(f"{Fore.YELLOW}Нет данных")
        except Exception as e:
            print(f"{Fore.RED}Ошибка: {e}")

    def add_student(self):
        self.print_header("Добавить студента")

        print("Введите данные студента:")

        max_id = self.client.execute("SELECT max(toInt64(substring(student_id, 4))) FROM students")[0][0]
        if max_id is None:
            max_id = 1000
        new_id = f"STU{max_id + 1}"
        print(f"ID: {new_id}")

        full_name = input("ФИО: ")
        birth_date = input("Дата рождения (ГГГГ-ММ-ДД): ")
        email = input("Email: ")
        faculty = input("Код факультета (FIT, FEF, FME, FLW, FMS): ").upper()
        group = input("Группа (например FIT-21-1): ")
        year = input("Год поступления: ")

        query = """
        INSERT INTO students 
        (student_id, full_name, birth_date, email, faculty_code, group_code, enrollment_year, status, gpa)
        VALUES
        """

        try:
            self.client.execute(query,
                                [(new_id, full_name, birth_date, email, faculty, group, int(year), 'active', 0.0)])
            print(f"{Fore.GREEN}Студент успешно добавлен с ID {new_id}")
        except Exception as e:
            print(f"{Fore.RED}Ошибка: {e}")

    def add_grade(self):
        self.print_header("Добавить оценку")

        student_id = input("ID студента: ")

        check = self.client.execute("SELECT count() FROM students WHERE student_id = %(id)s", {'id': student_id})[0][0]
        if check == 0:
            print(f"{Fore.RED}Студент не найден")
            return

        grade_id = f"GRD{int(time.time())}"
        course = input("Код курса: ")
        grade = input("Оценка (2-5): ")
        grade_type = input("Тип (exam/test/coursework/lab/project): ")
        semester = input("Семестр (1-8): ")

        query = """
        INSERT INTO grades 
        (grade_id, student_id, course_code, grade, grade_type, grade_date, semester, academic_year)
        VALUES
        """

        try:
            self.client.execute(query, [(
                grade_id, student_id, course, int(grade), grade_type,
                time.strftime('%Y-%m-%d'), int(semester), '2023-2024'
            )])
            print(f"{Fore.GREEN}Оценка успешно добавлена")
        except Exception as e:
            print(f"{Fore.RED}Ошибка: {e}")

    def update_gpa(self):
        self.print_header("Обновление GPA")

        student_id = input("ID студента: ")

        query = """
        SELECT round(avg(grade), 2) 
        FROM grades 
        WHERE student_id = %(id)s
        """

        try:
            new_gpa = self.client.execute(query, {'id': student_id})[0][0]
            if new_gpa:
                update = """
                ALTER TABLE students 
                UPDATE gpa = %(gpa)s 
                WHERE student_id = %(id)s
                """
                self.client.execute(update, {'gpa': new_gpa, 'id': student_id})
                print(f"{Fore.GREEN}GPA обновлен до {new_gpa}")
            else:
                print(f"{Fore.YELLOW}Нет оценок для расчета GPA")
        except Exception as e:
            print(f"{Fore.RED}Ошибка: {e}")

    def get_count(self, table):
        try:
            return self.client.execute(f"SELECT count() FROM {table}")[0][0]
        except:
            return 0


HOST = 'localhost'
PORT = 9000
DATABASE = 'test'

app = UniversityDBClient(host=HOST, port=PORT, database=DATABASE)
app.run()
