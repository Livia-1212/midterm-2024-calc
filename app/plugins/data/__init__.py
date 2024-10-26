import logging
import os
import pandas as pd
from app.commands import Command

class DataCommand(Command):
    def __init__(self, calculator):
        self.calculator = calculator

    def execute(self):
        categories = ('assignment', 'project', 'midterm', 'finals')
        classes = ['class1', 'class2']
        grades_list = []

        print("\n📊 Enter grades for each category and class.")
        
        for cls in classes:
            print(f"\n📚 Entering grades for {cls}:")
            
            for category in categories:
                while True:
                    try:
                        grade_input = input(f"Enter {category} grade: ")
                        
                        if grade_input == "":
                            print("⚠️ No input provided; skipping this entry.")
                            break

                        grade = float(grade_input)

                        if grade < 0:
                            print(f"❌ Error: Negative grades are not allowed for {category}.")
                            break

                        grades_list.append(grade)
                        break
                    
                    except ValueError:
                        print("❌ Error: Please enter a valid positive number.")

        # Update calculator values
        if grades_list:
            self.calculator.values.extend(grades_list)
            print("\n✅ Grades added to the calculator.")
        else:
            print("\n⚠️ No valid grades were added.")

    def export_grades_to_csv(self):
        """Exports collected grades to a CSV file."""
        if not self.calculator.values:
            print("⚠️ No grades to export.")
            return

        data_dir = './data'
        
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
            logging.info(f"The directory '{data_dir}' was created.")

        csv_file_path = os.path.join(data_dir, 'grades_export.csv')
        df_grades = pd.DataFrame(self.calculator.values, columns=['Grade'])
        df_grades.to_csv(csv_file_path, index=False)
        logging.info(f"Grades saved to CSV at '{csv_file_path}'.")
        print(f"\n📁 Grades saved to '{csv_file_path}'.")
