import subprocess
import pathlib
import json
import slackweb

current_dir = pathlib.Path(__file__).parent.resolve()
config_json = json.load(open(str(current_dir) + '/' + 'config.json', 'r'))

def slack_notify(send_text: str):
    slack = slackweb.Slack(url=config_json['slackWebhookUrl'])
    slack.notify(text=send_text)

def main():
    try:
        subprocess.run([config_json['proconGardenerPath'] + 'procon-gardener', 'archive'], cwd=config_json['path'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except Exception as e:
        slack_notify('<!channel> エラー出てるよ！\n' + str(e))
        exit()

    try:
        res = subprocess.run(['git', 'push'], cwd=config_json['path'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except Exception as e:
        slack_notify('<!channel> エラー出てるよ！\n' + str(e))
        exit()

    if res.stderr == b'Everything up-to-date\n':
        send_text = '<!channel> 今日まだACできてないよ！'
    else:
        send_text = '今日も精進お疲れ様！'

    slack_notify(send_text)

if __name__ == '__main__':
    main()

