# Habit Tracker

## 1. Project Overview

Habit Tracker is a command-line application developed in Python for the Object Oriented and Functional Programming with Python (DLBDSOOFPP01) course at IU International University of Applied Sciences.

The application allows users to create habits, record completions, view saved habits, analyse streaks, and delete habits. It uses object-oriented programming, SQLite database persistence, and functional-style analytics.

## 2. Technologies Used

- **Python 3** — application logic and command-line interface
- **SQLite** — persistent storage through Python's built-in `sqlite3` module
- **pytest** — automated testing
- **Git and GitHub** — version control and project hosting

## 3. Current Features

- Create habits with a name and daily or weekly periodicity.
- Display saved habits and their IDs.
- Record habit completions.
- Prevent duplicate completion dates within a Habit object.
- Store habits and completion dates in SQLite.
- Delete habits and their associated completion records.
- Calculate current and longest consecutive-date streaks.
- Run automated tests with pytest.

## 4. Installation

**Prerequisite:** Python 3.

Clone or download this repository and open a terminal in the project directory.

To install pytest for running the tests:

```bash
python -m pip install pytest
```

The application uses Python's built-in `sqlite3` module, so no separate SQLite installation is required.

## 5. Running the Application

Run:

```bash
python main.py
```

Follow the numbered menu to create, list, complete, analyse, or delete habits.

## 6. Running the Tests

Run the test suite with:

```bash
python -m pytest
```

At the initial development checkpoint, six tests passed. The final test results will be updated after the remaining functionality and tests are completed.

## 7. Project Structure

```text
HabitTracker/
├── main.py
├── habit.py
├── analytics.py
├── database.py
├── cli.py
├── .gitignore
└── tests/
    └── test_habit.py
```

## 8. Database and Persistence

The application uses SQLite to store habits and their completion dates. The database schema contains a `habits` table and a `completions` table. The local database file is excluded from version control.

## 9. Remaining Development Work

The following requirements must be implemented and verified before the final release:

- Period-based streak calculations for daily and weekly habits.
- Correct handling of missed periods and multiple completions within one period.
- Five predefined habits with four weeks of example tracking data.
- Habit creation date and time.
- Required analytics for periodicity filtering, the longest streak across all habits, and the longest streak for a selected habit.
- Expanded automated tests for analytics, database operations, and periodicity rules.

## 10. Author and Course

**Author:** Sadaf Hussain

**Course:** Object Oriented and Functional Programming with Python (DLBDSOOFPP01)

**Repository:** https://github.com/sadafmumtaz-hussain/Habit-Tracker

---

*This documentation will be updated as the remaining requirements are implemented and tested.*
