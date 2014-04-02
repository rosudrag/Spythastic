from app import db


class Player(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True)
    alliance = db.Column(db.String(100), index=True, unique=True)
    lastUpdated = db.Column(db.DATETIME, index=True)


class EVESystem(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True)
    playersLinkId = db.Column(db.INTEGER, index=True, unique=True)
    lastUpdated = db.Column(db.DATETIME, index=True)


class EVESystemPlayerLinks(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    systemid = db.Column(db.INTEGER, index=True)
    playerid = db.Column(db.INTEGER, index=True)


class Universe(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    systemsLinkId = db.Column(db.INTEGER, index=True, unique=True)
    lastUpdated = db.Column(db.DATETIME, index=True)


class UniverseEVESystemLinks(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    universeid = db.Column(db.INTEGER, index=True)
    systemid = db.Column(db.INTEGER, index=True)