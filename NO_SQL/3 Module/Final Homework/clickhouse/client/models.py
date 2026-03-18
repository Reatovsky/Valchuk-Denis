from dataclasses import dataclass
from datetime import date

@dataclass
class Student:
    student_id: str
    full_name: str
    birth_date: date
    email: str
    faculty_code: str
    group_code: str
    enrollment_year: int
    status: str
    gpa: float
    
    def __str__(self):
        return f"{self.full_name} ({self.student_id})"

@dataclass
class Teacher:
    teacher_id: str
    full_name: str
    email: str
    position: str
    degree: str
    hire_date: date
    max_hours: int
    current_hours: int

@dataclass
class Grade:
    grade_id: str
    student_id: str
    course_code: str
    grade: int
    grade_type: str
    grade_date: date
    semester: int
    academic_year: str
