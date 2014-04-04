from flask import Flask, request, render_template
from flask.ext.restful import Resource, Api, fields
from app import app
from collections import OrderedDict
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
    def __init__(self, name, alliance, standings, corporation):
        self.name = name
        self.alliance = alliance
        self.standings = standings
        self.corporation = corporation


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
        systemsjsonlist = request.json

        print(systemsjsonlist)

        #systems inserted counter
        nrsystemsinserted = 0

        #Go through each system and construct player list
        for systemjson in systemsjsonlist:

            players = systemjson['players']

            playerlist = list()

            #construct the player objects
            for p in players:
                allianceToSet = str(p.get('Alliance', ''))
                nameToSet = p.get('Name', '')
                standingsToSet = p.get('Standings', '')
                corpToSet = p.get('Corporation', '')

                thePlayer = Player(name=nameToSet, alliance=allianceToSet, standings=standingsToSet, corporation=corpToSet)

                playerlist.append(thePlayer)

            system_name = systemjson['systemname']

            if system_name == '':
                continue

            sortedPlayerList1 = sorted(playerlist, key=lambda x: x.alliance)
            theSystem = EVESystem(name=system_name, players=sortedPlayerList1)
            systems[system_name] = theSystem

            nrsystemsinserted += 1

        return 'Inserted %s number of systems' % nrsystemsinserted


@app.route('/evesystems')
def evesystems():
    systemNames = ''
    for key, value in systems.items():
        systemNames += value['name'] + ' '
    return render_template('test1.html', name=systemNames)


@app.route('/htmltest')
def htmltest():
    sortedSystems = OrderedDict(sorted(systems.items(), key=lambda x: x[1].name))
    return render_template('base.html', systems=sortedSystems)

@app.route('/htmltest2')
def htmltest2():
    sortedSystems = OrderedDict(sorted(systems.items(), key=lambda x: x[1].name))
    return render_template('base2.html', systems=sortedSystems)


api.add_resource(System, '/evesystem')

if __name__ == '__main__':
    app.run(host='0.0.0.0')