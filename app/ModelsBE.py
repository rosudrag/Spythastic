class EVEPlayerBE:
    def __init__(self, name, alliance, standings, corporation):
        self.name = name
        self.alliance = alliance
        self.standings = standings
        self.corporation = corporation


class EVESystemBE:
    def __init__(self, name, players):
        self.name = name
        self.players = players


class UniverseBE:
    def __init__(self, systems):
        self.systems = systems