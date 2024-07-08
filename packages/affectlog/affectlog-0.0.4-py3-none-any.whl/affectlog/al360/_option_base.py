class OptionBase:
    """
    Base class providing methods for options. The goal of it is to
    create common interface for PlotContainer and Resource.
    """
    options_category = "base"
    options = {}
    def __init__(self, al360):
        if type(al360).__name__ != 'AL360' or type(al360).__module__ != 'affectlog.al360.object':
            raise Exception('Invalid AL360 argument')
        self.al360 = al360

    def get_option(self, name):
        return self.al360.get_option(self.__class__.options_category, name)

    def set_option(self, name, value):
        return self.al360.set_option(self.__class__.options_category, name, value)
