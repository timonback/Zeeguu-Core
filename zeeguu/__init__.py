# -*- coding: utf8 -*-
import os

log_file = os.path.expanduser("~/.config/zeeguu/zeeguu_log.txt")


def log(text):
    with open(log_file, "a") as myfile:
        myfile.write((text+"\n"))
