import json
from subprocess import Popen, PIPE

wifi_score_command = ['/usr/bin/ndsctl', 'status']
score_process = Popen(wifi_score_command, stdout=PIPE)
stdout = score_process.communicate()
msg = json.loads(stdout[0].decode('utf-8'))['client_length']
print(msg)
score_process.kill()
