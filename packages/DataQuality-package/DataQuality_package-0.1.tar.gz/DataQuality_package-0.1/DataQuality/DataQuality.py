
def ProcessData(n):
    if n == 0:
        return 1
    return n * ProcessData(n - 1)