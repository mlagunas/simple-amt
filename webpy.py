import web
import codecs
from web import form
import json

web.config.debug = False

# in_use = []
# for i in range(num_hits):
#     in_use.append(False)
urls = ("/",  "Icons",
        "/end", "End")
web.app = web.application(urls, globals())
web.idx = 22
web._HITS = 50
# if web.config.get('_session') is None:
#     store = web.session.DiskStore('sessions')
#     session = web.session.Session(web.app, store, initializer={'count': 0, '_HITS':3})
#     web.config._session = session
# else:
#     session = web.config._session

web.config.session_parameters['timeout'] = 60 * 10,


class Icons:

    def GET(self):
        # print idx
        print "idx " + str(web.idx)
        f = codecs.open(
            "/home/mlagunas/TFM/simple-amt/rendered_templates/image_sentence_" + str(web.idx) + ".html", 'r')

        if web.idx == web._HITS - 1:
            web.idx = 0
        else:
            web.idx += 1

        content = f.read()
        return content

    def POST(self):

        # build JSON from post method
        data = web.input()
        data['assignmentId'] = data.assignmentId
        data['output'] = json.loads(data.output)
        data['train_acc'] = data.train_acc
        data['easy_acc'] = data.easy_acc

        with open("examples/image_sentence/results_local.json", "a") as myfile:
            myfile.write(json.dumps(data)) + ",\n"

        raise web.seeother('/end')


class End:

    def GET(self):
        return "The test has finished Thanks for your time. We hope you enjoyed it!."

if __name__ == "__main__":
    web.app.run()
