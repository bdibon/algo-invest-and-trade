"""Brute force solution to find the optimal set of shares."""

from shares import load_shares_from_csv, ShareCombination, print_shares_combinations

SHARES = load_shares_from_csv('shares.csv')
MAX_COST = 500


def brute_force_shares_combinations(share_comb: ShareCombination):
    """Finds all possible ShareCombination in O(2^n)."""
    combinations = []

    def _bfsc(index=0):
        if index >= len(SHARES) or share_comb.total_cost + SHARES[index].cost > MAX_COST:
            if len(share_comb) != 0:
                combinations.append(share_comb.copy())
            return

        # Let's take this share.
        share_comb.add(SHARES[index])
        _bfsc(index + 1)

        # What if we do not take it?
        share_comb.remove(SHARES[index])
        _bfsc(index + 1)

    _bfsc()
    return combinations


share_combinations = brute_force_shares_combinations(ShareCombination())
share_combinations.sort(key=lambda share_comb: share_comb.two_years_profit, reverse=True)
print_shares_combinations(share_combinations[:50])
