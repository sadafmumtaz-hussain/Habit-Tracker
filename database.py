import sqlite3


def create_database():
    connection = sqlite3.connect("habits.db")

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            periodicity TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS completions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_id INTEGER NOT NULL,
            completion_date TEXT NOT NULL,
            FOREIGN KEY (habit_id) REFERENCES habits(id)
        )
    """)

    connection.commit()
    connection.close()


def save_habit(name, periodicity):
    connection = sqlite3.connect("habits.db")

    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO habits (name, periodicity) VALUES (?, ?)",
        (name, periodicity)
    )

    habit_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return habit_id


def save_completion(habit_id, completion_date):
    connection = sqlite3.connect("habits.db")

    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO completions (habit_id, completion_date) VALUES (?, ?)",
        (habit_id, completion_date)
    )

    connection.commit()
    connection.close()


def load_habits():
    connection = sqlite3.connect("habits.db")

    cursor = connection.cursor()

    cursor.execute(
        "SELECT id, name, periodicity FROM habits"
    )

    habits = cursor.fetchall()

    connection.close()

    return habits


def load_completions(habit_id):
    connection = sqlite3.connect("habits.db")

    cursor = connection.cursor()

    cursor.execute(
        "SELECT completion_date FROM completions WHERE habit_id = ?",
        (habit_id,)
    )

    completions = cursor.fetchall()

    connection.close()

    return completions


def load_habit_objects():
    from habit import Habit
    from datetime import date

    habit_rows = load_habits()

    habit_objects = []

    for habit_id, name, periodicity in habit_rows:
        completion_rows = load_completions(habit_id)

        completion_history = []

        for row in completion_rows:
            completion_history.append(
                date.fromisoformat(row[0])
            )

        habit = Habit(
            name,
            periodicity,
            habit_id,
            completion_history
        )

        habit_objects.append(habit)

    return habit_objects

def delete_habit(habit_id):
    connection = sqlite3.connect("habits.db")

    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM completions WHERE habit_id = ?",
        (habit_id,)
    )

    cursor.execute(
         "DELETE FROM habits WHERE id = ?",
         (habit_id,)
    )

    connection.commit()
    connection.close()

