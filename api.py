from bson import json_util

from flask import request,render_template
from flask.ext.restful import Resource, Api
from app import app
from app.modelsDA import *


api = Api(app)

#Json models

'''
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


@app.route('/htmltest')
def htmltest():
    sortedSystems = OrderedDict(sorted(systems.items(), key=lambda x: x[1].name))
    return render_template('base.html', systems=sortedSystems)

@app.route('/htmltest2')
def htmltest2():
    sortedSystems = OrderedDict(sorted(systems.items(), key=lambda x: x[1].name))
    return render_template('base2.html', systems=sortedSystems)


api.add_resource(System, '/evesystem')
'''

class ExposeUniverse(Resource):
    def put(self):
        systemsjsonlist = request.json

        #print(systemsjsonlist)

        #systems inserted counter
        nrsystemsinserted = 0

        universe = UniverseDA()
        #Go through each system and construct player list
        for systemjson in systemsjsonlist:

            players = systemjson['players']

            playerlist = list()

            #construct the player objects
            for p in players:
                allianceToSet = str(p.get('Alliance', ''))
                nameToSet = p.get('Name', '')
                standingsToSet = str(p.get('Standings', ''))
                corpToSet = p.get('Corporation', '')

                thePlayer = EVEPlayerDA(name=nameToSet, alliance=allianceToSet, standings=standingsToSet, corporation=corpToSet)

                playerlist.append(thePlayer)

            system_name = systemjson['systemname']

            if system_name == '':
                continue

            sortedPlayerList = sorted(playerlist, key=lambda x: x.alliance)
            theSystem = EVESystemDA(name=system_name, players=sortedPlayerList)

            universe.systems.append(theSystem)

            nrsystemsinserted += 1

        try:
            universe.save()
        except Exception as e:
            print(e)

        return 'Inserted %s number of systems' % nrsystemsinserted


def SerialiseUniverse(x):
    systems = list()
    for s in x.systems:
        playerList = list()
        for p in s.players:
            player = EVEPlayerBE(name=p.name, alliance=p.alliance, corporation=p.corporation, standings=p.standings)
            playerList.append(player)
        system = EVESystemBE(name=s.name, players=playerList)
        systems.append(system)
    universe = UniverseBE(systems=systems)

    return universe


def SerialiseSystems(x):
    systems = {}
    for s in x.systems:
        playerList = list()
        for p in s.players:
            player = EVEPlayerBE(name=p.name, alliance=p.alliance, corporation=p.corporation, standings=p.standings)
            playerList.append(player)
        system = EVESystemBE(name=s.name, players=playerList)
        systems[s.name] = system
    return systems


@app.route('/htmltest2')
def htmltest2():
    try:
        x = UniverseDA.objects.first()
        #systems = SerialiseSystems(x)
        systems = {}
        for s in x.systems:
            system = s.BE()
            systems[system.name] = system
    except Exception as e:
        print(e)
    return render_template('/base2.html', systems=systems)

api.add_resource(ExposeUniverse, '/evesystem')

if __name__ == '__main__':
    app.run(host='0.0.0.0')