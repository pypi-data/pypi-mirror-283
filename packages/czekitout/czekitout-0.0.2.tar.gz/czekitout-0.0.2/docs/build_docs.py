# Code adopted from
# ``https://github.com/ThoSe1990/SphinxExample/blob/main/docs/build_docs.py``.

import subprocess
import yaml 
import os

def build_doc(version, language, tag):
    os.environ["current_version"] = version
    os.environ["current_language"] = language
    subprocess.run("git checkout " + tag, shell=True)
    subprocess.run("git checkout main -- conf.py", shell=True)
    subprocess.run("git checkout main -- versions.yaml", shell=True)
    os.environ["SPHINXOPTS"] = "-D language='{}'".format(language)
    subprocess.run("make html", shell=True)    

def move_dir(src, dst):
    subprocess.run(["mkdir", "-p", dst])
    subprocess.run("mv "+src+"* "+dst, shell=True)

os.environ["build_all_docs"] = str(True)
os.environ["pages_root"] = "https://mrfitzpa.github.io/czekitout" 

build_doc("latest", "en", "main")
move_dir("./_build/html/", "../pages/")

with open("versions.yaml", "r") as yaml_file:
    docs = yaml.safe_load(yaml_file)

for version, details in docs.items():
    tag = details.get("tag", "")
    for language in details.get("languages", []): 
        build_doc(version, language, tag)
        move_dir("./_build/html/", "../pages/"+version+"/"+language+"/")
