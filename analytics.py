
from datetime import date, timedelta


def get_completed_periods(completion_history, periodicity):
    """Return unique daily dates or weekly periods."""
    dates = set(completion_history)

    if periodicity == "daily":
        return dates

    if periodicity == "weekly":
        return {
            (day.isocalendar().year, day.isocalendar().week)
            for day in dates
        }

    raise ValueError("Periodicity must be daily or weekly")


def periods_are_consecutive(previous, current, periodicity):
    """Check whether two completed periods are consecutive."""
    if periodicity == "daily":
        return previous + timedelta(days=1) == current

    previous_year, previous_week = previous
    current_year, current_week = current

    if previous_year == current_year:
        return current_week == previous_week + 1

    return (
        current_year == previous_year + 1
        and previous_week == date(previous_year, 12, 28).isocalendar().week
        and current_week == 1
    )


def calculate_longest_streak(completion_history, periodicity="daily"):
    periods = sorted(
        get_completed_periods(completion_history, periodicity)
    )

    if not periods:
        return 0

    longest = 1
    streak = 1

    for previous, current in zip(periods, periods[1:]):
        if periods_are_consecutive(previous, current, periodicity):
            streak += 1
        else:
            streak = 1

        longest = max(longest, streak)

    return longest


def calculate_current_streak(completion_history, periodicity="daily"):
    periods = sorted(
        get_completed_periods(completion_history, periodicity)
    )

    if not periods:
        return 0

    today = date.today()

    if periodicity == "daily":
        if periods[-1] != today:
            return 0
    else:
        current_week = (today.isocalendar().year, today.isocalendar().week)
        if periods[-1] != current_week:
            return 0

    streak = 1

    for previous, current in zip(reversed(periods[:-1]), reversed(periods[1:])):
        if periods_are_consecutive(previous, current, periodicity):
            streak += 1
        else:
            break

    return streak


def filter_habits_by_periodicity(habits, periodicity):
    """Return habits matching daily or weekly periodicity."""
    if periodicity not in ("daily", "weekly"):
        raise ValueError("Periodicity must be daily or weekly")

    return [
        habit for habit in habits
        if habit.periodicity == periodicity
    ]


def longest_streak_across_habits(habits):
    """Return the longest streak and its habit."""
    if not habits:
        return 0, None

    results = [
        (
            calculate_longest_streak(
                habit.completion_history,
                habit.periodicity,
            ),
            habit,
        )
        for habit in habits
    ]

    return max(results, key=lambda result: result[0])


def longest_streak_for_habit(habits, habit_id):
    """Return the longest streak for a selected habit ID."""
    for habit in habits:
        if habit.id == habit_id:
            return calculate_longest_streak(
                habit.completion_history,
                habit.periodicity,
            )

    return None
