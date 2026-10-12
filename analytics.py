from datetime import timedelta


def calculate_longest_streak(completion_history):
    if not completion_history:
        return 0

    dates = sorted(completion_history)

    streak = 1
    longest_streak = 1

    for i in range(len(dates) - 1):
        current_date = dates[i]
        next_date = dates[i + 1]

        if current_date + timedelta(days=1) == next_date:
            streak = streak + 1
        else:
            streak = 1

        if streak > longest_streak:
            longest_streak = streak

    return longest_streak


def calculate_current_streak(completion_history):
    if not completion_history:
        return 0
    dates = sorted(completion_history)

    streak = 1

    for i in range(len(dates) - 1):
        current_date = dates[i]
        next_date = dates[i + 1]

        if current_date + timedelta(days=1) == next_date:
            streak = streak + 1
        else:
            streak = 1

    return streak
