from flask import Flask, request, render_template
from flask.ext.restful import Resource, Api, fields
from app import app
import time

api = Api(app)

#Json models

player1 = {'name': 'noob1', 'alliance': 'boon'}
player2 = {'name': 'newb', 'alliance': 'c0ven'}

system1 = {'name': 'w-q332',
           'players': [player1, player2]}

systems = {}

#Classes


class Player:
    def __init__(self, name, alliance):
        self.name = name
        self.alliance = alliance

class EVESystem:
    def __init__(self, name, players):
        self.name = name
        self.players = players
        self.timestamp = time.time()

    @property
    def lastupdatetime(self):
        return int(time.time() - self.timestamp)


class Universe:
    def __init__(self, name, systems):
        self.name = name
        self.systems = systems


class System(Resource):
    def put(self):
        theJson = request.json
        players = theJson['players']

        playerlist = list()

        for p in players:
            playerlist.append(Player(name=p['Name'], alliance=p['Alliance']))

        system_name = theJson['systemname']

        theSystem = EVESystem(name=system_name, players=playerlist)

        systems[system_name] = theSystem
        return theSystem.name + ' inserted'

@app.route('/evesystems')
def evesystems():
    systemNames = ''
    for key, value in systems.items():
        systemNames += value['name'] + ' '
    return render_template('test1.html', name=systemNames)

@app.route('/htmltest')
def htmltest():
    return render_template('base.html', systems=systems)

api.add_resource(System, '/evesystem')

if __name__ == '__main__':
    app.run()