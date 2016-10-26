import json

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

# {
#     "assignment_id": "33CUSNVVNOIUNKTKJE64U3MT6MQ88B",
#     "output": [{
#         "time_used": 4751,
#         "selection": 3,
#         "triplet_id": 0
#     }, {
#         "time_used": 3159,
#         "selection": 3,
#         "triplet_id": 1
#     }, {
#         "time_used": 3311,
#         "selection": 3,
#         "triplet_id": 2
#     }],
#     "worker_id": "A1U9ICW77279OX",
#     "hit_id": "3Y40HMYLL1OGDY3B4MEZIAPVHPXXUJ"
# }

i = 0
data_mturk = read_multiple_json("image_sentence/results.json")
with open("image_sentence/inputs_local.json") as data_file:
    data_local = json.load(data_file)

if data_mturk[1]["hit_id"] == data_local[1]["hit_id"]:
    data_mturk[1]["output"][]
