import argparse
import yaml
from flask import Flask, request

from entities import Message, SlackTarget, ProgramConfig, Channel


def read_config(path: str) -> ProgramConfig:
    with open(path, 'r') as f:
        config = yaml.safe_load(f)

    # Auth keys
    auth_keys = config['auth_keys']

    # Targets
    targets = {}
    for target_name in config['targets']:
        t = config['targets'][target_name]
        if t['type'] == 'slack':
            t_parsed = SlackTarget(t['hook_url'])
        else:
            raise ValueError('Unknown target type: ' + t['type'])
        targets[target_name] = t_parsed

    # Channels
    channels = {}
    for channel_name in config['channels']:
        target_names = config['channels'][channel_name]['targets']
        for tn in target_names:
            if tn not in targets:
                raise ValueError('Unknown target: ' + tn)
        channels[channel_name] = Channel([targets[tn] for tn in target_names])

    return ProgramConfig(auth_keys, targets, channels)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('config_file', help='path to config.yml')
    args = parser.parse_args()
    print('Config file: {}'.format(args.config_file))

    program_config = read_config(args.config_file)
    app = Flask(__name__)


    @app.route('/send', methods=['POST'])
    def send():
        channel = request.json.get('channel')
        message = Message(
            request.json.get('level', 'INFO'),
            request.json.get('subject'),
            request.json.get('body')
        )
        for target in program_config.channels[channel].targets:
            target.send_message(message)
        return {
            'success': True
        }


    app.run(host='0.0.0.0', port=8080)
