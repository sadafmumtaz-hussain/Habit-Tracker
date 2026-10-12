
from datetime import date, timedelta

from habit import Habit
from analytics import (
    calculate_current_streak,
    calculate_longest_streak,
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


def test_longest_daily_streak():
    today = date.today()

    history = [
        today - timedelta(days=3),
        today - timedelta(days=2),
        today - timedelta(days=1),
        today,
    ]

    assert calculate_longest_streak(history, "daily") == 4


def test_current_daily_streak():
    today = date.today()

    history = [
        today - timedelta(days=2),
        today - timedelta(days=1),
        today,
    ]

    assert calculate_current_streak(history, "daily") == 3


def test_empty_history():
    assert calculate_current_streak([], "daily") == 0
    assert calculate_longest_streak([], "daily") == 0
    assert calculate_current_streak([], "weekly") == 0
    assert calculate_longest_streak([], "weekly") == 0


def test_weekly_streak():
    today = date.today()

    history = [
        today - timedelta(weeks=3),
        today - timedelta(weeks=2),
        today - timedelta(weeks=1),
        today,
    ]

    assert calculate_longest_streak(history, "weekly") == 4


def test_multiple_completions_in_one_week_count_once():
    today = date.today()

    history = [
        today - timedelta(weeks=1),
        today - timedelta(weeks=1) + timedelta(days=1),
        today,
    ]

    assert calculate_longest_streak(history, "weekly") == 2


def test_missed_week_breaks_streak():
    today = date.today()

    history = [
        today - timedelta(weeks=3),
        today - timedelta(weeks=1),
        today,
    ]

    assert calculate_longest_streak(history, "weekly") == 2


def test_invalid_periodicity():
    try:
        calculate_longest_streak([date.today()], "monthly")
    except ValueError:
        return

    assert False, "Expected ValueError for invalid periodicity"

from analytics import (
    filter_habits_by_periodicity,
    longest_streak_across_habits,
    longest_streak_for_habit,
)


def test_filter_habits_by_periodicity():
    daily_habit = Habit("Reading", "daily")
    weekly_habit = Habit("Cleaning", "weekly")

    result = filter_habits_by_periodicity(
        [daily_habit, weekly_habit], "weekly"
    )

    assert len(result) == 1
    assert result[0].name == "Cleaning"


def test_longest_streak_for_selected_habit():
    from datetime import date, timedelta

    today = date.today()
    habit = Habit(
        "Reading",
        "daily",
        habit_id=1,
        completion_history=[
            today - timedelta(days=2),
            today - timedelta(days=1),
            today,
        ],
    )

    result = longest_streak_for_habit([habit], 1)

    assert result == 3


def test_longest_streak_across_habits():
    from datetime import date, timedelta

    today = date.today()

    habit_one = Habit(
        "Reading",
        "daily",
        habit_id=1,
        completion_history=[
            today - timedelta(days=1),
            today,
        ],
    )

    habit_two = Habit(
        "Exercise",
        "daily",
        habit_id=2,
        completion_history=[
            today - timedelta(days=3),
            today - timedelta(days=2),
            today - timedelta(days=1),
            today,
        ],
    )

    longest, habit = longest_streak_across_habits(
        [habit_one, habit_two]
    )

    assert longest == 4
    assert habit.name == "Exercise"
