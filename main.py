import csv
from itertools import product


def to_minutes(time_text):
    """Turn a time like '13:55' into minutes after midnight (835)."""
    hours, minutes = time_text.split(":")
    return int(hours) * 60 + int(minutes)


def load_meetings(filename):
    """Read the CSV and return a list of class meetings."""
    meetings = []
    with open(filename, newline="") as file:
        for row in csv.DictReader(file):
            if None in row.values():
                print(f"Skipping bad row (missing values): {row}")
                continue
            if row["days"] == "":
                print(f"Skipping {row['course']} {row['type']} (no set meeting times)")
                continue
            meetings.append({
                "course": row["course"],
                "section": row["section"],
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


def group_sections(meetings):
    """Organize meetings as {course: {section: [its meetings]}}."""
    courses = {}
    for m in meetings:
        courses.setdefault(m["course"], {}).setdefault(m["section"], []).append(m)
    return courses


def build_schedules(courses):
    """Try every combination of one section per course; keep conflict-free ones."""
    course_names = list(courses.keys())
    section_options = [list(courses[name].keys()) for name in course_names]
    valid = []
    for combo in product(*section_options):
        chosen = []
        for name, section in zip(course_names, combo):
            chosen.extend(courses[name][section])
        if not find_conflicts(chosen):
            valid.append({"sections": dict(zip(course_names, combo)), "meetings": chosen})
    return valid


def to_clock(minutes):
    """Turn minutes after midnight (835) back into a time like '1:55 PM'."""
    hours, mins = divmod(minutes, 60)
    suffix = "AM" if hours < 12 else "PM"
    hours = hours % 12 or 12
    return f"{hours}:{mins:02d} {suffix}"


def schedule_stats(meetings):
    """Measure a schedule: days on campus, total gap minutes, earliest class."""
    days_used = set()
    for m in meetings:
        days_used |= m["days"]

    earliest = min(m["start"] for m in meetings)

    gap_minutes = 0
    for day in days_used:
        todays = sorted((m for m in meetings if day in m["days"]), key=lambda m: m["start"])
        for prev, nxt in zip(todays, todays[1:]):
            gap_minutes += nxt["start"] - prev["end"]

    return {"days": len(days_used), "earliest": earliest, "gaps": gap_minutes}

print("Schedule builder starting")
meetings = load_meetings("courses.csv")
courses = group_sections(meetings)
schedules = build_schedules(courses)

for s in schedules:
    s["stats"] = schedule_stats(s["meetings"])

# Best first: fewest days, then least gap time, then latest first class
schedules.sort(key=lambda s: (s["stats"]["days"], s["stats"]["gaps"], -s["stats"]["earliest"]))

print(f"Found {len(schedules)} possible schedule(s), best first.")
for number, s in enumerate(schedules, start=1):
    stats = s["stats"]
    print(f"\nSchedule {number}: {stats['days']} days on campus, "
          f"{stats['gaps']} min of gaps, earliest class {to_clock(stats['earliest'])}")
    for course, section in s["sections"].items():
        print(f"  {course} section {section}")