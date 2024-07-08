import os
import shutil


def move_file(source, destination):
    shutil.move(source, destination)


def copy_file(source, destination):
    shutil.copy(source, destination)


def rename_file(source, new_name):
    os.rename(source, new_name)


def delete_file(file_path):
    os.remove(file_path)


def create_file(file_path):
    with open(file_path, "w") as file:
        pass


def read_file(file_path):
    with open(file_path, "r") as file:
        return file.read()
