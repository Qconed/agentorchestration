# Virtual environment practices

The file requirements.txt will contain the dependencies to use 

create the virtual environment using venv (sytem dependencies-free)

```bash
python3 -m venv .venv
source .venv/bin/activate # activate the environment (windows: .venv\Scripts\activate)
pip install -r requirements.txt
```

Installing packages and adding to the dependencies

```bash
source .venv/bin/activate # activate the environment (windows: .venv\Scripts\activate)
pip install <package>
pip freeze > requirements.txt # export the current dependencies to the requirements.txt
```

Uninstalling packages and adding to the dependencies
```bash
source .venv/bin/activate
pip uninstall <package>
pip freeze > requirements.txt
```

to do a clean remove and install of dependencies:
```bash
# Remove everything and start over
pip uninstall -y -r <(pip freeze)
pip install -r requirements.txt # ensure for this requirements.txt is up to date with git !
```


# Api Keys

Copy the .env.example to give you a template, rename it `.env` and write your API keys in it.
Make sure .env is written in the .gitignore file !!

