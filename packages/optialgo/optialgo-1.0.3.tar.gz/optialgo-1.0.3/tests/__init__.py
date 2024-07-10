import sys
import os


def checkPath():
    path = "/home/lopyu/opensource/optialgo"
    if path not in sys.path:
        sys.path.append(path)

