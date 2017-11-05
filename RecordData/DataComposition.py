from os import getcwd
from Reader import Reader
from EmotivEpoc import AverageBandPowers3
from time import sleep
from threads.myThreading import threaded


def bonding(first_list, second_list):
    res = [lst for lst in first_list]
    res.extend(second_list)
    return res


def get_data():
    return [0 for _ in range(5)]


def write_data(filename, update_time):
    try:
        file = open(getcwd() + filename, "w")
    except Exception as e:
        print("not open write file.", e)

    while not r.get_work():
        pass
    curr_all_data = []
    while r.get_work():
        curr_pos = r.get_pos()
        curr_input_data = bonding(brain.getActive(), [r.get_time_pause()])
        # curr_input_data = bonding(get_data(), [r.get_time_pause()])
        print(r.get_time_pause())
        curr_all_data.append(curr_input_data)
        curr_all_data.append(curr_pos)
        file.write(" ".join([str(i) for i in curr_input_data]))
        file.write(" || " + str(r.get_state()) + " || " + str(curr_pos) + "\n")
        print("to do...")
        curr_all_data.clear()
        sleep(update_time)

    file.flush()
    file.close()


# =========================================================


UPDATE_TIME = 0.2
FILE_NAME = "/ResultData/data2"

r = Reader.Reader("InputData/text2.txt")
brain = AverageBandPowers3.Brain()

threaded(r.sliding_read)()
threaded(brain.go)()
write_data(FILE_NAME, UPDATE_TIME)
