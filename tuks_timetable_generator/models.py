
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
        self.time_start = time_start
        self.time_end = time_end
        self.venue = venue

    def __str__(self):
        return self.module + ' ' + self.lecture_number + ', ' + self.day + ' ' + self.time_start + '-' + self.time_end

    def is_tutorial(self):
        return self.lecture_number[0] == 'T'

    def is_lecture(self):
        return self.lecture_number[0] == 'L'

    def is_practical(self):
        return self.lecture_number[0] == 'P'


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
            return None
        else:
            choice_item = choice_list[choice_index]
            choice_item.reset_current_option()
            while choice_item.has_more():
                new_child = Choice(self, choice_item.get_next_choice())
                self.children.append(new_child)
                new_index = choice_index + 1
                new_child.generate_children(choice_list, new_index)



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