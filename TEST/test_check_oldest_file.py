#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2023/10/28 1:48
# @Author  : Luis Liu
# @Email   : myheartu@126.com
# @File    : test_check_oldest_file
# @Software: PyCharm

import os


def get_oldest_file(folder_path):
    """Returns the oldest file in the given folder.
    Args:
    folder_path: The path to the folder to search.

    Returns:
    The path to the oldest file in the folder, or None if the folder is empty.
    """
    oldest_file = None
    oldest_file_mtime = 0

    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        file_mtime = os.path.getmtime(file_path)

    if oldest_file is None or file_mtime < oldest_file_mtime:
        oldest_file = file_path
        oldest_file_mtime = file_mtime

    return oldest_file


folder_path = "/Users/LUISLIU1/PycharmProjects/pythonProject/SNOW"
oldest_file_path = get_oldest_file(folder_path)

if oldest_file_path is not None:
    print("The oldest file in the folder is:", oldest_file_path)
else:
    print("The folder is empty.")
