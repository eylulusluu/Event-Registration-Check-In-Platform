import csv


def attendance_report(events: list, registrations: list) -> dict:
    report = {}

    for event in events:
        event_id = event["id"]
        total = len([r for r in registrations if r["event_id"] == event_id])
        checked_in = len([
            r for r in registrations
            if r["event_id"] == event_id and r.get("checked_in")
        ])

        report[event_id] = {
            "event_name": event["name"],
            "registered": total,
            "checked_in": checked_in
        }

    return report


def revenue_report(events: list, registrations: list) -> dict:
    report = {}

    for event in events:
        event_id = event["id"]
        revenue = sum(
            r.get("price", 0)
            for r in registrations
            if r["event_id"] == event_id and r.get("status") == "confirmed"
        )

        report[event_id] = {
            "event_name": event["name"],
            "revenue": revenue
        }

    return report


def session_popularity(events: list, registrations: list) -> dict:
    popularity = {}

    for event in events:
        for session in event.get("sessions", []):
            count = 0
            for r in registrations:
                if session["id"] in r.get("sessions", []):
                    count += 1

            popularity[session["id"]] = {
                "session_title": session["title"],
                "attendance": count
            }

    return popularity


def export_report(report: dict, filename: str) -> str:
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Key", "Value"])

        for key, value in report.items():
            writer.writerow([key, value])

    return filename
