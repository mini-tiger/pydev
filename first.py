import random

jiaoshengDict = {"tiger": "Wow..", "sheep": "mie.."}
tizhongDict = {"tiger": 200, "sheep": 100}
foodDict = {"tiger": "meat", "sheep": "grass"}

typeList = ["tiger", "meat"]


class Room(object):
    def __init__(self, *args, **kwargs):
        self.type = args[0]
        self.roomnum = args[1]
        print(args)
        self.tizhong = tizhongDict[self.type]
        self.food = foodDict[self.type]
        self.jiaosheng = jiaoshengDict[self.type]

    def weishi(self, food):
        if self.food == food:
            self.tizhong = self.tizhong + 10
        else:
            print("喂错了", self.type)
            self.tizhong = self.tizhong - 10

    def qiaomen(self):
        print(self.jiaosheng)


if __name__ == "__main__":
    roomlist = []
    for i in range(1, 11):
        suiji_num = random.randint(0, 10)
        if suiji_num > 5:
            r = Room("tiger", i)
        else:
            r = Room("sheep", i)
        roomlist.append(r)

    # print(r.__dict__)

    for i in range(0, 3):  # 不用3分钟  执行3次
        suiji_room = roomlist[random.randint(0, len(roomlist) - 1)]
        val = input("please qiaomen or weishi:")
        print("choose:", val)

        if val == "qiaomen":
            print(suiji_room.jiaosheng)
        elif val == "weishi":
            food = input("please meat or grass:")
            suiji_room.weishi(food)
        else:
            print("input 错了")

    for i in roomlist:
        print("roomNum:%d,Name:%s,tizhong:%d" % (i.roomnum, i.type, i.tizhong))
