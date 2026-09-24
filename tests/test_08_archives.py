# test_08_archives.py
echo("Archiving log files")
mkdir("logs")
touch("logs/app.log")
tar("-czvf", "logs_backup.tar.gz", "logs")
gzip("logs/app.log")
zip("backup.zip", "logs")
unzip("backup.zip", destination="extracted")
