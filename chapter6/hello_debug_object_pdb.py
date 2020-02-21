class Z: pass
zz = Z()

def add(x,y):
    import pdb;pdb.set_trace()
    print(f"The value of x: {x}")
    print(f"The value of y: {y}")
    return x+y

result = add(3,zz)
print(result)