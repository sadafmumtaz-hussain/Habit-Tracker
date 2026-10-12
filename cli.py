
def show_menu():
    print()
    print("========================")
    print("      HABIT TRACKER")
    print("========================")
    print("1. Create habit")
    print("2. Show habits")
    print("3. Complete habit")
    print("4. Analyse habits")
    print("5. Delete habit")
    print("6. Exit")

    return input("Choose an option: ").strip()


def show_habits(habits):
    print()
    print("Current habits:")

    if not habits:
        print("No habits found.")
        return

    for habit in habits:
        print(
            habit.id,
            ".",
            habit.name,
            "-",
            habit.periodicity,
            "- Created:",
            habit.created_at,
        )
