# Algo Invest & Trade

This project solves an optimization problem: regarding a set of shares where every share has a cost and a two years profit; a maximum budget; what is the best subset of shares that we can buy?

## Bruteforce solution

The `bruteforce.py` file implements the naïve approach which calculates every possible subset and chooses the one that gives the best two years profit. It has a time complexity of `O(2^n)` and a space complexity of `O(n)`.

```
❯ py bruteforce.py -t
3.107956013001967
```

## Dynamic Progamming

This problem is a variant of the Knapsack problem, thus the `optimized.py` solution implements a bottom up approach to find the best set of shares. Here the time and space complexity are tied to the size of our grid which would be `n * m` where `n` is the number of shares available and `m` the number of sub budgets we consider.

The current implementation has a rather simple approach, to compute `m` take the minimum step that exists between two share's cost, so we are sure to not miss any subproblem.

Note that we might compute an excessive amount of subproblems in some scenarios, the spacing between the different sub budgets is definitely a bottleneck that would diserve to be improved.

```
> py optimized.py -t
0.014617622997320723

> py optimized.py --dataset2

Shares                                                                                                                                                                                                                              Total Cost    2 years profit
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------  ------------  ----------------
Share-ANFX, Share-PATS, Share-LXZU, Share-YFVZ, Share-ZOFA, Share-FWBE, Share-PSMF, Share-NDKR, Share-ALIY, Share-JWGF, Share-ROOM, Share-JGTW, Share-XQII, Share-VCXT, Share-UPCV, Share-PLLK, Share-FAPS, Share-LFXB, Share-IXCI           500            198.06
```

FYI: the second dataset takes about 2 minutes and 30 seconds on my machine.

Do not try the `--dataset1` or `--dataset2` with the bruteforce solution, this is way too slow.

## Source files

Different source files are provided,

* `shares.csv` file is an easy one, no floating numbers nor corrupted data
* `debug.csv` can be used to analyze the program on a lazy human scale
* the other two csv files are bloated with non-sense such as negative or null costs for shares or zero profit, this garbage data is filtered by our script before it proceeds, plus they involve a lot of float numbers which causes our DP approach to be slower than we would like it (still a billion time faster than bruteforce though)
