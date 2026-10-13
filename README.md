# Bitset Subset Sum Solver

[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue?style=flat-square)](https://python.org)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen?style=flat-square)](test_solver.py)
[![License: MIT](https://img.shields.io/badge/license-MIT-green?style=flat-square)](LICENSE)

A solver for the Subset Sum problem (NP-complete) using bitset-parallel dynamic programming. Runs in $O(n \cdot W / 64)$ time by exploiting Python's arbitrary-precision integers as bitfields.

## Why I built this

I run a tutoring business ([Academia Ítaca](https://itacacademia.com)) where students pay via Bizum (Spain's peer-to-peer payment system). Bizum has hard monthly caps — max number of incoming transactions and max volume per account. With hundreds of transactions a month across multiple bank accounts, I needed to partition them optimally.

Greedy approaches fail to find exact splits. Brute force is exponential. Standard DP works but is slow for large target sums. The bitset approach compresses the DP table into a single integer and processes 64 states per CPU instruction:

$$\text{dp}_{i} = \text{dp}_{i-1} \lor (\text{dp}_{i-1} \ll w_i)$$

## Performance comparison

| Approach | Time | Practical limit |
|:---|:---|:---|
| Brute force | $O(2^n)$ | ~30 items |
| Meet in the middle | $O(2^{n/2} \log 2^{n/2})$ | ~45 items |
| Standard DP | $O(n \cdot W)$ | $W \le 10^5$ |
| **Bitset DP (this)** | $O(n \cdot W / 64)$ | Sub-ms for $n=500, W=10^6$ |

## Usage

```python
from solver import BitsetSubsetSum

transactions = [1500, 2550, 4000, 5000, 7500]  # amounts in cents
solver = BitsetSubsetSum(transactions)

# Can we hit exactly €65.50?
solver.can_partition_exact(6550)  # True

# Which items?
solver.find_subset_exact(6550)  # [1500, 5050] or similar

# Split into two accounts with minimal difference
acc_a, acc_b, diff = solver.partition_two_accounts()
```

## Running tests

```bash
git clone https://github.com/MiguelMartinVieira/bitset-subset-sum-balancer.git
cd bitset-subset-sum-balancer
uv run --with pytest pytest test_solver.py
```

## Structure

```
├── solver.py        # Core solver
├── test_solver.py   # Test suite
├── pyproject.toml
└── README.md
```

## License

MIT
