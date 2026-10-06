# NC State Schedule Builder

A Pyhton tool that finds every conflict-free combination of class sections and ranks them by what students actually are about.

## Features

- Reads course sections from a simple CSV file
- Detects time conflicts between lectures, labs, and recitations
- Keeps linked meetings together (a lecture and its recitation are scheduled as one section)
- Ranks schedule by fewest days on cmapus, least time between classes, and latest first class
- Skips online classes with no meeting times and flags malformed rows instead of crashing

## How to Run

Requires Python 3. No extra package needed

```
python3 main.py
```

## CSV Format

Each row is one class meeting. Days use M, T, W, H (Thursday), F, and times use 24-hour format.

```
course,section,type,days,start,end
CH 101,004,LEC,MWF,12:50,13:40
CH 101,004,REC,T,15:00,15:50
MA 241,005,LEC,TH,11:45,13:00
```

## Example Output

```
Schedule builder starting
Skipping E 115 LEC (no set meeting times)
Found 1 possible schedule(s), best first.

Schedule 1: 5 days on campus, 695 min of gaps, earliest class 8:30 AM
  CH 101 section 004
  CH 102 section 101
  ENG 101 section 004
  HESF 102 section 001
  MA 241 section 005
```

## Planned Features

- Let users choose which priorities matter most
- Web interface with a weekly calendar view

## Author

Matthew Wanderski, Electrical Engineering, NC State University