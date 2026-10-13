"""Unit tests for the Bitset Subset Sum solver."""

import pytest
from solver import BitsetSubsetSum


def test_can_partition_exact():
    transactions = [15, 25, 40, 50, 75]
    solver = BitsetSubsetSum(transactions)

    assert solver.can_partition_exact(65) is True   # 25 + 40
    assert solver.can_partition_exact(100) is True  # 25 + 75
    assert solver.can_partition_exact(105) is True  # 15 + 40 + 50
    assert solver.can_partition_exact(12) is False  # Minimum item is 15
    assert solver.can_partition_exact(101) is False # Impossible with these numbers
    assert solver.can_partition_exact(0) is True


def test_find_subset_exact():
    transactions = [12, 18, 30, 45, 60]
    solver = BitsetSubsetSum(transactions)

    subset = solver.find_subset_exact(48)
    assert subset is not None
    assert sum(subset) == 48
    for item in subset:
        assert item in transactions


def test_partition_two_accounts():
    transactions = [20, 30, 40, 50, 60] # Total = 200, perfect split = 100 & 100
    solver = BitsetSubsetSum(transactions)

    acc_a, acc_b, diff = solver.partition_two_accounts()
    assert sum(acc_a) + sum(acc_b) == 200
    assert abs(sum(acc_a) - sum(acc_b)) == diff
    assert diff == 0  # e.g., (40 + 60) vs (20 + 30 + 50)
