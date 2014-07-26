__author__ = 'amyalenkov'


class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.allPoints = list()
        self.currentPointX = None
        self.currentPointY = None


class Analyse:
    def __init__(self, players):
        self.players = list(players)

    def findPlayer(self, cx, cy):
        xRadius = 100
        yRadius = 100
        # todo to complete algorithm
        for player in self.players:
            if player.currentPointX is not None:
                difX = abs(cx - player.currentPointX)
                difY = abs(cy - player.currentPointY)
                if (xRadius <= difX) and (yRadius <= difY):
                    return self.getColorByName(player.name)


    def getColorByName(self, playerName):
        for player in self.players:
            if player.name == playerName:
                return player.color

    def getCoordinatesByName(self, playerName):
        for player in self.players:
            if player.name == playerName:
                return player.allPoints