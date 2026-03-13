import json
from datetime import datetime

def create_event(event):
    lines = []
    lines.append("BEGIN:VEVENT")
    lines.append(f"UID:{event['uid']}")
    lines.append(f"DTSTAMP:{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}")
    
    if event.get("all_day"):
        lines.append(f"DTSTART;VALUE=DATE:{event['date'].replace('-', '')}")
    else:
        time = event.get("time", "0900")
        lines.append(f"DTSTART:{event['date'].replace('-', '')}T{time}00")

    if event.get("rrule"):
        lines.append(f"RRULE:{event['rrule']}")

    lines.append(f"SUMMARY:{event['summary']}")

    if event.get("description"):
        lines.append(f"DESCRIPTION:{event['description']}")

    lines.append("END:VEVENT")

    return "\n".join(lines)


def build_calendar(name, events):

    lines = []
    lines.append("BEGIN:VCALENDAR")
    lines.append("VERSION:2.0")
    lines.append(f"PRODID:-//Marc Life Calendar//{name}//EN")
    lines.append("CALSCALE:GREGORIAN")

    for event in events:
        lines.append(create_event(event))

    lines.append("END:VCALENDAR")

    return "\n".join(lines)


def main():

    with open("calendar_data.json") as f:
        data = json.load(f)

    for calendar_name, events in data.items():

        content = build_calendar(calendar_name, events)

        filename = f"{calendar_name}.ics"

        with open(filename, "w") as f:
            f.write(content)

        print(f"Generated {filename}")


if __name__ == "__main__":
    main()
