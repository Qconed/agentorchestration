# Virtual environment practices

The file requirements.txt will contain the dependencies to use 

create the virtual environment using venv (sytem dependencies-free)

```bash
pyton3 -m venv .venv
source .venv/bin/activate # activate the environment (windows: .venv\Scripts\activate)
pip install <package> # install package

deactivate # deactivate the environment
pip freeze > requirements.txt # export the current dependencies to the requirements.txt
pip install -r requirements.txt
pip uninstall <package> # uninstall package
```

> adding/removing dependency, do pip freeze, then commit the requirements.txt file

to do a clean remove and install of dependencies:

```bash
# Remove everything and start over
pip uninstall -y -r <(pip freeze)
pip install -r requirements.txt # ensure for this requirements.txt is up to date with git !
```
