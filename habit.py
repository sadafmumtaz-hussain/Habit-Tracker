
from datetime import date, datetime

from database import save_completion


class Habit:
    def __init__(
        self,
        name,
        periodicity,
        habit_id=None,
        completion_history=None,
        created_at=None,
    ):
        self.id = habit_id
        self.name = name
        self.periodicity = periodicity
        self.created_at = created_at or datetime.now().isoformat()

        if completion_history is None:
            self.completion_history = []
        else:
            self.completion_history = completion_history

    def complete(self):
        today = date.today()

        if today not in self.completion_history:
            self.completion_history.append(today)

            if self.id is not None:
                save_completion(self.id, today.isoformat())
