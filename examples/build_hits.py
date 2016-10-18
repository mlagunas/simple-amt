import os
import os.path
import torchfile
from random import randint

def get_url(rel_path):
    split = rel_path.split("/")
    res = offset
    for i in range(len(split) - 3, len(split)):
        if i == len(split) - 1:
            res += split[i]
        else:
            res += split[i] + "/"
    return res
offset = "https://raw.githubusercontent.com/mlagunas/simple-amt/master/SMALL_ICONS/"
dataset = torchfile.load("/home/mlagunas/TFM/DML_icons/data/SMALL_ICONS.t7")
n_hits = 3
n_task = 3

output = ""
for j in range(n_hits):
    output += "["
    for i in range(n_task):
        # Getting styles
        ref_style = dataset.style_list[randint(0, len(dataset.style_list) - 1)]
        oth_style = dataset.style_list[randint(0, len(dataset.style_list) - 1)]
        while ref_style == oth_style:
            oth_style = dataset.style_list[
                randint(0, len(dataset.style_list) - 1)]

        # Creating the triplet
        ref_img = dataset.style[ref_style][
            randint(0, len(dataset.style[ref_style]) - 1)]
        dis_img = dataset.style[oth_style][
            randint(0, len(dataset.style[oth_style]) - 1)]
        sim_img = dataset.style[ref_style][
            randint(0, len(dataset.style[ref_style]) - 1)]
        while ref_img == sim_img:
            sim_img = dataset.style[ref_style][
                randint(0, len(dataset.style[ref_style]) - 1)]

        # Building the output
        if i == n_task - 1:
            output += "[ \"" + get_url(ref_img) + "\", \"" + \
                get_url(dis_img) + "\", \"" + get_url(sim_img) + "\"] "
        else:
            output += "[\" " + get_url(ref_img) + "\", \"" + \
                get_url(dis_img) + "\", \"" + get_url(sim_img) + "\"], "

    output += "]\n"

#write file with the output generated
f = open('image_sentence/inputs.json', 'w')
f.write(output)  # python will convert \n to os.linesep
f.close()  # you can omit in most cases as the destructor will call it
