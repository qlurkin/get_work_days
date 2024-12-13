from datetime import datetime
import requests
import argparse
import icalendar
import json
import subprocess as sp

from dateutil.rrule import MO, TU, WE, TH, FR, SA, SU, WEEKLY, rrule, weekday

wd: dict[str, weekday] = {
    "MO": MO,
    "TU": TU,
    "WE": WE,
    "TH": TH,
    "FR": FR,
    "SA": SA,
    "SU": SU,
}

try:
    with open("config.json") as file:
        config = json.loads(file.read())
        url = config["url"]
        trigramme = config["trigramme"]
        firstname = config["firstname"]
        lastname = config["lastname"]
        price_per_km = config["priceperkm"]
        address = config["address"]
except FileNotFoundError:
    raise Exception("Config file not found")

parser = argparse.ArgumentParser(
    description="Get the number of work day between start date (inclusive) and end date (exclusive)",
)

parser.add_argument("start")
parser.add_argument("end")

args = parser.parse_args()
start = datetime.fromisoformat(args.start)
end = datetime.fromisoformat(args.end)

response = requests.get(url)

if response.status_code != 200:
    raise Exception(f"Request failed with code {response.status_code}")

ics = response.text

c = icalendar.Calendar.from_ical(ics)

# with open("LUR.ics") as file:
#     c = icalendar.Calendar.from_ical(file.read())

days = set()

for event in c.walk("VEVENT"):
    dtstart = event.get("DTSTART").dt
    recur = event.get("RRULE")
    if recur is not None:
        freq = recur["FREQ"][0]
        count = recur["COUNT"][0]
        byday = tuple(filter(None, map(wd.get, recur["BYDAY"])))
        dts = list(
            rrule(freq=WEEKLY, count=count, byweekday=byday, wkst=MO, dtstart=dtstart)
        )
    else:
        dts = [dtstart]
    for dt in dts:
        dt = dt.replace(tzinfo=None)
        if dt >= start and dt < end:
            days.add(dt.date())

# print(f"du {start.strftime('%d/%m/%Y')} au {end.strftime('%d/%m/%Y')}")
days = "(" + ", ".join([f'"{d.strftime("%d/%m/%Y")}"' for d in sorted(days)]) + ")"
# print()
# print(len(days))

with open("template.typ") as file:
    content = (
        file.read()
        .replace('("DAYS",)', days)
        .replace('"PRICE_PER_KM"', str(price_per_km))
        .replace("FULLNAME", firstname + " " + lastname)
        .replace("FIRSTNAME", firstname)
        .replace("LASTNAME", lastname)
        .replace("ADDRESS", address)
    )

with open("document.typ", "w") as file:
    file.write(content)

sp.run(["typst", "compile", "document.typ"])
