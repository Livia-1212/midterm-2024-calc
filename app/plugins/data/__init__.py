import logging
import os
from app.commands import Command

class DataCommand(Command):
    def __init__(self, calculator):
        self.calculator = calculator

    def execute(self):
        categories = ('assignment', 'project', 'midterm', 'finals')
        classes = ['class1', 'class2']
        all_grades = {}  # To store grades by class
        grades_list = []  # To store overall grades as list

        print("\n📊 Enter grades for each category and class.")

        # Collect grades for each class
        for cls in classes:
            grades_tuple = []  # Tuple for current class
            print(f"\n📚 Entering grades for {cls}:")

            # Collect grades for each category in the current class
            for category in categories:
                while True:
                    try:
                        grade = float(input(f"Enter {category} grade: "))
                        grades_tuple.append(grade)
                        break
                    except ValueError:
                        print("❌ Error: Please enter a valid number.")

            # Convert to tuple and store in list and dictionary
            grades_tuple = tuple(grades_tuple)
            grades_list.extend(grades_tuple)
            all_grades[cls] = grades_tuple

        # Log collected grades
        logging.info(f"Grades List: {grades_list}")
        logging.info(f"Grades by Class: {all_grades}")
        print(f"\n✅ Grades collected:\nList: {grades_list}\nClasses: {all_grades}")

        # Update calculator values
        self.calculator.values.extend(grades_list)

        # Save grades to CSV
        self.export_grades_to_csv(grades_list)

        print("\n📊 You can now use 'mean', 'median', or 'standard_deviation' commands on the collected grades.")

    def export_grades_to_csv(self, grades_list):
        import pandas as pd
        data_dir = './data'
        
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
            logging.info(f"The directory '{data_dir}' was created.")

        csv_file_path = os.path.join(data_dir, 'grades_export.csv')
        df_grades = pd.DataFrame(grades_list, columns=['Grade'])
        df_grades.to_csv(csv_file_path, index=False)
        logging.info(f"Grades saved to CSV at '{csv_file_path}'.")
        print(f"\n📁 Grades saved to '{csv_file_path}'.")
