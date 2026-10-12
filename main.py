from database import (
    create_database,
    load_habit_objects,
    save_habit,
    delete_habit
)

from cli import show_menu, show_habits

from analytics import (
    calculate_current_streak,
    calculate_longest_streak
)


def main():
    create_database()

    habits = load_habit_objects()

    running = True

    while running:
        choice = show_menu()

        print("You entered:", choice)

        if choice == "1":
            name = input("Enter habit name: ")
            periodicity = input("Enter periodicity (daily/weekly): ")

            habit_id = save_habit(name, periodicity)

            print("Habit created successfully.")
            print("Habit ID:", habit_id)

            habits = load_habit_objects()

        elif choice == "2":
            show_habits(habits)

            input("\nPress Enter to return to the main menu...")

        elif choice == "3":
            habit_id = int(input("Enter habit ID to complete: "))

            for habit in habits:
                if habit.id == habit_id:
                    habit.complete()
                    print("Habit completed successfully.")
                    break
            else:
                print("Habit not found.")

            habits = load_habit_objects()

        elif choice == "4":
            for habit in habits:
                current_streak = calculate_current_streak(
                    habit.completion_history
                )

                longest_streak = calculate_longest_streak(
                    habit.completion_history
                )

                print()
                print(habit.id, ".", habit.name)
                print("Current streak:", current_streak)
                print("Longest streak:", longest_streak)

            input("\nPress Enter to return to the main menu...")

        elif choice == "5":
            habit_id = int(input("Enter habit ID to delete: "))

            delete_habit(habit_id)

            print("Habit deleted successfully.")

            habits = load_habit_objects()

        elif choice == "6":
            print("Goodbye!")
            running = False

        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()

    