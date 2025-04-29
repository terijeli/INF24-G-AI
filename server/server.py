import asyncio
from websockets.asyncio.server import serve
import random
import player as Player

import socket
ip = socket.gethostbyname(socket.gethostname())
print("Server started on ws://{}:8765".format(ip))
exit()

paddleSpeed = "5"
ids = []
players = {}
#{
#    # id : [corY, corX]
#}

x = 600 // 2
y = 600 // 2
ball = str(x) + "," + str(y)
speedX = random.uniform(-3, 5)
speedY = random.uniform(-3, 5)
WIDTH, HEIGHT = 600, 600
rectSize = 75

    
def getId(messages):
    playerId = str(hash(random.uniform(0,10)))
    player = Player.Player(playerId)
    if len(list(players)) > 0:
        player.setPos(messages[1], WIDTH - 30)
        players["secondary"] = player
    else:
        players["primary"] = player
        player.setPos(messages[1], 20)
    coordinates = player.getPos()
    return playerId + "," + coordinates[0] + "," + coordinates[1]


def getOpp(messages):  
        if players["primary"].getId == messages[1]:
            coordinates = players["primary"].getPos()
        elif players["secondary"]:
            coordinates = players["secondary"].getPos()
        else:
            coordinates = [0,0]
        return coordinates[0] + "," + coordinates[1]


def setCoor(messages):
        if players["primary"].getId() == messages[1]:
            player = players["primary"]
        else:
            player = players["secondary"]
        player.setPos(messages[2], messages[3])
        coordinates = player.getPos()
        return coordinates[0] + "," + coordinates[1]


def getBall(messages):
        global x,y,speedX, speedY
        playerids = list(players.keys())
        player = players[playerids[0]].getPos()
        playerbtn = float(player[0]) - rectSize / 2
        playertop = float(player[0]) + rectSize / 2
        playerx = float(player[1])
        opp = players[playerids[1]].getPos()
        oppbtn = float(opp[0]) - rectSize / 2
        opptop = float(opp[0]) + rectSize / 2
        oppx = float(opp[1])
        if playerx < x < playerx + 10 and playerbtn < y < playertop:
            speedX *= -1
        if oppx < x <  oppx + 10 and oppbtn < y < opptop:
            speedX *= -1
        if y < 0 or y > HEIGHT:
            speedY *= -1
        x += speedX
        y += speedY
        return str(x) + "," + str(y)


def opCode(opcode : str, messages): 
        response = ""
        if opcode == "getId":
            response = getId(messages)
        elif opcode == "getOpp":
            response = getOpp(messages)
        elif opcode == "getIds":
            response = players["primary"].getId() + "," + players["secondary"].getId()
        elif opcode == "setCoor":
            response = setCoor(messages)
        elif opcode == "getBall":
            response = getBall(messages)
        elif opcode == "resetBall":
            x = 600 // 2
            y = 600 // 2
            speedX = random.uniform(-3, 5)
            speedY = random.uniform(-3, 5)

            response = str(x) + "," + str(y)
        return response


async def respond(websocket):
    global x,y,speedX, speedY
    async for message in websocket:
        messages = message.split(",")
        opcode = messages[0]
        response = opCode(opcode, messages)

        await websocket.send(response)

"""async def echo(websocket):
    global x,y,speedX, speedY
    async for message in websocket:
        messages = message.split(",")
        opcode = messages[0]
        response = ""
        if opcode == "getId":
            playerId = str(hash(random.uniform(0,10)))
            if len(list(players.keys())) > 0:
                
                x = WIDTH - 30
            else:
                x = 20
            players[playerId] = [messages[1], str(x)]
            response = playerId + "," + players[playerId][0] + "," + players[playerId][1]
        elif opcode == "getOpp":
            opId = str(messages[1]) 
            response = players[opId][0] + "," + players[opId][1]
        elif opcode == "getIds":
            response = ""
            ids = list(players.keys())
            for i in range(len(ids)):
                response += ids[i-1]
                response += ","
            response = response[:-1]
        elif opcode == "setCoor":
            id = messages[1]
            players[id][0] = messages[2]
            response = players[id][0] + "," + players[id][1]
            print(response)
        elif opcode == "getBall":
            playerids = list(players.keys())
            player = players[playerids[0]]
            playerbtn = float(player[0]) - rectSize / 2
            playertop = float(player[0]) + rectSize / 2
            playerx = float(player[1])
            opp = players[playerids[1]]
            oppbtn = float(opp[0]) - rectSize / 2
            opptop = float(opp[0]) + rectSize / 2
            oppx = float(opp[1])
            if playerx < x < playerx + 10 and playerbtn < y < playertop:
                speedX *= -1
            if oppx < x <  oppx + 10 and oppbtn < y < opptop:
                speedX *= -1
            if y < 0 or y > HEIGHT:
                speedY *= -1
            x += speedX
            y += speedY
            response = str(x) + "," + str(y)
            print(response)
        elif opcode == "resetBall":
            x = 600 // 2
            y = 600 // 2
            speedX = random.uniform(-3, 5)
            speedY = random.uniform(-3, 5)
            response = str(x) + "," + str(y)

        await websocket.send(response)
"""

async def main():
    print("Server started on ws://{}:8765".format(ip))
    async with serve(respond, ip, 8765) as server:
        await server.serve_forever()


asyncio.run(main())