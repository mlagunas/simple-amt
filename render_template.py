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
    for i, line in enumerate(args.input_json_file):
        hit_input = json.loads(line.strip())
        easy_qs.append(hit_input[0])
        inputs.append(hit_input[1])
        answer_qs.append(hit_input[2])

    html = template.render({'input': json.dumps(
        inputs), 'easy_q': json.dumps(easy_qs), 'answer_q': json.dumps(answer_qs)})

    with open(os.path.join(output_dir, args.html_template), 'w') as f:
        f.write(html)
