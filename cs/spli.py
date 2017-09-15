raw = ["201708141002:[3]", "201708141003:[3,1]", "201708141004:[3,1]", "201708141005:[0,1]"]

import re

ls = []
for x in raw:
    raw = x.split(':')[0]
    ls1 = []
    for x in eval(x.split(':')[1]):
        ls1.append(raw+':'+str(x))
    ls.append(ls1)
print(ls)


    # for y in splited:
    #     ls.apend(x)
