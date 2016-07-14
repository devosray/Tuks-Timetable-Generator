from tuks_timetable_generator import web_scraper, configuration
from tuks_timetable_generator.models import Choice, ChoiceListItem

print("Downloading and parsing latest timetable...")
module_list = web_scraper.download_and_parse_url(configuration.HATFIELD_TIMETABLE_URL)

print("Finished parsing timetable")

# For testing purposes; demonstration list of modules to filter out
module_filter = [
    "ALL 121",
    "STK 120",
    "WTW 124",
    "COS 121",
    "PHY 124",
    "OBS 124",
    "COS 110"
]

for filter in module_filter:
    found = False
    for module in module_list:
        if module.module_name == filter:
            found = True
            break

    if not found:
        print("Did not find module '%s'" % filter)

# Remove modules not in filter list
temp_list = []
for module in module_list:
    if module.module_name in module_filter:
        temp_list.append(module)
module_list = temp_list

# for module in module_list:
#     if module.module_name == 'WTW 124':
#
#         # Get all lecture groups
#         lecture_groups = dict()
#         for lecture in module.lectures:
#             group = lecture.lecture_number
#             if not group in lecture_groups:
#                 lecture_groups[group] = [lecture]
#             else:
#                 lecture_groups[group].append(lecture)
#
#         print(lecture_groups)

# Root node
rootNode = Choice(parent=None, currentChoice=None)

choiceList = []
item1 = ChoiceListItem(choices=['A', 'B', 'C'])
item2 = ChoiceListItem(choices=['1', '2', '3'])
item3 = ChoiceListItem(choices=['X', 'Y', 'Z'])
choiceList.append(item1)
choiceList.append(item2)
choiceList.append(item3)

rootNode.generate_children(choiceList, 0)
print("DONE")