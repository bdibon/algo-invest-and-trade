"""Dynamic programming solution to get the best set of shares."""

from typing import List

from shares import Share, load_shares_from_csv, ShareCombination, print_shares_combinations

DEFAULT_CSV_FILE = 'shares.csv'
MAX_COST = 500


def print_grid(grid: List[List], shares, budgets) -> None:
    """Prints the underlying grid for the optimized_shares_combination algorithm."""
    for row_idx, row in enumerate(grid):
        for budget_idx, budget in enumerate(budgets):
            if row_idx == 0:
                if budget_idx == len(budgets) - 1:
                    print(f"{f'{budgets[budget_idx]}€': <12}")
                elif budget_idx == 0:
                    print(f"{f'{budgets[budget_idx]: >9}€': <{21 - len(str(budgets[budget_idx + 1]))}}", end='')
                else:
                    nb_digits = len(str(budgets[budget_idx]))
                    print(f"{f'{budgets[budget_idx]}€': <12}", end='')
        for col_idx, share_comb in enumerate(row):

            if col_idx == 0:
                print(f'A{shares[row_idx].id.lstrip("Action-"): <6}', end='\t')
                print(f'{f"{share_comb.two_years_profit:.2f}€": <9}', end='\t')
            elif col_idx == len(row) - 1:
                print(f'{share_comb.two_years_profit:.2f}€')
            else:
                print(f'{f"{share_comb.two_years_profit:.2f}€": <9}', end='\t')
    print()


def optimized_shares_combination(shares: List[Share], should_print: bool = False) -> ShareCombination:
    """Finds the best ShareCombination in O(n * m)."""
    sorted_costs = [share.cost for share in shares]
    sorted_costs.sort()

    # This is our cost step.
    min_diff = None
    for curr_idx in range(len(sorted_costs) - 1):
        next_idx = curr_idx + 1
        diff = abs(sorted_costs[curr_idx] - sorted_costs[next_idx])
        if min_diff is None or diff < min_diff:
            min_diff = diff

    sub_budgets = list(range(sorted_costs[0], MAX_COST + 1, min_diff))
    grid = [[None for col in range(len(sub_budgets))] for row in range(len(shares))]

    for share_idx, share in enumerate(shares):
        for budget_idx, budget in enumerate(sub_budgets):
            # First row.
            if share_idx == 0:
                share_comb = ShareCombination()
                if share.cost <= budget:
                    share_comb.add(share)
                grid[share_idx][budget_idx] = share_comb
            # Other rows.
            else:
                current_share_comb = grid[share_idx - 1][budget_idx]
                budget_left = budget - share.cost
                if budget_left < 0:
                    grid[share_idx][budget_idx] = current_share_comb
                else:
                    share_comb = ShareCombination()
                    share_comb.add(share)

                    # Use previous solution.
                    budget_left_idx = budget_left // min_diff - min_diff
                    if budget_left_idx >= 0:
                        budget_left_comb = grid[share_idx - 1][budget_left_idx]
                        share_comb += budget_left_comb

                    if share_comb.two_years_profit >= current_share_comb.two_years_profit:
                        grid[share_idx][budget_idx] = share_comb
                    else:
                        grid[share_idx][budget_idx] = current_share_comb

    if should_print:
        print_grid(grid, shares, sub_budgets)

    best_comb = grid[-1][-1]
    return best_comb


if __name__ == '__main__':
    import sys

    if '-t' in sys.argv:
        import timeit

        t_flag_index = sys.argv.index('-t')
        number = int(sys.argv[t_flag_index + 1]) if t_flag_index + 1 < len(sys.argv) else 1
        t = timeit.timeit('optimized_shares_combination(shares_catalog)',
                          setup=f"from __main__ import optimized_shares_combination\n"
                                f"from shares import load_shares_from_csv\n"
                                f"shares_catalog = load_shares_from_csv({DEFAULT_CSV_FILE})",
                          number=number)
        print(t)
    else:
        print_flag = True if '-p' in sys.argv else False
        debug_flag = True if '-d' in sys.argv else False
        source_file = DEFAULT_CSV_FILE

        if '-f' in sys.argv:
            f_flag_index = sys.argv.index('-f')
            source_file = sys.argv[f_flag_index + 1] if f_flag_index + 1 < len(sys.argv) else DEFAULT_CSV_FILE

        if debug_flag:
            shares_catalog = load_shares_from_csv('debug.csv')
            MAX_COST = 14
        else:
            shares_catalog = load_shares_from_csv(source_file)

        best_shares_comb = optimized_shares_combination(shares_catalog, print_flag)
        print_shares_combinations([best_shares_comb])
