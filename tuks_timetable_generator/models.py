
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


class Module(object):

    module_name = None
    semester    = None

    lectures   = []
    tutorials  = []
    practicals = []

    def __init__(self, name, semester):
        self.module_name = name
        self.semester = semester

    def __str__(self):
        return "%s sem. %s: %s lectures, %s tuts and %s pracs" % (self.module_name, self.semester,
                                                                  self.lectures.count(), self.tutorials.count(),
                                                                  self.practicals.count())



