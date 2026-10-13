# ⚡ Bitset-Accelerated Subset Sum Solver for Banking Transaction Balancing

[![Python Version](https://img.shields.io/badge/Python-3.11%20%7C%203.12-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Complexity](https://img.shields.io/badge/Time%20Complexity-O(n%20%C2%B7%20W%20%2F%2064)-blueviolet?style=flat-square)](#computational-complexity--algorithm-design)
[![Tests](https://img.shields.io/badge/Tests-Passing-2ea44f?style=flat-square&logo=pytest&logoColor=white)](test_solver.py)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)

> A high-performance algorithmic solver for the **NP-complete Subset Sum & Multi-Way Partition Problem** accelerated via **bitwise DP state shifts**.
> 
> Engineered and deployed in production at **Academia Ítaca** to partition daily peer-to-peer micro-transactions (e.g., Bizum) across multiple accounts to satisfy statutory monthly transaction quotas and balance targets.

---

## 💡 The Real-World Engineering Problem

In Spain, peer-to-peer instant payment platforms (Bizum) and banking regulations enforce strict monthly transaction caps on institutional and business accounts:
- Maximum number of incoming operations per account per month (e.g. 60 transactions cap).
- Hard limits on cumulative incoming volume to comply with banking compliance triggers.

When handling hundreds of private tutoring transactions:
- Naive round-robin distribution leaves accounts unbalanced or violates operation counts.
- Greedy heuristics frequently fail to find exact split combinations, leading to account starvation or regulatory overflow.

To achieve optimal multi-account balance:
$$\min \left| \sum_{x \in A} x - \sum_{y \in B} y \right| \quad \text{subject to } |A| \le K_A, \, |B| \le K_B$$

---

## 🧮 Computational Complexity & Algorithm Design

The classic **Subset Sum** problem is NP-complete. 

### Comparison of Approaches

| Approach | Time Complexity | Space Complexity | Practical Limit ($n$) |
| :--- | :--- | :--- | :--- |
| **Naive Recursion / Backtracking** | $\mathcal{O}(2^n)$ | $\mathcal{O}(n)$ | $n \approx 30$ |
| **Meet-in-the-Middle** | $\mathcal{O}(2^{n/2} \log 2^{n/2})$ | $\mathcal{O}(2^{n/2})$ | $n \approx 45$ |
| **Standard DP (Table / Hash Set)** | $\mathcal{O}(n \cdot W)$ | $\mathcal{O}(W)$ | $W \le 10^5$ |
| **Bitset-Parallel DP (This Solver)** | $\mathbf{\mathcal{O}(n \cdot W / 64)}$ | $\mathbf{\mathcal{O}(W / 64)}$ | **Sub-millisecond for $n = 500, W = 10^6$** |

### The Bitwise Parallel Shift
Instead of maintaining a 2D boolean array or a hash set of reachable sums, the set of all achievable totals is represented as an arbitrary-precision bitfield:
$$\text{dp}_{i} = \text{dp}_{i-1} \lor (\text{dp}_{i-1} \ll w_i)$$

A single 64-bit CPU instruction computes 64 state transitions simultaneously:
```python
# Transition step in Python (arbitrary precision integer bitset)
dp = (dp | (dp << val)) & mask
```

---

## 🚀 Quickstart & Usage

### 1. Install & Run Tests

```bash
# Clone the repository
git clone https://github.com/MiguelMartinVieira/bitset-subset-sum-balancer.git
cd bitset-subset-sum-balancer

# Run tests with uv or pytest
uv run --with pytest pytest test_solver.py
```

### 2. Basic Example

```python
from solver import BitsetSubsetSum

# Transaction amounts in cents (e.g., €15.00, €25.50, etc.)
transactions = [1500, 2550, 4000, 5000, 7500]
solver = BitsetSubsetSum(transactions)

# 1. Decision Problem: Is an exact total of €65.50 achievable?
print(solver.can_partition_exact(6550))  # True (1550 + 5000)

# 2. Subset Recovery: Find the exact items
subset = solver.find_subset_exact(6550)
print(subset)  # [1550, 5000]

# 3. Two-Account Balancing: Partition transactions with minimal difference
acc_a, acc_b, diff = solver.partition_two_accounts()
print(f"Account A: {acc_a} (Sum: {sum(acc_a)})")
print(f"Account B: {acc_b} (Sum: {sum(acc_b)})")
print(f"Difference: €{diff / 100:.2f}")
```

---

## 📁 Repository Structure

```
bitset-subset-sum-balancer/
├── solver.py        # Core BitsetSubsetSum engine
├── test_solver.py   # Unit test suite verifying boundary conditions
├── pyproject.toml   # Modern packaging configuration
└── README.md        # Technical explanation & complexity analysis
```

---

## 📄 License & Attribution

Designed and engineered by **Miguel Martín Vieira** — Undergraduate in Mathematical Engineering & AI at **Comillas-ICAI**.  
Distributed under the MIT License.
