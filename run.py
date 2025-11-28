#!flask/bin/python
from app import app
import shutil,os

d = "./CLI_examples"

shutil.rmtree(d, ignore_errors=True)  # remove if exists (no error if not)
os.makedirs(d)                        # recreate empty dir

d = "./shots"
shutil.rmtree(d, ignore_errors=True)  # remove if exists (no error if not)
os.makedirs(d)                        # recreate empty dir

d = "./shots/pie"
shutil.rmtree(d, ignore_errors=True)  # remove if exists (no error if not)
os.makedirs(d)                        # recreate empty dir

d = "./temp_figs"
shutil.rmtree(d, ignore_errors=True)  # remove if exists (no error if not)
os.makedirs(d)                        # recreate empty dird)

d = "./comp_analysis"
shutil.rmtree(d, ignore_errors=True)  # remove if exists (no error if not)
os.makedirs(d)                        # recreate empty dir

app.run(host='127.0.0.1',port=8080,debug=True)
