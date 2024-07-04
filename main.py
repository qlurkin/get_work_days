# from ics import Calendar
from datetime import datetime
import requests
import argparse
import arrow
import icalendar

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
    with open("config") as file:
        url = file.read().strip()
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

# c = Calendar(ics)
c = icalendar.Calendar.from_ical(ics)

days = set()

# for event in c.events:
#     d = event.begin
#     d = arrow.arrow.Arrow(d.year, d.month, d.day)
#     if d.is_between(start, end, bounds="[)"):
#         days.add(d)

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


print(f"du {start.strftime('%d/%m/%Y')} au {end.strftime('%d/%m/%Y')}")
print(len(days))

# e = sorted(list(days))[19]

# print(dir(e))
# print(e._get_iteration_params())
