import pprint
from dataclasses import dataclass
import random


@dataclass
class Sheep:
    type: int = 0
    weight: int = 100


@dataclass
class Tiger:
    type: int = 1
    weight: int = 200


def mapGenAnimal(type):
    """Factory Method"""
    genAnimal = {
        0: Tiger,
        1: Sheep,
    }
    return genAnimal[type]()


class Game:
    def __init__(self):

        randomlist = [random.randint(0, 1) for i in range(10)]

        print(randomlist)

        res = map(mapGenAnimal, randomlist)

        self.cages = list(res)

    def pickone(self):
        while True:
            randnum = random.randint(0, 9)
            randombeast = self.cages[randnum]
            val = input("选择喂食或敲门? ")
            if val == "喂食":
                foodval = input("选择喂meat或grass?")
                if foodval == self.__feed(randombeast):
                    self.cages[randnum].weight += 10
                    #pprint.pprint(self.cages)
                else:
                    self.cages[randnum].weight -= 10
                    #pprint.pprint(self.cages)
            elif val == "敲门":
                self.__knock(randombeast)
            else:
                continue

    @staticmethod
    def __knock(animaltype):
        if type(animaltype).__name__ == "Tiger":
            print("Wow !!")
        else:
            print("mie~~")
    @staticmethod
    def __feed(animaltype):
        if type(animaltype).__name__ == "Tiger":
            return "meat"
        else:
            return "grass"


if __name__ == '__main__':
    game = Game()
    game.pickone()
