import datetime

from app import db
from app.ModelsBE import *

class EVEPlayerDA(db.EmbeddedDocument):
    amendedAt = db.DateTimeField(default=datetime.datetime.now, required=True)
    name = db.StringField(max_length=255, required=True)
    alliance = db.StringField(max_length=255, required=False)
    standings = db.StringField(required=False)
    corporation = db.StringField(max_length=255, required=False)

    meta = {
        'allow_inheritance': True,
        'indexes': ['-amendedAt', 'name', 'alliance'],
        'ordering': ['-amendedAt']
    }

    def BE(self):
        jsonPlayer = EVEPlayerBE(name=self.name, alliance=self.alliance, corporation=self.corporation, standings=self.corporation)

        return jsonPlayer



class EVESystemDA(db.EmbeddedDocument):
    amendedAt = db.DateTimeField(default=datetime.datetime.now, required=True)
    name = db.StringField(max_length=255, required=True)
    players = db.ListField(db.EmbeddedDocumentField('EVEPlayerDA'))

    meta = {
        'allow_inheritance': True,
        'indexes': ['-amendedAt', 'name'],
        'ordering': ['-amendedAt']
    }

    def BE(self):

        playerList = list()
        for p in self.players:
            jsonP = p.BE()
            playerList.append(jsonP)
        jsonSystem = EVESystemBE(self.name, players=playerList)

        return jsonSystem


class UniverseDA(db.Document):
    amendedAt = db.DateTimeField(default=datetime.datetime.now, required=True)
    systems = db.ListField(db.EmbeddedDocumentField('EVESystemDA'))

    meta = {
        'allow_inheritance': True,
        'indexes': ['-amendedAt'],
        'ordering': ['-amendedAt']
    }

