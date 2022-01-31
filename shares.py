"""Utilities that helps to solve the best shares set problem."""

import csv
from collections import namedtuple
from functools import reduce
from typing import List

from tabulate import tabulate

Share = namedtuple('Share', 'id cost profit')


def load_shares_from_csv(filename: str) -> List[Share]:
    with open(filename) as file:
        share_reader = csv.DictReader(file, fieldnames=['id', 'cost', 'profit'])
        next(share_reader)
        return [Share(share['id'], int(share['cost']) * 100, int(share['profit'].rstrip('%')) / 100) for
                share in share_reader]


def load_shares_from_dataset1(filename: str) -> List[Share]:
    with open(filename) as file:
        share_reader = csv.DictReader(file, fieldnames=['id', 'price', 'profit'])
        next(share_reader)
        shares = [Share(share['id'], int(round(float(share['price']), 2) * 100), round(float(share['profit']) / 100, 2))
                  for
                  share in share_reader]
        return [share for share in shares if share.cost > 0]


def print_shares_combinations(shares_data):
    table_headers = ['Shares', 'Total Cost', '2 years profit']
    table = [[share_comb.shares_ids, share_comb.total_cost, share_comb.two_years_profit] for share_comb in shares_data]
    print(tabulate(table, headers=table_headers))


class ShareCombination:
    """A wrapper class around the set data type that provides business logic to deal with a set of actions."""

    def __init__(self, shares=None):
        self.shares_set = shares
        self._calc_total_cost()
        self._calc_two_years_profit()

    def __str__(self):
        return str({share.id for share in self.shares_set})

    def __repr__(self):
        return f"{self.__class__.__name__}({str(self)})"

    def __len__(self):
        return len(self.shares_set)

    def __add__(self, other):
        return ShareCombination(self.shares_set | other.shares_set)

    @property
    def shares_set(self):
        return self._shares_set

    @shares_set.setter
    def shares_set(self, shares):
        if shares is None:
            shares = set()
        if not isinstance(shares, set):
            raise AttributeError(f'{self.__class__.__name__}: shares_set attribute must be a set')
        self._shares_set = shares

    @property
    def total_cost_cents(self):
        return self._total_cost

    @property
    def total_cost(self):
        return round(self._total_cost / 100, 2)

    @property
    def two_years_profit(self):
        return round(self._two_years_profit / 100, 2)

    @property
    def shares_ids(self):
        def callback_action_dash(result, share):
            contraction = 'A' + share.id.lstrip("Action-")
            if len(result) == 0:
                result += contraction
            else:
                result += ', ' + contraction
            return result

        def callback_vanilla(result, share):
            if len(result) == 0:
                result += share.id
            else:
                result += ', ' + share.id
            return result

        if 'Action-' in next(iter(self.shares_set)):
            # Case: original.
            return reduce(callback_action_dash, self.shares_set, '')
        else:
            # Case: dataset1.
            return reduce(callback_vanilla, self.shares_set, '')

    def add(self, share):
        self._shares_set.add(share)
        self._total_cost += share.cost
        self._two_years_profit += share.cost * share.profit

    def remove(self, share):
        self._shares_set.remove(share)
        self._total_cost -= share.cost
        self._two_years_profit -= share.cost * share.profit

    def copy(self):
        return ShareCombination(self._shares_set.copy())

    def _calc_total_cost(self):
        self._total_cost = 0
        for share in self.shares_set:
            self._total_cost += share.cost
        return self._total_cost

    def _calc_two_years_profit(self):
        self._two_years_profit = 0
        for share in self.shares_set:
            self._two_years_profit += share.cost * share.profit
        return self._two_years_profit
