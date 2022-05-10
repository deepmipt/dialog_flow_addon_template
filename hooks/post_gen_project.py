#!/usr/bin/env python
# This file was got from https://github.com/s3rius/FastAPI-template/blob/master/fastapi_template/template/hooks/post_gen_project.py
import json
import os
import shutil
import subprocess

from pathlib import Path

CONDITIONAL_MANIFEST = "conditional_files.json"
REPLACE_MANIFEST = "replaceable_files.json"


def delete_resource(resource):
    if os.path.isfile(resource):
        os.remove(resource)
    elif os.path.isdir(resource):
        shutil.rmtree(resource)


def delete_resources_for_disabled_features():
    with open(CONDITIONAL_MANIFEST) as manifest_file:
        manifest = json.load(manifest_file)
        for feature_name, feature in manifest.items():
            if feature["enabled"].lower() != "true":
                text = "Removing resources for disabled feature feature_nam..."
                print(text)
                for resource in feature["resources"]:
                    delete_resource(resource)
    delete_resource(CONDITIONAL_MANIFEST)
    print("cleanup complete!")


def replace_resources():
    print("⭐ Placing resources nicely in your new project ⭐")
    with open(REPLACE_MANIFEST) as replace_manifest:
        manifest = json.load(replace_manifest)
        for target, replaces in manifest.items():
            target_path = Path(target)
            delete_resource(target_path)
            for src_file in map(Path, replaces):
                if src_file.exists():
                    shutil.move(src_file, target_path)
    delete_resource(REPLACE_MANIFEST)
    print("Resources are happy to be where they are needed the most.")


def init_repo():
    subprocess.run(["git", "init"], stdout=subprocess.PIPE)
    print("Git repository initialized.")
    subprocess.run(["git", "add", "."], stdout=subprocess.PIPE)
    print("Added files to index.")
    subprocess.run(["git", "commit", "-m", "Initial commit"], stdout=subprocess.PIPE)


if __name__ == "__main__":
    delete_resources_for_disabled_features()
    replace_resources()
    init_repo()
