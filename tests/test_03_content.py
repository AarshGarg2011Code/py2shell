# test_03_content.py
echo("Inspecting log files")
touch("server.log")
head("server.log", lines=5)
tail("server.log", lines=5)
grep("ERROR", "server.log")
wc("server.log")
