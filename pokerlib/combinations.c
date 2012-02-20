#!/usr/bin/env python
# port to C...

def comb(c, n, k):
    j = k - 1

    if c[j] < n - 1:
        c[j] += 1
        return True

    while (j >= 0) and (c[j] >= n - k + j):
        j -= 1

    if j < 0:
        return False

    c[j] += 1

    for j in range(j + 1, k):
        c[j] = c[j-1] + 1

    return True


if __name__ == "__main__":
    c = [0, 1, 2]
    print(c)
    while comb(c, 5, 3):
        print(c)
