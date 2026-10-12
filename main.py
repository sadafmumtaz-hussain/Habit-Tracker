
from database import (
    create_database,
    seed_sample_habits,
    load_habit_objects,
    save_habit,
    delete_habit,
)

from cli import show_menu, show_habits

from analytics import (
    calculate_current_streak,
    calculate_longest_streak,
    filter_habits_by_periodicity,
    longest_streak_across_habits,
    longest_streak_for_habit,
)


def analyse_habits(habits):
    if not habits:
        print("No habits found.")
        return

    for habit in habits:
        current = calculate_current_streak(
            habit.completion_history, habit.periodicity
        )
        longest = calculate_longest_streak(
            habit.completion_history, habit.periodicity
        )

        print(f"\n{habit.id}. {habit.name}")
        print("Periodicity:", habit.periodicity)
        print("Created:", habit.created_at)
        print("Current streak:", current)
        print("Longest streak:", longest)


def main():
    create_database()
    seed_sample_habits()
    habits = load_habit_objects()

    while True:
        print("\n===== HABIT TRACKER =====")
        print("1. Create habit")
        print("2. Show habits")
        print("3. Complete habit")
        print("4. Analyse all habits")
        print("5. Delete habit")
        print("6. Filter habits by periodicity")
        print("7. Longest streak across all habits")
        print("8. Longest streak for one habit")
        print("9. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            name = input("Enter habit name: ").strip()
            periodicity = input(
                "Enter periodicity (daily/weekly): "
            ).strip().lower()

            if not name:
                print("Habit name cannot be empty.")
            elif periodicity not in ("daily", "weekly"):
                print("Periodicity must be daily or weekly.")
            else:
                habit_id = save_habit(name, periodicity)
                print("Habit created. ID:", habit_id)

            habits = load_habit_objects()

        elif choice == "2":
            show_habits(habits)

        elif choice == "3":
            try:
                habit_id = int(input("Enter habit ID to complete: "))
                selected = next(
                    (h for h in habits if h.id == habit_id), None
                )

                if selected is None:
                    print("Habit not found.")
                elif date_already_completed(selected):
                    print("This habit is already completed today.")
                else:
                    selected.complete()
                    print("Habit completed successfully.")

                habits = load_habit_objects()

            except ValueError:
                print("Enter a valid numeric habit ID.")

        elif choice == "4":
            analyse_habits(habits)

        elif choice == "5":
            try:
                habit_id = int(input("Enter habit ID to delete: "))

                if any(h.id == habit_id for h in habits):
                    delete_habit(habit_id)
                    print("Habit deleted.")
                    habits = load_habit_objects()
                else:
                    print("Habit not found.")

            except ValueError:
                print("Enter a valid numeric habit ID.")

        elif choice == "6":
            periodicity = input(
                "Filter by daily or weekly: "
            ).strip().lower()

            try:
                filtered = filter_habits_by_periodicity(
                    habits, periodicity
                )
                show_habits(filtered)
            except ValueError as error:
                print(error)

        elif choice == "7":
            longest, habit = longest_streak_across_habits(habits)

            if habit is None:
                print("No habits found.")
            else:
                print(
                    f"Longest streak: {longest} periods "
                    f"({habit.name}, {habit.periodicity})"
                )

        elif choice == "8":
            try:
                habit_id = int(
                    input("Enter habit ID to analyse: ")
                )
                longest = longest_streak_for_habit(habits, habit_id)

                if longest is None:
                    print("Habit not found.")
                else:
                    print("Longest streak:", longest)

            except ValueError:
                print("Enter a valid numeric habit ID.")

        elif choice == "9":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Choose 1–9.")


def date_already_completed(habit):
    from datetime import date
    return date.today() in habit.completion_history


if __name__ == "__main__":
    main()
