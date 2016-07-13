import urllib.request
from bs4 import BeautifulSoup

from . import configuration
from .models import TimetableEntry, Module

def download_url(url):
    request = urllib.request.Request(url)
    return urllib.request.urlopen(request)

# Downloads the timetable from the URL and parse entry into modules
# Returns array of module objects
# TODO: Allow different campus timetables
# TODO: Add more types of lecture types (B, O?)
def download_and_parse_url(url):
    html_response = download_url(url)
    soup = BeautifulSoup(html_response, 'html.parser')
    data_table = soup.find(id="myTable")
    table_body = data_table.find("tbody")
    table_rows = table_body.find_all("tr")

    parsed_timetable = []

    # Parse HTML into objects
    for row in table_rows:
        data_elements = row.find_all("td")

        # Elements in Hatflied timetable returned as follows:
        #               0                   1                 2                 3                   4               5
        # [<td>2/MBY 262/G02/B/P1</td>, <td>S2</td>, <td>Wednesday</td>, <td>14:30:00</td>, <td>17:30:00</td>, <td>Biolab C</td>]
        description_items = data_elements[0].get_text().split('/')
        year = description_items[0]
        module = description_items[1]
        group = description_items[2]
        language = description_items[3]
        lecture_number = description_items[4]

        semester = data_elements[1].get_text()
        day = data_elements[2].get_text()
        time_start = data_elements[3].get_text()
        time_end = data_elements[4].get_text()
        venue = data_elements[5].get_text()

        timetable_element = TimetableEntry(year, module, group, language, lecture_number, semester, day,
                                           time_start, time_end, venue)

        parsed_timetable.append(timetable_element)

    # Parse array of objects into modules
    modules_list = []

    for timetable_entry in parsed_timetable:
        found = False
        current_module = None
        for module in modules_list:
            if module.module_name == timetable_entry.module:
                found = True
                current_module = module
                break

        if not found:
            new_module = Module(timetable_entry.module, timetable_entry.semester)
            modules_list.append(new_module)
            current_module = new_module

        current_module.add_timetable_entry(timetable_entry)

    return modules_list

