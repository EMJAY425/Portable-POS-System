class GradeCalculator:
    def __init__(self, student_name):
        self.student_name = student_name
        self.scores = []

    def add_score(self, score):
        self.scores.append(score)

    def calculate_average(self):
        if not self.scores:
            return 0
        return sum(self.scores) / len(self.scores)

    def get_decimal_grade(self, average):
        if average >= 98:
            return 1.0
        elif average >= 95:
            return 1.25
        elif average >= 92:
            return 1.5
        elif average >= 89:
            return 1.75
        elif average >= 86:
            return 2.0
        elif average >= 83:
            return 2.25
        elif average >= 80:
            return 2.5
        elif average >= 77:
            return 2.75
        elif average >= 75:
            return 3.0
        else:
            return 5.0

def main():
    name = input("Enter Student Name: ")

    student_portal = GradeCalculator(name)

    for i in range(1, 7):
        while True:
            try:
                score_input = float(input(f"Subject {i} Score: "))
                # Validation: Ensure score is between 0 and 100
                if 0 <= score_input <= 100:
                    student_portal.add_score(score_input)
                    break
                else:
                    print("Invalid input. Please enter a score between 0 and 100.")
            except ValueError:
                print("Invalid input. Please enter a numerical value.")

    avg = student_portal.calculate_average()
    decimal_grade = student_portal.get_decimal_grade(avg)

    # Final Report
    print("\n" + "=" * 35)
    print(f"STUDENT REPORT: {student_portal.student_name}")
    print(f"AVERAGE SCORE:  {avg:.2f}%")
    print(f"COLLEGE GRADE:  {decimal_grade}")
    print("=" * 35)

if __name__ == "__main__":
    main()