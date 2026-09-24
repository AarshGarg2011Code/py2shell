# test_06_permissions.py
echo("Updating script permissions")
touch("deploy.sh")
chmod("+x", "deploy.sh")
sudo("chown", "root:root", "deploy.sh")
ls("deploy.sh", long_format=True)
