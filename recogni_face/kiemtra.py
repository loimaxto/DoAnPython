import os
n = "1.123.jpg"
print(os.path.split(n)[-1].split(".")[0])