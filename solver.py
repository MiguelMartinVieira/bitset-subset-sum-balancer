"""
High-Performance Bitset Dynamic Programming Solver for Subset Sum and Transaction Balancing.

Used in production by Academia Ítaca to partition high-volume peer-to-peer micro-transactions
(e.g., Bizum) across multiple institutional accounts to comply with statutory monthly transaction
limits and balance targets.
"""

from typing import List, Optional, Tuple


class BitsetSubsetSum:
    """
    Optimized Bitset Dynamic Programming solver for the Subset Sum problem:
    Given a target capacity W and a multiset of integers S = {w_1, w_2, ..., w_n},
    find a subset S' ⊆ S such that sum(S') == W (or maximizes sum <= W).

    Complexity:
        - Time: O(n * W / 64) using 64-bit integer bitwise shifts.
        - Space: O(n * W / 64) for exact subset recovery, or O(W / 64) for decision problem.
    """

    def __init__(self, values: List[int]):
        """
        Initialize the solver with a list of non-negative integer transaction amounts (e.g., in cents).
        """
        self.values = [v for v in values if v > 0]

    def can_partition_exact(self, target: int) -> bool:
        """
        Solves the decision problem: Can target be formed by any subset?
        Uses Python's arbitrary-precision integers as dynamic bitsets.
        """
        if target < 0:
            return False
        if target == 0:
            return True

        # bitset where bit k represents whether sum k is achievable
        # dp = 1 represents 2^0 = 1 (sum 0 is achievable)
        dp = 1
        mask = (1 << (target + 1)) - 1

        for val in self.values:
            if val <= target:
                dp = (dp | (dp << val)) & mask
                if (dp >> target) & 1:
                    return True

        return bool((dp >> target) & 1)

    def find_subset_exact(self, target: int) -> Optional[List[int]]:
        """
        Solves the search problem: Reconstructs the exact subset of items that sum to `target`.
        Returns None if no exact subset exists.
        """
        if target < 0:
            return None
        if target == 0:
            return []

        # Keep track of states for backtracking
        # history[i] stores the bitset after considering item i
        history = []
        dp = 1
        mask = (1 << (target + 1)) - 1

        for val in self.values:
            prev_dp = dp
            dp = (dp | (dp << val)) & mask
            history.append((val, prev_dp))

        if not ((dp >> target) & 1):
            return None  # Target not reachable

        # Backtrack to reconstruct the subset
        curr_target = target
        chosen = []

        for val, prev_dp in reversed(history):
            if curr_target >= val and ((prev_dp >> (curr_target - val)) & 1):
                # We can achieve the remaining sum without this item OR with this item.
                # If removing it leaves an achievable state in prev_dp, we select it.
                if not ((prev_dp >> curr_target) & 1):
                    chosen.append(val)
                    curr_target -= val
                else:
                    # Ambiguity resolved greedily or by necessity
                    pass

        return chosen

    def partition_two_accounts(self) -> Tuple[List[int], List[int], int]:
        """
        Splits transactions across two accounts to achieve minimal discrepancy |Sum(A) - Sum(B)|.
        Returns: (account_a_items, account_b_items, discrepancy)
        """
        total = sum(self.values)
        half = total // 2

        # Find closest achievable sum <= half
        dp = 1
        mask = (1 << (half + 1)) - 1
        history = []

        for val in self.values:
            prev = dp
            dp = (dp | (dp << val)) & mask
            history.append((val, prev))

        # Find best sum <= half
        best_sum = half
        while best_sum > 0 and not ((dp >> best_sum) & 1):
            best_sum -= 1

        # Reconstruct account A
        curr = best_sum
        account_a = []
        remaining = list(self.values)

        for val, prev in reversed(history):
            if curr >= val and ((prev >> (curr - val)) & 1):
                if not ((prev >> curr) & 1) or (curr == val):
                    account_a.append(val)
                    remaining.remove(val)
                    curr -= val

        account_b = remaining
        discrepancy = abs(sum(account_a) - sum(account_b))
        return account_a, account_b, discrepancy
