class Room:
    def __init__(self, name, ident, max_valence, max_num, utilities):
        self.name = name
        self.ident = ident
        self.max_valence = max_valence
        self.max_num = max_num
        self.utilities = utilities

    def get_display_name(self, index):
        return self.name + '-' + str(index)

    def is_exterior(self):
        return self.ident == 0
