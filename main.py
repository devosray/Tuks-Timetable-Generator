from tuks_timetable_generator import web_scraper, configuration
from tuks_timetable_generator.models import Choice, ChoiceListItem, ModuleFilterItem, LectureGroupingEnum,\
    LectureLanguageEnum, Counter

print("Downloading and parsing latest timetable...")
module_list = web_scraper.download_and_parse_url(configuration.HATFIELD_TIMETABLE_URL)

print("Finished parsing timetable")

# For testing purposes; demonstration list of modules to filter out
# With this config there are 213840 options
module_filter = [
    ModuleFilterItem("PHY 124"),
    ModuleFilterItem("WTW 124"),
    ModuleFilterItem("ALL 121"),
    ModuleFilterItem("OBS 124"),
    ModuleFilterItem("COS 121", lecture_grouping=LectureGroupingEnum.group_by_lecture_number),
    ModuleFilterItem("COS 110", lecture_grouping=LectureGroupingEnum.group_by_lecture_number),
    ModuleFilterItem("STK 120", lecture_langauge=)
]

for filter in module_filter:
    found = False
    for module in module_list:
        if module.module_name == filter.module_name:
            found = True
            break

    if not found:
        print("Did not find module '%s'" % filter)

# Remove modules not in filter list
temp_list = []
for module in module_list:
    found = False
    for filter in module_filter:
        if module.module_name == filter.module_name:
            module.filter = filter
            temp_list.append(module)
            break

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

# Generate list of choices based on selected modules and preference
choiceList = []

def generate_grouped_by_group_choices_from_array(lecture_array):
    group_choices = ChoiceListItem(choices=[])
    lecture_groups = dict()
    for lecture in lecture_array:
        group = lecture.group
        if group not in lecture_groups:
            lecture_groups[group] = [lecture]
        else:
            lecture_groups[group].append(lecture)

    for group_no in lecture_groups.keys():
        lectures_array = lecture_groups[group_no]
        group_choices.options.append(lectures_array)

    return group_choices


def generate_grouped_by_lecture_choices_from_array(lecture_array):
    group_choices = ChoiceListItem(choices=[])
    lecture_groups = dict()
    for lecture in lecture_array:
        group = lecture.lecture_number
        if group not in lecture_groups:
            lecture_groups[group] = [lecture]
        else:
            lecture_groups[group].append(lecture)

    for group_no in lecture_groups.keys():
        lectures_array = lecture_groups[group_no]
        group_choices.options.append(lectures_array)

    return group_choices


for module in module_list:


    # Split up in choices with the same lecture group like L1, L2 and L3 with common group 2
    if module.filter.lecture_grouping == LectureGroupingEnum.group_by_group:
        choiceList.append(generate_grouped_by_group_choices_from_array(module.lectures))

    elif module.filter.lecture_grouping == LectureGroupingEnum.group_by_lecture_number:
        generated_list = generate_grouped_by_lecture_choices_from_array(module.lectures)
        for choice in generated_list.options:
            new_choice_item = ChoiceListItem(choices=choice)
            choiceList.append(new_choice_item)

    # Filter tutorials
    if module.filter.tutorial_grouping == LectureGroupingEnum.group_by_group:
        choiceList.append(generate_grouped_by_group_choices_from_array(module.tutorials))

    elif module.filter.tutorial_grouping == LectureGroupingEnum.group_by_lecture_number:
        generated_list = generate_grouped_by_lecture_choices_from_array(module.tutorials)
        for choice in generated_list.options:
            new_choice_item = ChoiceListItem(choices=choice)
            choiceList.append(new_choice_item)

    # Select only ONE of all them
    elif module.filter.tutorial_grouping == LectureGroupingEnum.group_by_type:
        group_choices = ChoiceListItem(choices=[])
        for tutorial in module.tutorials:
            group_choices.options.append(tutorial)
        choiceList.append(group_choices)

    # Filter practicals
    if module.filter.practical_grouping == LectureGroupingEnum.group_by_type:
        group_choices = ChoiceListItem(choices=[])
        for practical in module.practicals:
            group_choices.options.append(practical)
        choiceList.append(group_choices)

# Filter out all empty choices
temp_list = []
for c in choiceList:
    if len(c.options) > 0:
        temp_list.append(c)
choiceList = temp_list

# item1 = ChoiceListItem(choices=[['A','P'], 'B', 'C'])
# item2 = ChoiceListItem(choices=['1', '2', '3'])
# item3 = ChoiceListItem(choices=['X', 'Y', 'Z'])
# choiceList.append(item1)
# choiceList.append(item2)
# choiceList.append(item3)

print("Generating Children")
rootNode.generate_children(choiceList, 0)
print("DONE")
print(Counter.counter)
