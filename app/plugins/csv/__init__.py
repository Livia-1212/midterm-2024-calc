import logging
import os
from app.commands import Command
import pandas as pd

class CsvCommand(Command):
    def __init__(self, calculator):
        self.calculator = calculator

    def execute(self):
        data_dir = './data'
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
            logging.info(f"The directory '{data_dir}' was created.")
        elif not os.access(data_dir, os.W_OK):
            logging.error(f"The directory '{data_dir}' is not writable.")
            return

        # Example dictionary for grades (updated content)
        grades_dict = {
            'class1_assignment': 85,
            'class1_project': 90,
            'class1_midterm': 78,
            'class1_final': 88,
            'class2_assignment': 82,
            'class2_project': 89,
            'class2_midterm': 76,
            'class2_final': 92
        }

        # Convert dictionary to DataFrame and save to CSV
        df_grades = pd.DataFrame(list(grades_dict.items()), columns=['Category', 'Grade'])
        csv_file_path = os.path.join(data_dir, 'grades_export.csv')
        df_grades.to_csv(csv_file_path, index=False)
        logging.info(f"Grades saved to CSV at '{csv_file_path}'.")

        # Only update calculator if grades are found
        if not df_grades.empty:
            self.calculator.values.extend(df_grades['Grade'].tolist())
            print("\n📊 Added grades from CSV for statistical calculations. Use 'mean', 'median', or 'standard_deviation' to analyze.")
        else:
            logging.warning("No grades found to add to the calculator.")
