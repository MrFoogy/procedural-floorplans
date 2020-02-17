class Room:
    def __init__(self, name, ident):
        self.name = name
        self.ident = ident

    def get_display_name(self):
        return self.name + '-' + str(self.ident)

    def is_exterior(self):
        return self.ident == 0
