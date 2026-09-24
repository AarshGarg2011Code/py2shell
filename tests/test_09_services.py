# test_09_services.py
echo("Checking service statuses")
systemctl("status", "nginx")
journalctl(unit="nginx", lines=10)
netstat("-tulpn")
ss("-tulpn")
