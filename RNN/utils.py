import numpy as np
import random


def unpack_train_data(filename):
    file = open(filename, "r")
    data_x = []
    data_y = []
    data_z = []
    for line in file:
        train_data = line.split(sep=' || ')
        train_data[0] = train_data[0].split(sep=' ')
        x = np.array([float(i) for i in train_data[0]])
        np.delete(x, -1, 0)
        y = int(train_data[1])
        z = int(train_data[2])
        data_x.append(x)
        data_y.append(y)
        data_z.append(z)
    file.close()
    return np.array(data_x), np.array(data_y), np.array(data_z)


def generate_random_data(filename, count):
    f = open(filename, "w")
    for _ in range(count):
        x = [random.random() for _ in range(6)]
        y = random.randint(0, 1)
        f.write(" ".join([str(i) for i in x]) + " || " + str(y) + "\n")
    f.flush()
    f.close()


def to_binary(arr):
    return np.array([[1, 0] if y[0] > y[1] else [0, 1] for y in arr])


def accuracy(y_res, y_true):
    count = 0
    if len(y_res) != len(y_true):
        return -1
    for i in range(len(y_res)):
        if np.array_equal(y_res[i], y_true[i]):
            count += 1
    return count / len(y_res)


def to_class(y, count_class):
    return np.array([1 if i == y[-1] else 0 for i in range(count_class)])


def separation(data):
    data_0 = np.array([elem[0] for elem in data])
    data_1 = np.array([elem[1] for elem in data])
    return data_0, data_1


def prepare_data(all_x, all_y, length_seq, count_class,
                 count_train_batch, count_test_batch):
    try:
        count_data = all_x.shape[0]
        min_count_data = length_seq + count_train_batch + count_test_batch - 1
        if count_data < min_count_data:
            raise Exception("need more data")
        all_data = []
        for i in range(min_count_data):
            all_data.append(np.array([all_x[i:i+length_seq],
                            to_class(all_y[i:i+length_seq], count_class)]))
        all_data = np.array(all_data)
        np.random.shuffle(all_data)
        train_data = np.array([all_data[i] for i in range(0, count_train_batch)])
        test_data = np.array([all_data[i] for i in range(count_train_batch,
                                                         count_train_batch + count_test_batch)])
        train_x, train_y = separation(train_data)
        test_x, test_y = separation(test_data)
        return train_x, train_y, test_x, test_y
    except Exception as e:
        print(e)
        print(e.args)
        exit(1)


def prepare_test_data(all_x, all_y, all_z, length_seq, count_class):
    try:
        count_data = all_x.shape[0]
        if count_data < length_seq:
            raise Exception("need more data")
        all_data = []
        for i in range(count_data - length_seq):
            all_data.append(np.array([all_x[i:i+length_seq],
                                      to_class(all_y[i:i+length_seq], count_class),
                                      all_z[i]]))
        x = np.array([elem[0] for elem in all_data])
        y = np.array([elem[1] for elem in all_data])
        z = np.array([elem[2] for elem in all_data])
        return x, y, z
    except Exception as e:
        print(e)
        print(e.args)
        exit(1)


def prepare_real_data(all_x, all_z, length_seq):
    try:
        count_data = all_x.shape[0]
        if count_data < length_seq:
            raise Exception("need more data")
        all_data = []
        for i in range(count_data - length_seq):
            all_data.append(np.array([all_x[i:i+length_seq], all_z[i]]))
        train_x, train_z = separation(all_data)
        return train_x, train_z
    except Exception as e:
        print(e)
        print(e.args)
        exit(1)


def get_state(y):
    for i in range(len(y)):
        if y[i] == 1:
            return i


def write_code_se(f, state):
    if state == 0:
        f.write('<font color="BLUE">')
    elif state == 1:
        f.write('<font color="GREEN">')
    else:
        f.write("</font>")


def write_code_t(f, state):
    f.write("</font>")
    if state == 0:
        f.write('<font color="BLUE">')
    elif state == 1:
        f.write('<font color="GREEN">')


def padding_arr(arr, count):
    return np.concatenate((np.array([arr[0] for _ in range(count)]), arr), axis=0)


def markup_text(filename_w, filename_r, cls, pos, length_seq):
    try:
        states = np.array([get_state(c) for c in cls])
        padding_arr(states, length_seq)
        file_r = open(filename_r, "r")
        full_text = list(file_r.read())
        file_r.close()
        file_w = open(filename_w, 'w')
        file_w.write('<HTML><HEAD><TITLE>Форматирование текстовых данных</TITLE></HEAD><BODY>')
        write_code_se(file_w, states[0])
        pre_pos = 0
        for i in range(len(states)-1):
            if states[i] != states[i+1]:
                curr_pos = pos[i]
                for j in range(pre_pos, curr_pos):
                    file_w.write(full_text[j])
                pre_pos = curr_pos
                write_code_t(file_w, states[i+1])
        for j in range(pre_pos, len(full_text)):
            file_w.write(full_text[j])
        write_code_se(file_w, -1)
        file_w.write('</BODY></HTML>')
        file_w.close()
    except Exception:
        print("Oops...")
