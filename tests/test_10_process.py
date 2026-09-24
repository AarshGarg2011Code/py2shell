# test_10_process.py
echo("Managing processes and remote commands")
top()
htop()
kill(1234, signal_num=9)
ssh("user@remote-host", command="uptime")
clear()
