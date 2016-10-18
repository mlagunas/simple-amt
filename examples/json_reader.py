import json


# "assignment_id": "3WT783CTPCNF1LH4326JNR8D4JQCBE",
# "output": [
#     "image_url": "http://www.wired.com/images_blogs/photos/uncategorized/2008/03/04/puppy.jpg",
#     "description": "White dog on the grass"
# ,
#     "image_url": "http://cdn.cutestpaw.com/wp-content/uploads/2011/11/Puppy-Power-l.jpg",
#     "description": "Black yorkshire with a white t-shirt"
# ],
# "worker_id": "A1U9ICW77279OX",
# "hit_id": "3P888QFVX301RWI2MM7YPW1D2Y2QOE"



i = 0
file = "image_sentence/results.json"
with open(file) as f:
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

print(data[0]["assignment_id"])
