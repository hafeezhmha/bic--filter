import requests
from icalendar import Calendar
import os
from datetime import datetime

FEED_URL = "https://bangaloreinternationalcentre.org/events/category/performance-art/?ical=1"
OUTPUT_FILE = "bic_filtered.ics"
LOG_FILE = "log.md"

INCLUDE = [
    "jazz", "orchestra", "symphony", "ballet",
    "mozart", "beethoven", "choir", "musical", "piano", "violin"
]
EXCLUDE = [
    "bharatanatyam", "kuchipudi", "kathak", "odissi",
    "carnatic", "hindustani", "raag", "tabla",
    "mridangam", "sitar"
]

def event_matches(event):
    text = ""
    for field in ["SUMMARY", "DESCRIPTION"]:
        if field in event:
            text += str(event[field]).lower() + " "

    if any(kw in text for kw in INCLUDE):
        return True
    if any(kw in text for kw in EXCLUDE):
        return False
    return False

def main():
    # fetch
    try:
        resp = requests.get(FEED_URL, timeout=15)
        resp.raise_for_status()
    except Exception as e:
        print(f"⚠️ Error fetching feed: {e}")
        if os.path.exists(OUTPUT_FILE):
            print("Keeping existing .ics file (no overwrite).")
            return
        else:
            raise SystemExit("No existing .ics file to fall back on.")

    # parse
    try:
        cal = Calendar.from_ical(resp.content)
    except Exception as e:
        print(f"⚠️ Could not parse feed: {e}")
        if os.path.exists(OUTPUT_FILE):
            print("Keeping existing .ics file (no overwrite).")
            return
        else:
            raise SystemExit("No existing .ics file to fall back on.")

    new_cal = Calendar()
    for name, value in cal.items():
        new_cal.add(name, value)

    included, excluded = [], []

    for component in cal.walk():
        if component.name == "VEVENT":
            title = str(component.get("SUMMARY", "Untitled"))
            if event_matches(component):
                new_cal.add_component(component)
                included.append(title)
            else:
                excluded.append(title)

    if not included:
        print("⚠️ No matching events found. Not overwriting existing file.")
        return

    with open(OUTPUT_FILE, "wb") as f:
        f.write(new_cal.to_ical())

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"## Run on {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC\n\n")
        f.write("### ✅ Included Events\n")
        if included:
            for ev in included:
                f.write(f"- {ev}\n")
        else:
            f.write("- None\n")

        f.write("\n### ❌ Excluded Events\n")
        if excluded:
            for ev in excluded:
                f.write(f"- {ev}\n")
        else:
            f.write("- None\n")

        f.write("\n---\n\n")

    print(f"✅ Saved {OUTPUT_FILE} with {len(included)} events. Log updated.")

if __name__ == "__main__":
    main()