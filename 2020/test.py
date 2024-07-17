

result = 0
for i in range(1, 8):
    for j in range(0, 10):
        if i < j and j not in (1, 3, 5, 7, 9):
            print(str(i)+"+"+str(j))
            result += 1
print(result)
