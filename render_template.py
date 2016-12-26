import argparse
import os
import os.path
import simpleamt
import json


if __name__ == '__main__':
    parser = argparse.ArgumentParser(parents=[simpleamt.get_parent_parser()])
    parser.add_argument('--html_template', required=True)
    parser.add_argument('--input_json_file', type=argparse.FileType('r'))
    args = parser.parse_args()

    env = simpleamt.get_jinja_env(args.config)
    template = env.get_template(args.html_template)

    output_dir = args.config['rendered_template_directory']
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    easy_qs = []
    inputs = []
    answer_qs = []
    html = []
    assignmentId = [-1]

    for i, line in enumerate(args.input_json_file):
        hit_input = json.loads(line.strip())
        assignmentId[0] = i
        html.append(template.render({'input': json.dumps(hit_input[1]), 'easy_q': json.dumps(hit_input[0]), 'answer_q': json.dumps(hit_input[2]), 'assignmentId': json.dumps(assignmentId)}))

    for i in range(len(html)):
        with open(os.path.join(output_dir, args.html_template.split(".")[0]) + "_" + str(i) + ".html", 'w') as f:
            for j in range(350,500):
                print j, html[i][j]
            f.write(html[i])
