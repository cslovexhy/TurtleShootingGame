import copy
import time
import random


class Currency:
    def __init__(self, exchange_rates):

        def add_rate_to_map(src, dst, rate):
            if src not in self.m:
                self.m[src] = dict()
            if dst not in self.m[src]:
                self.m[src][dst] = None
            self.m[src][dst] = rate

        self.m = {}
        for src, dst, rate in exchange_rates:
            assert (rate > 0)
            add_rate_to_map(src, dst, rate)
            add_rate_to_map(dst, src, 1 / rate)

    def calc_exchange_rate(self, src, dst):
        assert (src in self.m and dst in self.m)

        visited = {src: 1}
        batch = [src]

        while batch:
            next_batch = []
            for node in batch:
                if node == dst:
                    return visited[node]
                for next_node, rate in self.m[node].items():
                    if next_node in visited:
                        continue
                    next_batch.append(next_node)
                    visited[next_node] = visited[node] * rate
            batch = next_batch

        print("{} and {} are not exchangeable".format(src, dst))
        return -1


rates = (('A', 'B', 0.5), ('B', 'C', 0.6))

currency = Currency(rates)

print(currency.calc_exchange_rate('A', 'C'))
print(currency.calc_exchange_rate('C', 'A'))
print(currency.calc_exchange_rate('B', 'A'))
# print(currency.calc_exchange_rate('D', 'A'))