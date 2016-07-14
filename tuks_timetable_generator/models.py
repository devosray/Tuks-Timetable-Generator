from enum import Enum
import time

class TimetableEntry(object):

    year     = None
    module   = None
    group    = None
    language = None
    lecture_number = None

    semester    = None
    day         = None
    time_start  = None
    time_end    = None
    venue       = None

    def __init__(self, year, module, group, language, lecture_number, semester, day, time_start, time_end, venue):
        self.year = year
        self.module = module
        self.group = group
        self.language = language
        self.lecture_number = lecture_number
        self.semester = semester
        self.day = day

        # Parse time and catch exception (some entries does not have a time...????)
        try:
            self.time_start = time.strptime(self.day + time_start, '%A%H:%M:%S')
        except:
            self.time_start = None

        try:
            self.time_end = time.strptime(self.day + time_end, '%A%H:%M:%S')
        except:
            self.time_end = None

        self.venue = venue

    def __str__(self):
        return self.module + ' ' + self.lecture_number + ', ' + self.day + ' ' + self.time_start + '-' + self.time_end

    def is_tutorial(self):
        return self.lecture_number[0] == 'T'

    def is_lecture(self):
        return self.lecture_number[0] == 'L'

    def is_practical(self):
        return self.lecture_number[0] == 'P'

    def does_clash_with_other(self, other_entry):
        clash = False

        if other_entry.day != self.day:
            return False

        if (other_entry.time_start == self.time_start and other_entry.time_end == self.time_end):
            clash = True

        if (self.time_start < other_entry.time_start < self.time_end):
            clash = True

        if (self.time_start < other_entry.time_end < self.time_end):
            clash = True

        if (other_entry.time_start > self.time_start and other_entry.time_end < self.time_end):
            clash = True

        if (self.time_start > other_entry.time_start and self.time_end < other_entry.time_end):
            clash = True

        return clash


class Module(object):

    module_name = None
    semester    = None

    def __init__(self, name, semester):
        # These arrays contain TimetableEntries
        self.lectures = []
        self.tutorials = []
        self.practicals = []

        self.module_name = name
        self.semester = semester

        self.filter = ModuleFilterItem(self.module_name)

    def __str__(self):
        return "%s sem. %s: %s lectures, %s tuts and %s pracs" % (self.module_name, self.semester,
                                                                 len(self.lectures), len(self.tutorials),
                                                                  len(self.practicals))

    def add_timetable_entry(self, timetable_entry):
        if timetable_entry.is_tutorial():
            self.tutorials.append(timetable_entry)
        elif timetable_entry.is_lecture():
            self.lectures.append(timetable_entry)
        elif timetable_entry.is_practical():
            self.practicals.append(timetable_entry)


class Choice(object):

    def __init__(self, parent, currentChoice):
        self.parent = parent
        self.currentChoice = currentChoice
        self.children = []

    def generate_children(self, choice_list, choice_index):
        if len(choice_list) <= choice_index:
            # Leaf node. Time to navigate back up
            #print(self.temp_find_root())
            entry_array = self.get_all_chosen_entries()

            # print(len(entry_array))

            # Group into days
            entries_grouped = dict()
            for entry in entry_array:
                if entry.day in entries_grouped:
                    entries_grouped[entry.day].append(entry)
                else:
                    entries_grouped[entry.day] = [entry]
            # print("FOUND :'D")
            Counter.counter += 1
            return None
        else:
            # Before we check any more children, we need to

            choice_item = choice_list[choice_index]
            choice_item.reset_current_option()
            while choice_item.has_more():
                new_child = Choice(self, choice_item.get_next_choice())
                self.children.append(new_child)

                # Before we add the new node to the tree, we need to make sure it fits!
                is_valid = True
                if isinstance(new_child.currentChoice, list):
                    for new_current_choice in new_child.currentChoice:
                        if not self.is_valid_child(new_current_choice):
                            is_valid = False
                else:
                    if not self.is_valid_child(new_child.currentChoice):
                        is_valid = False

                if is_valid:
                    new_index = choice_index + 1
                    new_child.generate_children(choice_list, new_index)
                    self.children = []

    def temp_find_root(self):
        if self.parent == None:
            return ""
        else:
            return self.currentChoice + self.parent.temp_find_root()

    def get_all_chosen_entries(self):
        if self.currentChoice is None:
            return []
        else:
            arr = self.parent.get_all_chosen_entries()
            if isinstance(self.currentChoice, list):
                for choice in self.currentChoice:
                    arr.append(choice)
            else:
                arr.append(self.currentChoice)
            return arr

    # Recursive function to see if a newly generated child clashes
    def is_valid_child(self, new_child):
        if self.parent == None:
            # No parent means root tree and that makes it automatically a valid entry
            return True
        else:
            # Does the time overlap with any of the choices?
            if isinstance(self.currentChoice, list):
                for choice in self.currentChoice:
                    if choice.does_clash_with_other(new_child):
                        return False
            else:
                if self.currentChoice.does_clash_with_other(new_child):
                    return False
            return self.parent.is_valid_child(new_child)



class ChoiceListItem(object):

    def __init__(self, choices=[]):
        self.options = choices
        self.currentOption = -1

    def get_next_choice(self):
        if self.currentOption >= len(self.options)-1:
            return None
        else:
            self.currentOption += 1
            return self.options[self.currentOption]

    def has_more(self):
        return self.currentOption < len(self.options)-1

    def reset_current_option(self):
        self.currentOption = -1


class LectureGroupingEnum(Enum):
    group_by_group = 1
    group_by_lecture_number = 2
    group_by_type = 3

class LectureLanguageEnum(Enum):
    afrikaans = 1
    english = 2
    any = 3

class ModuleFilterItem(object):

    def __init__(self, module_name,
                 lecture_grouping=LectureGroupingEnum.group_by_group,
                 tutorial_grouping=LectureGroupingEnum.group_by_type,
                 practical_grouping=LectureGroupingEnum.group_by_type,
                 lecture_langauge=LectureLanguageEnum.any):
        self.lecture_grouping = lecture_grouping
        self.tutorial_grouping = tutorial_grouping
        self.practical_grouping = practical_grouping
        self.module_name = module_name
        self.lecture_language = lecture_langauge

    def __str__(self):
        return self.module_name

class Counter(object):
    counter = 0

