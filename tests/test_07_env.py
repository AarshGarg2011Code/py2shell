# test_07_env.py
echo("Setting up environment variables")
export("MODE", "production")
export("PORT", "8080")
env_mode = sh("MODE")
echo(env_mode)
env()
