from nest_asyncio import apply

apply()
import subprocess

# install node
subprocess.run(
    args="curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash",
    shell=True,
)
subprocess.run(
    args="""export NVM_DIR="$([ -z "${XDG_CONFIG_HOME-}" ] && printf %s "${HOME}/.nvm" || printf %s "${XDG_CONFIG_HOME}/nvm")"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh" # This loads nvm""",
    shell=True,
)

subprocess.run(
    args="nvm install --lts",
    shell=True,
)
subprocess.run(
    args="nvm use --lts",
    shell=True,
)

# install npx
subprocess.run(
    args="npm i google-it",
    shell=True,
)

subprocess.run(
    args="npm i percollate",
    shell=True,
)


def warmup():
    pass
