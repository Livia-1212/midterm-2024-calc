# Midterm-2024-Calc

## Table of Contents
- [Introduction](#introduction)
- [Design Pattern Rationale](#design-pattern-rationale)
  - [Command Design Pattern](#command-design-pattern)
  - [Dynamic Plugin Loading](#dynamic-plugin-loading)
  - [Pandas for History Management](#pandas-for-history-management)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
  - [REPL Interface](#repl-interface)
  - [Available Commands](#available-commands)
- [Example Usage](#example-usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction
This project is a command-line calculator with support for basic arithmetic and statistical operations. It is designed with modularity and flexibility in mind, using the **Command Design Pattern** to allow for dynamic loading of plugins and easy addition of new commands. The application tracks the history of operations using **Pandas** and allows users to reset the calculator while preserving the history.

## Design Pattern Rationale

### Command Design Pattern
The **Command Design Pattern** is employed as the core architectural design of this project. It allows each operation (e.g., addition, subtraction, greet, data commands) to be encapsulated as a command object. Here’s why the **Command Design Pattern** is suitable for this project:
- **Encapsulation**: Each command is represented by its own class (e.g., `AddCommand`, `DataCommand`), encapsulating its behavior.
- **Extensibility**: New commands can be easily added without altering existing code. This adheres to the **Open-Closed Principle**, a key principle of SOLID design.
- **Command Management**: Commands are registered in a `CommandHandler`, which manages their execution, ensuring a consistent interface for invoking commands.
- **Undo Functionality**: Although not implemented here, the command pattern can be extended to include an "undo" mechanism, making it flexible for future enhancements.

### Dynamic Plugin Loading
The project also employs **dynamic plugin loading** to scan and import available plugins at runtime using the `pkgutil` and `importlib` modules. This approach provides:
- **Modularity**: Each plugin resides in its own folder under the `app/plugins` directory, making it easy to manage and extend.
- **Ease of Maintenance**: Plugins can be added or modified independently without affecting the main application logic.
- **Automatic Registration**: The `App` class automatically discovers and registers commands from each plugin, promoting clean code separation and loose coupling.

### Pandas for History Management
The project uses **Pandas** for efficient management of the calculator’s operation history. The benefits include:
- **Structured Storage**: The history of operations is stored in a Pandas DataFrame, providing a structured way to manage and analyze the data.
- **Persistence**: The operation history is saved to a CSV file when the user exits the REPL, enabling data persistence across sessions.
- **Data Analysis**: Pandas makes it easy to implement statistical commands (mean, median, etc.) and analyze operation history in a straightforward manner.

## Project Structure
Midterm-2024-Calc\
> app \
>> commands \
>>> init.py \

>> plugins \
>>> plugins/calc \
>>>> init.py \
>>>> calculator.py

>>> plugins/data \
>>>> init.py \

>>> plugins/csv \
>>>> init.py

>>> plugins/greet \
>>>> init.py \

>>> plugins/logging_config \
>>>> init.py \

>>> plugins/mean \
>>>> init.py

>>> plugins/median \
>>>> init.py

>>> plugins/mode \
>>>> init.py

>>> plugins/standard_deviation \
>>>> init.py

>> app/init.py \

> data \
>> data/gpt_states.csv 
>> data/states.csv 
>> data/calculation_history.csv
>> data/states.csv

> tests \
>> tests/init.py \
>> tests/conftest.py \
>> tests/test_app.py \
>> tests/test_plugin_greet.py \


>  main.py \
> README.md \
> requirements.txt \
> .gitignore



### 📝 **Explanation**
- **app**: Contains the main application logic, commands, and plugins for dynamic operations.
- **app/plugins**: Contains modular plugins like `calc`, `data`, `mean`, etc., which encapsulate specific functionalities.
- **data**: Stores CSV files for operation history and other data.
- **tests**: Contains test files for ensuring application correctness and stability.
- **main.py**: Entry point of the application.
- **README.md**: Documentation of the project.
- **requirements.txt**: Lists project dependencies.

## Setup Instructions
1. Clone the repository: git clone https://github.com/Livia-1212/midterm-2024-calc.git
2. Navigate to the project directory: cd Midterm-2024-Calc
3. Install the dependencies: pip install -r requirements.txt
4. Run the application: python3 main.py

## License
This project is licensed under the MIT License.