from app.modelsDA import *




u1 = Universe()
u1.save()

p1 = EVEPlayer(name='Chewy Ruko', alliance='C0ven')

s1 = EVESystem(name='w-q332')
s1.players.append(p1)

u1.systems.append(s1)

u1.save()




