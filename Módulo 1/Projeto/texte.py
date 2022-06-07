def n_fibo(n, memo = [0, 1]):
    if len(memo) == n:
        return memo[-1]
    else:
        memo.append(memo[-2] + memo[-1])
        return n_fibo(n, memo)

print(n_fibo(10))