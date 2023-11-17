import filecmp

f1 = "my1.txt"
f2 = "my.txt"

# shallow comparison
result = filecmp.cmp(f1, f2)
print(result)
# deep comparison
result = filecmp.cmp(f1, f2, shallow=False)
print(result)
