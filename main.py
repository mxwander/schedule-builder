import csv

def to_minutes(time_text):
    """Turn a time like '13:55' into minutes after midnight (835)."""
    hours, minutes = time_text.split(":")
    return int(hours) * 60 + int(minutes)

def load_meetings(filename):
    """Read the CSV and return a list of class meetings."""
    meetings = []
    with open(filename, newline="") as file:
        for row in csv.DictReader(file):
            if row["days"] == "":
                print(f"Skipping {row['course']} {row['type']} (no set meeting times)")
                continue
            meetings.append({
                "name": f"{row['course']} {row['section']} {row['type']}",
                "days": set(row["days"]),
                "start": to_minutes(row["start"]),
                "end": to_minutes(row["end"]),
            })
    return meetings

def overlaps(a, b):
    """Two meetings conflict if they share a day AND their times overlap."""
    share_a_day = len(a["days"] & b["days"]) > 0
    times_overlap = a["start"] < b["end"] and b["start"] < a["end"]
    return share_a_day and times_overlap

def find_conflicts(meetings):
    """Compare every meeting with every other meeting once."""
    conflicts = []
    for i in range(len(meetings)):
        for j in range(i + 1, len(meetings)):
            if overlaps(meetings[i], meetings[j]):
                conflicts.append((meetings[i]["name"], meetings[j]["name"]))
    return conflicts

print("Schedule builder starting")
meetings = load_meetings("courses.csv")
print(f"Loaded {len(meetings)} class meetings.")

conflicts = find_conflicts(meetings)
if conflicts:
    for a, b in conflicts:
        print(f"CONFLICT: {a} overlaps {b}")
else:
    print("No conflicts found")