import re

class VerRe:
    def __init__(self):
        self.regex = []

    def __str__(self): return ''.join(self.regex)
    def getRaw(self): return ''.join(self.regex)
    def add(self, value): self.regex.append(value)

    def match(self, value):
        complied = re.compile(self.getRaw())
        return complied.match(value)

    # ----- Command ----- #

    def start_of_line(self):
        self.add('^')
        return self

    def end_of_line(self):
        self.add('$')
        return self

    def maybe(self, value):
        self.add('(%s)?' % value)
        return self

    def find(self, value):
        self.add('(%s)' % value)
        return self

    def OR(self, a, b):
        self.add('(%s|%s)' % (a, b))
        return self


    # ----- Special Character ----- #

    def anything(self):
        self.add('.')
        return self

    def dot(self):
        self.add('[.]')
        return self

    # ----- One of Command ----- #

    def oneOf(self, *args):
        self.add('[%s]' % ''.join(args))
        return self

    def notOneOf(self, *args):
        self.add('[^%s]' % ''.join(args))
        return self

    def oneOfRange(self, start, end):
        self.add('[%s-%s]' % (start, end))
        return self

    def notOneOfRange(self, start, end):
        self.add('[^%s-%s]' % (start, end))
        return self

    # ----- Repeat Command ----- #

    def repeatPreviousRange(self, start : int = 0, end : int = 0):
        if start < 0: start = 0
        self.add('{%d,%d}' % (start, end))
        return self

    def repeatPrevious(self, value : int):
        if value < 0: value = 1
        self.add('{%d}' % value)
        return self

    def repeatPreviousOver1(self):
        self.add('+')
        return self

    def repeatPreviousOver0(self):
        self.add('*')
        return self