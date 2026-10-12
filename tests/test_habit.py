from datetime import date, timedelta

from habit import Habit
from analytics import (
    calculate_current_streak,
    calculate_longest_streak
)


def test_create_habit():
    habit = Habit("Reading", "weekly")

    assert habit.name == "Reading"
    assert habit.periodicity == "weekly"
    assert habit.completion_history == []


def test_complete_habit():
    habit = Habit("Reading", "daily")

    assert habit.completion_history == []

    habit.complete()

    assert len(habit.completion_history) == 1


def test_duplicate_completion():
    habit = Habit("Reading", "daily")

    habit.complete()
    habit.complete()

    assert len(habit.completion_history) == 1


def test_longest_streak():
    today = date.today()

    completion_history = [
        today - timedelta(days=3),
        today - timedelta(days=2),
        today - timedelta(days=1),
        today
    ]

    result = calculate_longest_streak(completion_history)

    assert result == 4


def test_current_streak():
    today = date.today()

    completion_history = [
        today - timedelta(days=2),
        today - timedelta(days=1),
        today
    ]

    result = calculate_current_streak(completion_history)

    assert result == 3


def test_empty_history():
    assert calculate_current_streak([]) == 0
    assert calculate_longest_streak([]) == 0
    