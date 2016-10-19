import json


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
fi = "image_sentence/results.json"
data = {}
with open(fi) as f:
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

        # do something with jfile
for i in range(len(data)):
    res = data[i]["output"]
    for j in range(len(res)):
data

assignments_id = data[:]["assignment_id"]
