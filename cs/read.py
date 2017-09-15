import os

import re

def path_url():
    path = "/Users/user/work/链接/1.txt"
    with open(path,'r') as f:
        fr = f.readlines()
        [print(x.strip()) for x in fr]
        return [x.strip() for x in fr if x.strip()!='']

# path_url()
