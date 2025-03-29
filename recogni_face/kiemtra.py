import time
begin = time.time()
count = 0
while True:
    count+=1
    if count ==10000000:
        break
end = time.time()
print(end-begin)