from typing import List, Dict, Optional, Tuple, Callable
import sys

MENU_OPTIONS = {
    "1": "Add a new student",
    "2": "Add grades for a student",
    "3": "Generate a full report",
    "4": "Find the top student",
    "5": "Exit program"
}

class StudentManager:

    def __init__(self) -> None:
        self.students: List[Dict[str, object]] = []
        self._student_names: set[str] = set()
        self._cached_averages: Dict[str, float] = {}
        self._is_cache_dirty: bool = True

    def add_new_student(self, name: str) -> bool:
        """Add a new student with O(1) complexity."""
        normalized_name = name.strip().lower()

        if normalized_name in self._student_names:
            print(f"Student with name {normalized_name} already exists.")
            return False

        self.students.append({"name": normalized_name, "grades": []})
        self._student_names.add(normalized_name)
        self._is_cache_dirty = True
        print(f"Added new student {normalized_name}")
        return True

    def find_student_by_name(self, name: str) -> Optional[Dict[str, object]]:
        normalized_name = name.strip().lower()

        if normalized_name not in self._student_names:
            return None

        for student in self.students:
            if student["name"].lower() == normalized_name:
                return student
        return None


    def add_grades_for_student(self, name: str, grades: List[float]) -> bool:
        student = self.find_student_by_name(name)
        if not student:
            print(f"Student with name {name} doesn't exist.")
            return False

        student["grades"].extend(grades)
        self._is_cache_dirty = True
        print(f"Added {len(grades)} grades for student {student['name']}")
        return True

    def _calculate_all_averages(self) -> Dict[str, float]:
        if not self._is_cache_dirty and self._cached_averages:
            return self._cached_averages

        averages = {}
        for student in self.students:
            grades = student["grades"]
            if grades:
                averages[student["name"]] = sum(grades) / len(grades)

        self._cached_averages = averages
        self._is_cache_dirty = False
        return averages

    def get_student_average(self, student: Dict[str, object]) -> Optional[float]:
        averages = self._calculate_all_averages()
        return averages.get(student["name"])

    def show_report(self) -> None:
        if not self.students:
            print("No students available.")
            return

        print("\n--- Student Report ---")
        averages = self._calculate_all_averages()

        student_average = []
        for student in self.students:
            avg = averages.get(student["name"])
            if avg is None:
                print(f"{student['name']}'s average grade is N/A.")
            else:
                print(f"{student['name']}'s average grade is {avg:.1f}.")
                student_average.append(avg)

        self._show_summary_statistics(student_average)

    def _show_summary_statistics(self, averages: List[float]) -> None:
        if not averages:
            print("\nNo grades available.")
            return

        max_avg = max(averages)
        min_avg = min(averages)
        overall_avg = sum(averages) / len(averages)

        print("--------------------------")
        print(f"Max average: {max_avg:.1f}")
        print(f"Min average: {min_avg:.1f}")
        print(f"Overall average: {overall_avg:.1f}")

    def find_top_performer(self)-> None:
        if not self.students:
            print("No students available.")
            return

        averages = self._calculate_all_averages()
        if not averages:
            print("No students with grades available.")
            return

        top_student_name = max(
            averages.items(),
            key=lambda item: item[1]
        )[0]

        top_avg = averages[top_student_name]
        print(f"The student with the highest average is {top_student_name} with a grade of {top_avg:.1f}.")

def get_user_grades() -> List[float]:
    grades = []
    print("Enter a grade (or 'done' to finish): ")

    while True:
        try:
            line = input().strip()
            if not line:
                break
            if line.lower() == "done":
                break

            grade = float(line)
            if 0<= grade <= 100:
                grades.append(grade)
            else:
                print("Invalid grade.")

        except ValueError:
            print("Invalid number! Please enter a valid number.")

    return grades

def main() -> None:
    manager = StudentManager()

    actions: Dict[str, Callable[[], bool]] = {
        "1": lambda: (
            manager.add_new_student(input("Enter student name: ").strip())
            or True
        ),
        "2": lambda: (
            manager.add_grades_for_student(
                input("Enter student name: ").strip(),
                get_user_grades()
            ) or True
        ),
        "3": lambda: (manager.show_report() or True),
        "4": lambda: (manager.find_top_performer() or True),
        "5": lambda: False
    }

    while True:
        print("\n--- Student Grade Analyzer ---")

        for key, description in MENU_OPTIONS.items():
            print(f"{key}. {description}")

        try:
            choice = input("\nEnter your choice: ").strip()

            action = actions.get(choice)
            if action:
                if not action():
                    print("Bye!")
                    break

            else:
                print("Invalid choice. Please enter a number.")

        except KeyboardInterrupt:
            print("\n\nProgram interrupted.")
            sys.exit(0)
        except EOFError:
            print("\n\nProgram ended.")
            sys.exit(0)
        except Exception as error:
            print(f"Unexpected error: {error}")

if __name__ == "__main__":
    main()