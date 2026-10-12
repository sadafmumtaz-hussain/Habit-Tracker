
import sqlite3
from datetime import date, timedelta, datetime


DATABASE_NAME = "habits.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def create_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            periodicity TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
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

    # Migrate existing databases without deleting saved habits.
    cursor.execute("PRAGMA table_info(habits)")
    columns = [column[1] for column in cursor.fetchall()]

    if "created_at" not in columns:
        cursor.execute(
            "ALTER TABLE habits ADD COLUMN created_at TEXT"
        )

    cursor.execute("""
        UPDATE habits
        SET created_at = ?
        WHERE created_at IS NULL
    """, (datetime.now().isoformat(timespec="seconds"),))

    # Prevent duplicate completion dates for the same habit.
    cursor.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS
        unique_habit_completion
        ON completions (habit_id, completion_date)
    """)

    connection.commit()
    connection.close()


def seed_sample_habits():
    sample_habits = [
        ("Reading", "daily"),
        ("Exercise", "daily"),
        ("Drink Water", "daily"),
        ("Clean Apartment", "weekly"),
        ("Plan the Week", "weekly"),
    ]

    connection = get_connection()
    cursor = connection.cursor()

    for name, periodicity in sample_habits:
        cursor.execute("""
            SELECT id FROM habits
            WHERE name = ? AND periodicity = ?
        """, (name, periodicity))

        result = cursor.fetchone()

        if result is None:
            cursor.execute("""
                INSERT INTO habits (name, periodicity, created_at)
                VALUES (?, ?, ?)
            """, (
                name,
                periodicity,
                datetime.now().isoformat(timespec="seconds"),
            ))
            habit_id = cursor.lastrowid
        else:
            habit_id = result[0]

        # Four weeks of example completions.
        for weeks_ago in range(4, 0, -1):
            sample_date = date.today() - timedelta(
                weeks=weeks_ago
            )

            cursor.execute("""
                INSERT OR IGNORE INTO completions
                (habit_id, completion_date)
                VALUES (?, ?)
            """, (habit_id, sample_date.isoformat()))

    connection.commit()
    connection.close()


def save_habit(name, periodicity):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO habits (name, periodicity, created_at)
        VALUES (?, ?, ?)
    """, (
        name,
        periodicity,
        datetime.now().isoformat(timespec="seconds"),
    ))

    habit_id = cursor.lastrowid
    connection.commit()
    connection.close()

    return habit_id


def save_completion(habit_id, completion_date):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO completions
        (habit_id, completion_date)
        VALUES (?, ?)
    """, (habit_id, completion_date))

    connection.commit()
    connection.close()


def load_habits():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, name, periodicity, created_at
        FROM habits
        ORDER BY id
    """)

    habits = cursor.fetchall()
    connection.close()

    return habits


def load_completions(habit_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT completion_date
        FROM completions
        WHERE habit_id = ?
        ORDER BY completion_date
    """, (habit_id,))

    completions = cursor.fetchall()
    connection.close()

    return completions


def load_habit_objects():
    from habit import Habit

    habit_objects = []

    for habit_id, name, periodicity, created_at in load_habits():
        completion_rows = load_completions(habit_id)

        completion_history = [
            date.fromisoformat(row[0])
            for row in completion_rows
        ]

        habit = Habit(
            name=name,
            periodicity=periodicity,
            habit_id=habit_id,
            completion_history=completion_history,
            created_at=created_at,
        )

        habit_objects.append(habit)

    return habit_objects


def delete_habit(habit_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM completions WHERE habit_id = ?",
        (habit_id,),
    )
    cursor.execute(
        "DELETE FROM habits WHERE id = ?",
        (habit_id,),
    )

    connection.commit()
    connection.close()
