"""
Smart Study Planner
--------------------
A console-based programme that helps a student log, review and analyse
their study sessions across different subjects over a semester.

Data persists between runs by saving to/loading from 'study_log.txt'.
"""

import os

DATA_FILE = "study_log.txt"
DELIMITER = "|"  # used to separate fields when saving/loading sessions


# (c) classify_session
def classify_session(duration):
    """Classify a session's duration (in minutes) as Short, Medium or Long."""
    if duration < 30:
        return "Short"
    elif duration <= 90:
        return "Medium"
    else:
        return "Long"

# (g) save_sessions / load_sessions
def save_sessions(sessions):
    """Save every session to DATA_FILE, one session per line."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        for s in sessions:
            # Join fields with the delimiter; duration stored as a plain number
            line = DELIMITER.join([s["subject"], s["topic"], s["date"], str(s["duration"])])
            f.write(line + "\n")
    print(f"Sessions saved to {DATA_FILE}.")


def load_sessions():
    """Load sessions from DATA_FILE if it exists; otherwise start with an empty list."""
    sessions = []
    if not os.path.exists(DATA_FILE):
        # First run - no file yet, so just return an empty list (no crash)
        return sessions

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(DELIMITER)
                if len(parts) != 4:
                    continue  # skip any malformed line rather than crashing
                subject, topic, date, duration_str = parts
                try:
                    duration = float(duration_str)
                except ValueError:
                    continue  # skip lines with a corrupted duration value
                sessions.append({
                    "subject": subject,
                    "topic": topic,
                    "date": date,
                    "duration": duration
                })
    except OSError as e:
        print(f"Warning: could not read {DATA_FILE} ({e}). Starting with no sessions.")

    return sessions

# (b) add_session
def add_session(sessions):
    """Prompt the user for session details and append a new session dict to the list."""
    subject = input("Enter subject name: ").strip()
    topic = input("Enter topic covered: ").strip()
    date = input("Enter date/day label (e.g. 2026-09-01 or Monday): ").strip()

    # Keep re-prompting until a valid positive number is entered
    duration = None
    while duration is None:
        raw = input("Enter duration in minutes: ").strip()
        try:
            value = float(raw)
            if value <= 0:
                print("Duration must be a positive number. Please try again.")
            else:
                duration = value
        except ValueError:
            print("That's not a valid number. Please try again.")

    session = {
        "subject": subject,
        "topic": topic,
        "date": date,
        "duration": duration
    }
    sessions.append(session)
    print(f"Session added: {subject} ({classify_session(duration)}, {duration:.0f} min)\n")

# (d) view_sessions
def view_sessions(sessions):
    """Display every logged session in a neatly formatted table."""
    if not sessions:
        print("\nNo sessions logged yet.\n")
        return

    header = f"{'#':<4}{'Subject':<15}{'Topic':<20}{'Date':<15}{'Duration':<10}{'Type':<8}"
    print("\n" + header)
    print("-" * len(header))
    for i, s in enumerate(sessions, start=1):
        classification = classify_session(s["duration"])
        print(f"{i:<4}{s['subject']:<15}{s['topic']:<20}{s['date']:<15}"
              f"{s['duration']:<10.0f}{classification:<8}")
    print()

# (e) search_by_subject
def search_by_subject(sessions):
    """Search for sessions by subject name (case-insensitive) and show a total."""
    query = input("Enter subject to search for: ").strip().lower()

    matches = [s for s in sessions if s["subject"].lower() == query]

    if not matches:
        print(f"\nNo sessions found for subject '{query}'.\n")
        return

    header = f"{'Topic':<20}{'Date':<15}{'Duration':<10}{'Type':<8}"
    print(f"\nSessions for '{matches[0]['subject']}':")
    print(header)
    print("-" * len(header))
    total = 0
    for s in matches:
        classification = classify_session(s["duration"])
        print(f"{s['topic']:<20}{s['date']:<15}{s['duration']:<10.0f}{classification:<8}")
        total += s["duration"]

    print(f"\nTotal time spent on {matches[0]['subject']}: {total:.0f} minutes "
          f"({total / 60:.2f} hours)\n")

# (f) study_statistics
def study_statistics(sessions):
    """Compute and display overall and per-subject study statistics."""
    if not sessions:
        print("\nNo sessions logged yet - no statistics to show.\n")
        return

    total_minutes = sum(s["duration"] for s in sessions)

    # Build per-subject totals
    subject_totals = {}
    for s in sessions:
        subject_totals[s["subject"]] = subject_totals.get(s["subject"], 0) + s["duration"]

    weakest_subject = min(subject_totals, key=subject_totals.get)
    longest_session = max(sessions, key=lambda s: s["duration"])

    print("\n--- Study Statistics ---")
    print(f"Total hours studied overall: {total_minutes / 60:.2f} hours\n")

    print("Hours studied per subject:")
    for subject, minutes in subject_totals.items():
        print(f"  {subject:<15}{minutes / 60:.2f} hours")

    print(f"\nWeakest area (least total study time): {weakest_subject} "
          f"({subject_totals[weakest_subject] / 60:.2f} hours)")

    print(f"Longest session recorded: {longest_session['subject']} - "
          f"{longest_session['topic']} ({longest_session['duration']:.0f} min, "
          f"{classify_session(longest_session['duration'])})\n")

# (a) main menu

def display_menu():
    print("=" * 40)
    print("       SMART STUDY PLANNER")
    print("=" * 40)
    print("1. Add a study session")
    print("2. View all sessions")
    print("3. Search sessions by subject")
    print("4. View statistics")
    print("5. Save and exit")


def main():
    sessions = load_sessions()  # automatically reload any existing data
    if sessions:
        print(f"Loaded {len(sessions)} existing session(s) from {DATA_FILE}.\n")

    while True:
        display_menu()
        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            add_session(sessions)
        elif choice == "2":
            view_sessions(sessions)
        elif choice == "3":
            search_by_subject(sessions)
        elif choice == "4":
            study_statistics(sessions)
        elif choice == "5":
            save_sessions(sessions)
            print("Goodbye! Happy studying.")
            break
        else:
            # Reject invalid choices without crashing
            print("Invalid choice. Please enter a number from 1 to 5.\n")


if __name__ == "__main__":
    main()