x = [(1,(2,3)), (4,(5,6))]



c = sorted(x, key=lambda x: x[1][0], reverse=True)

print(c)