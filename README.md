# sbdkparse.py is used to port wrappers from old sdk to new sdk. If you want to do that, follow the next few steps.

# First git clone desired sbg toolkit or tool which you want to port. 
git clone https://github.com/sbg/repo_name.git

# Open terminal, start vagrant, and in vagrant change dir to that repo.
vagrant up
vagrant ssh
cd repo_name

# From __init__.py of package choose wrapper(s) you want to parse, by commenting(#) others. 
# If you want to parse whole package, leave __init__.py intact. 

# SSH on image if that repo and change dir to /sbgenomics.
sbg sh
cd /sbgenomics

# Install required python packages for using sbgsdk.cli, which will allow us to output out_schema.json,
# which contains wrapper(s) to be parsed.
pip install .

# Edit attrdef.py with any text editor, by deleting "if k[0] != '_'" on the last line of code, and save changed python file. 
# This will allow us to use "_extra":{"arg"}.
nano /usr/local/lib/python2.7/dist-packages/sbgsdk/schema/attrdef.py

# Output out_schema.json with next code. sbg_package_name = project_name from state.json in .sbdk folder. 
# (If errors occur look in Errors section)
/usr/bin/python -m sbgsdk.cli --logging-config .sbdk/logging.json schema --package sbg_package_name > out_schema.json
exit(ctrl+d) and DON'T COMMIT CONTAINER(press n)!

# Copy out_schema.json contents to in_schema.json in rabixator folder.
# Run the parser and follow instructions on screen.
python sbdkparse.py

# Parser is parsing only schema.py from old sdk, which include Inputs, Params and Outputs. 
# If some of Input or Param doesn't have prefix(arg), it will ask you to enter it

Errors:
No such file or directory: '.sbdk/logging.json': 
Remove '.sbdk/logging.json' and '--logging-config' from cmd line.

Usage:
python sbdkparse.py
