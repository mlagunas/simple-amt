import os
import os.path
import torchfile
import json
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

# Loads a triplet from a given dataset
def load_data(ds):
    # Getting styles
    ref_class, ref_style = ds.style_list[
        randint(0, len(ds.style_list) - 1)].split("/")
    oth_class, oth_style = ds.style_list[
        randint(0, len(ds.style_list) - 1)].split("/")
    while ref_style == oth_style and ref_class == oth_class:
        oth_class, oth_style = ds.style_list[
            randint(0, len(ds.style_list) - 1)].split("/")

    # Creating the triplet
    ref_img = ds.style[ref_class][ref_style][
        randint(0, len(ds.style[ref_class][ref_style]) - 1)]
    dis_img = ds.style[oth_class][oth_style][
        randint(0, len(ds.style[oth_class][oth_style]) - 1)]
    sim_img = ds.style[ref_class][ref_style][
        randint(0, len(ds.style[ref_class][ref_style]) - 1)]
    while ref_img == sim_img:
        sim_img = ds.style[ref_class][ref_style][
            randint(0, len(ds.style[ref_class][ref_style]) - 1)]
    return ref_img, dis_img, sim_img

offset = "https://raw.githubusercontent.com/mlagunas/simple-amt/master/FULL_ICONS/"
dataset = torchfile.load("/home/mlagunas/TFM/DML_icons/data/icons_full.t7")
dataset_easy = torchfile.load(
    "/home/mlagunas/TFM/DML_icons/data/icons_small.t7")
n_hits = 3
n_task = 4

output = ""
output_local = []
for i in range(n_hits):
    output_local.append(0)
for j in range(n_hits):
    output += "["
    easy_sample = randint(n_task / 4 + 1, n_task / 4 * 3)
    aux = {}
    aux["hit_id"] = ""
    aux["easy_sample"] = easy_sample
    aux["triplets"] = []
    for i in range(n_task):
        if i == easy_sample:  # Get easy sample for spammers
            ref_img, dis_img, sim_img = load_data(dataset_easy)
        else:
            ref_img, dis_img, sim_img = load_data(dataset)
        aux["triplets"].append([ref_img, dis_img, sim_img])
        # Building the output
        if i == n_task - 1:
            output += "[ \"" + get_url(ref_img) + "\", \"" + \
                get_url(dis_img) + "\", \"" + get_url(sim_img) + "\"] "

        else:
            output += "[\" " + get_url(ref_img) + "\", \"" + \
                get_url(dis_img) + "\", \"" + get_url(sim_img) + "\"], "
    output_local[j] = aux
    output += "]\n"

# write file with the output generated
f = open('image_sentence/inputs.json', 'w')
f.write(output)  # python will convert \n to os.linesep
f.close()  # you can omit in most cases as the destructor will call it
with open('image_sentence/inputs_local.json', 'w') as outfile:
    json.dump(output_local, outfile)
