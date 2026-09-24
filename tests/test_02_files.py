# test_02_files.py
echo("Testing file duplication and moves")
touch("data.tmp")
cp("data.tmp", "data.bak")
mv("data.tmp", "cache.tmp")
rm("cache.tmp")
ls(".", long_format=True)
