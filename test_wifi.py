from subprocess import Popen, PIPE

wifi_score_command = ['/usr/bin/ndsctl', 'status']
score_process = Popen(wifi_score_command, stdout=PIPE)
stdout = score_process.communicate()
print(stdout)
score_process.kill()
