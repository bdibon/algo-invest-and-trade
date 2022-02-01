"""Dynamic programming solution to get the best set of shares."""

from typing import List

from shares import Share, load_shares_from_csv, load_shares_from_dataset1, ShareCombination, print_shares_combinations, \
    load_shares_from_dataset2

DEFAULT_CSV_FILE = 'shares.csv'
CENTS_PER_EURO = 100
MAX_COST = 500 * CENTS_PER_EURO


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
        if min_diff is None and diff != 0 or 0 < diff < min_diff:
            min_diff = diff

    min_budget = sorted_costs[0]
    sub_budgets = list(range(min_budget, MAX_COST + 1, min_diff))
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
                    budget_left_idx = (budget_left - min_budget) // min_diff
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

    print_flag = True if '-p' in sys.argv else False
    debug_flag = True if '--debug' in sys.argv else False
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

    # Use debug dataset.
    if debug_flag:
        shares_catalog = load_shares_from_csv('debug.csv')
        MAX_COST = 14 * 100

    if '-t' in sys.argv:
        # Time execution.
        import timeit

        t_flag_index = sys.argv.index('-t')
        number = int(sys.argv[t_flag_index + 1]) if t_flag_index + 1 < len(sys.argv) else 1
        t = timeit.timeit('optimized_shares_combination(shares_catalog)',
                          globals=globals(),
                          number=number)
        print(t)
    else:
        # Execute algorithm.
        best_shares_comb = optimized_shares_combination(shares_catalog, print_flag)
        print_shares_combinations([best_shares_comb])
