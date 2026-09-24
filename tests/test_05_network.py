# test_05_network.py
echo("Running network checks")
ping("1.1.1.1", count=2)
dig("example.com")
nslookup("example.com")
ifconfig()
ip("addr")
