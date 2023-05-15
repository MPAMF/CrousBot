import datetime
import locale
import os
from datetime import datetime
from typing import Optional, Dict, List

import pytz
import requests
from ics import Calendar


class Cours:
    urls: Dict[str, str]

    def __init__(self, client, message):
        self.client = client
        self.message = message
        self.name = "Cours"
        self.description = "Affiche les cours du jour"
        self.urls = {
            "sil": os.getenv("CALENDAR_URL_SIL", ""),
            "siris": os.getenv("CALENDAR_URL_SIRIS", ""),
            "sdsc": os.getenv("CALENDAR_URL_SDSC", ""),
            "i3d": os.getenv("CALENDAR_URL_I3D", "")
        }
        self.timezone = pytz.timezone(
            'Europe/Paris')  # Adjust to your local timezone
        locale.setlocale(locale.LC_TIME, 'fr_FR.utf8')

    def get_url(self, course: str) -> Optional[str]:
        url = self.urls[course] if course in self.urls.keys() else None
        return None if url is None or url == "rien" else url

    def gen_key_value_pairs(self, data) -> List[str]:
        # Calculate maximum width for keys and values
        max_key_length = max(len(key) for key, _ in data)
        max_value_length = max(len(value) for _, value in data)

        # Calculate rectangle width and height
        width = max_key_length + max_value_length + 6
        result = ["+" + "-" * (width - 1) + "+"]

        # Print the top line

        # Print each key-value pair in the rectangle
        for key, value in data:
            if key == "separator":
                result.append("+" + "-" * (width - 1) + "+")
                continue
            result.append(
                "| {:{}} : {:{}} |".format(key, max_key_length, value,
                                           max_value_length))

        return result

    async def execute(self):
        arr = self.message.content.split(" ")
        course = "sil" if len(arr) < 2 else arr[1]
        url = self.get_url(course)

        if url is None:
            return await self.message.channel.send("tu déconnes fréro")

        # Fetch the content of the iCalendar file
        response = requests.get(url)

        # Parse the calendar data
        calendar = Calendar(response.text)

        # Get today's date
        today = datetime.today().date()

        rows = []

        sorted_events = sorted(
            (event for event in calendar.events if
             event.begin.date() == today),
            key=lambda event: event.begin,
            reverse=False
        )

        for event in sorted_events:
            hour_begin = event.begin.astimezone(self.timezone).strftime('%H:%M')
            hour_end = event.end.astimezone(self.timezone).strftime('%H:%M')
            name = event.name if event.name else 'No Title'
            location = event.location if event.location else 'No Location'
            location = location.split(" (")[0]
            rows.append(('Horaire', hour_begin + ' -> ' + hour_end))
            rows.append(('Name', name))
            rows.append(('Salle', location))
            rows.append(('separator', ''))

        result = self.gen_key_value_pairs(rows)
        result.insert(0, "Jour %s :" % "sil".upper())
        await self.message.channel.send("```" + "\n".join(result) + "```")

