# sbdkparse.py

git clone https://github.com/sbg/repo_name.git
cd repo_name
from __init__.py choose wrapper you want to parse, comment(#) others.
sbg sh
pip install .
nano /usr/local/lib/python2.7/dist-packages/sbgsdk/schema/attrdef.py
delete  "if k[0] != '_'" on the last line of code, and save changed python file.
/usr/bin/python -m sbgsdk.cli --logging-config .sbdk/logging.json schema --package sbg_package_name > schema.json
exit(ctrl+d) and DON'T COMMIT CONTAINER(press n)!

mv schema.json to 'rabixator'
python sbdkparse.py

FAQ:
sbg_package_name = project_name from state.json in .sbdk folder

Errors:
No such file or directory: '.sbdk/logging.json': 
Remove '.sbdk/logging.json' and '--logging-config' from cmd line.

Usage:
python sbdkparse.py
