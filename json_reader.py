from __future__ import division
import json
import argparse
import simpleamt
import itertools

parser = argparse.ArgumentParser(parents=[simpleamt.get_parent_parser()])
args = parser.parse_args()
mtc = simpleamt.get_mturk_connection_from_args(args)

def read_multiple_json(json_file):
    data = {}
    i = 0
    with open(json_file) as f:
        for line in f:
            while True:
                try:
                    jfile = json.loads(line)
                    data[i] = jfile
                    i += 1
                    break
                except ValueError:
                    # Not yet a complete JSON value
                    line += next(f)
    return data

train_f = 5
easy_f = 1
results_file = "examples/image_sentence/results_50_100.json"
results_file2 = "examples/image_sentence/results_100_150.json"
train_n = 4
easy_n = 7
train_margin = 1 - (train_f/train_n) - 0.01
easy_margin = 1 - (easy_f/easy_n) - 0.01
# print train_margin, easy_margin
# train_margin = 0.49
# easy_margin = 0.
data_mturk1 = read_multiple_json(results_file)
data_mturk2 = read_multiple_json(results_file2)
data_mturk = []
for i in range(len(data_mturk1)):
    data_mturk.append(data_mturk1[i])
for i in range(len(data_mturk2)):
    data_mturk.append(data_mturk2[i])
print len(data_mturk)
# data_mturk = read_multiple_json(results_file)
train_failed = 0
easy_failed = 0
total_failed = 0
#
# a = float(6/7)
# print a
money = 0
money_rej = 0
rejected_asgm = []
for i in range(len(data_mturk)):
    fail = False
    if float(data_mturk[i]['train_acc']) < train_margin:
        train_failed += 1
        fail = True
    if float(data_mturk[i]['easy_acc']) < easy_margin:
        easy_failed += 1
        fail = True
    if fail:
        print ("worker_id " + data_mturk[i]['worker_id']), "Asgm_id " + data_mturk[i]['assignment_id'], "hit_id " + data_mturk[i]['hit_id']
        total_failed += 1
        rejected_asgm.append(data_mturk[i]['assignment_id'])
        money_rej += 0.28
    else:
        money += 0.28

print "train", train_failed
print "easy" ,easy_failed
print "Rejected", total_failed
print "$ to pay(in theory):", money
print "rejected $(in theory):", money_rej
with open('rejected.json', 'w') as outfile:
    json.dump(rejected_asgm, outfile)
