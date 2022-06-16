a = [[1,2],[3,4],[5,3]]

for i in range(len(a)):
    for j in range(1):
        if i%2 != 0:
            print(a[i][1])
        else:
            print(a[i][0])