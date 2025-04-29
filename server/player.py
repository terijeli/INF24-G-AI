# Author: SKQU
# Date: 2025-04-28  
# Description: Player class for the Pong game server.
# This class handles player attributes and methods for setting and getting player positions.
# It is used to manage player data in the game server.
#
#
# This code is part of a Pong game server implementation.
# The server handles player connections, manages game state, and communicates with clients.
# The Player class is a fundamental part of this implementation, allowing for easy management of player data.
#
## The code is licensed under the MIT License.
## For more information, see the LICENSE file in the project root.
#

class Player:
    __id  = ""
    __y = ""
    __x = ""

    # Constructor to initialize the player with a unique ID.
    # The ID is generated using a hash function to ensure uniqueness.
    def __init__(self, id):
        self.__id = id

    # Method to set the player's position on the game board.
    # The position is represented by y (vertical) and x (horizontal) coordinates.
    def setPos(self, y,x):
        self.__y = y
        self.__x = x

    # Method to get the player's current position.
    # The position is returned as a list of strings, representing y and x coordinates.
    def getPos(self):
        return [str(self.__y), str(self.__x)]

    # Method to get the player's unique ID.
    # The ID is returned as a string.
    def getId(self):
        return self.__id