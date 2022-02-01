"""Brute force solution to find the optimal set of shares."""

from shares import load_shares_from_csv, ShareCombination, print_shares_combinations, load_shares_from_dataset1, \
    load_shares_from_dataset2

DEFAULT_CSV_FILE = 'shares.csv'
CENTS_PER_EURO = 100
MAX_COST = 500 * CENTS_PER_EURO


def brute_force_shares_combinations(shares: list) -> list:
    """Finds all possible ShareCombination in O(2^n)."""
    combinations = []
    share_comb = ShareCombination()

    def _bfsc(index=0):
        if index >= len(shares) or share_comb.total_cost_cents + shares[index].cost > MAX_COST:
            if len(share_comb) != 0:
                combinations.append(share_comb.copy())
            return

        # Let's take this share.
        share_comb.add(shares[index])
        _bfsc(index + 1)

        # What if we do not take it?
        share_comb.remove(shares[index])
        _bfsc(index + 1)

    _bfsc()
    return combinations


if __name__ == '__main__':
    import sys

    source_file = DEFAULT_CSV_FILE

    # Data source.
    if '--dataset1' in sys.argv:
        source_file = 'dataset1_Python+P7.csv'
        shares_catalog = load_shares_from_dataset1(source_file)
    elif '--dataset2' in sys.argv:
        source_file = 'dataset2_Python+P7.csv'
        shares_catalog = load_shares_from_dataset2(source_file)
    else:
        shares_catalog = load_shares_from_csv(source_file)

    if '-t' in sys.argv:
        import timeit

        t_flag_index = sys.argv.index('-t')
        number = int(sys.argv[t_flag_index + 1]) if t_flag_index + 1 < len(sys.argv) else 1
        t = timeit.timeit(
            f'share_combinations = brute_force_shares_combinations(load_shares_from_csv("shares.csv"))\n'
            f'share_combinations.sort(key=lambda share_comb: share_comb.two_years_profit, reverse=True)\n'
            f'share_combinations[0]',
            setup=
            f"from __main__ import brute_force_shares_combinations\n"
            f"from shares import load_shares_from_csv",
            number=number)
        print(t)
    else:
        share_combinations = brute_force_shares_combinations(shares_catalog)
        share_combinations.sort(key=lambda share_comb: share_comb.two_years_profit, reverse=True)
        print_shares_combinations(share_combinations[:1])
