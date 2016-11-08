import os
import os.path
import torchfile
import json
import numpy.random as nprnd

from random import randint

# It builds a url from a given local path


def get_url(rel_path):
    split = rel_path.split("/")
    res = offset
    for i in range(len(split) - 3, len(split)):
        if i == len(split) - 1:
            res += split[i]
        else:
            res += split[i] + "/"
    return res


def load_data(ds):
    # Some vars of the data set
    ds = data_train
    ds_index = ds['index']
    ds_paths = ds['path']

    # Get three classes randomly
    c_1 = randint(0, len(ds_index))
    c_2 = randint(0, len(ds_index))
    c_3 = randint(0, len(ds_index))

    # Get the index of three images from the classes (c_1, c_2, c_3) randomly
    ref_idx = randint(int(ds_index[c_1][0]), int(ds_index[c_1][1]))
    A_idx = randint(int(ds_index[c_2][0]), int(ds_index[c_2][1]))
    B_idx = randint(int(ds_index[c_3][0]), int(ds_index[c_3][1]))

    # Get the paths of the images
    ref_i = ds_paths[ref_idx]
    A_i = ds_paths[A_idx]
    B_i = ds_paths[B_idx]

    return ref_i, A_i, B_i

# Get the data of the images, indexes, labels...
offset = "https://raw.githubusercontent.com/mlagunas/simple-amt/master/full-icons/"
dataset = torchfile.load("/home/mlagunas/TFM/DML_icons/data/full-dataset.t7")
data_train = dataset['train']
data_test = dataset['test']
data_val = dataset['val']

# Configuration variables for creating the hit
n_hits = 3
n_task = 5
n_randoms = 1 if n_task < 10 else n_task / 10

# get the easy triplets
with open("image_sentence/easy_triplets.json") as data_file:
    easy_triplets = json.load(data_file)

# global vars to store json objets
output = ""
output_local = []

for i in range(n_hits):
    output_local.append(0)
for j in range(n_hits):
    # Get the random indexes to place the easy images and detect spammers
    random_index = []
    summ = 0
    for i in range(n_randoms):
        rnd = randint(0, n_task - 1) if n_randoms == 1 else randint(
            5, n_task / n_randoms)
        random_index.insert(i, summ + rnd)
        summ += (n_task / n_randoms)

    # Start building hte JSON
    output += "["
    aux = {}
    aux["hit_id"] = ""
    aux["easy_samples"] = random_index
    aux["triplets"] = []
    answer = []

    # Configuration of the rndm easy triplets
    rnd_idx = 0
    nprnd.shuffle(easy_triplets)
    output += "["

    for i in range(len(random_index)):
        if i == len(random_index) - 1:
            output += str(random_index[i])
        else:
            output += str(random_index[i]) + ","

    output += "], ["

    for i in range(n_task):
        if i in random_index:  # Get easy sample for spammers
            ans = easy_triplets[rnd_idx][0]
            ref_i = easy_triplets[rnd_idx][1]
            A_i = easy_triplets[rnd_idx][2]
            B_i = easy_triplets[rnd_idx][3]
            answer.append(ans)
            rnd_idx += 1
        else:
            ref_i, A_i, B_i = load_data(data_train)
        aux["triplets"].append([ref_i, A_i, B_i])
        # Building the output
        if i == n_task - 1:
            output += "[ \"" + get_url(ref_i) + "\", \"" + \
                get_url(A_i) + "\", \"" + get_url(B_i) + "\"] "
        else:
            output += "[\" " + get_url(ref_i) + "\", \"" + \
                get_url(A_i) + "\", \"" + get_url(B_i) + "\"], "

    output += "], ["
    for i in range(len(answer)):
        if i == len(answer) - 1:
            output += "\"" + answer[i] + "\""
        else:
            output += "\"" + answer[i] + "\"" + ","

    output_local[j] = aux
    output += "]]\n"

# write file with the output generated
f = open('image_sentence/inputs.json', 'w')
f.write(output)  # python will convert \n to os.linesep
f.close()  # you can omit in most cases as the destructor will call it

with open('image_sentence/inputs_local.json', 'w') as outfile:
    json.dump(output_local, outfile)
