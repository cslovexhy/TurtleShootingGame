# Question:
# Given a set of coins, and a target amount, find all different coin combinations can sum to that amount
# example input:
# coin_value_list = [1, 2, 5]
# coin_count_list = [2, 1, 0]
# target = 2
#
# example output:
# [(2, 0, 0), (0, 1, 0)]

import copy


def find_all_combo(coin_value_list, coin_count_list, target):
    assert(target >= 0)
    n = len(coin_value_list)
    dp = [set() for _ in range(target+1)]
    dp_zero = [0] * n
    dp[0].add(tuple(dp_zero))
    # print("dp = " + str(dp))
    for i in range(1, target+1):
        # print("i = " + str(i))
        for j in range(n):
            # print("j = " + str(j))
            value = coin_value_list[j]
            # print("value = " + str(value))
            prev_index = i - value
            # print("prev_index = " + str(prev_index))
            if prev_index < 0:
                continue
            for combo in dp[prev_index]:
                new_combo = list(copy.deepcopy(combo))
                new_combo[j] += 1
                if new_combo[j] > coin_count_list[j]:
                    continue
                # dedup here
                dp[i].add(tuple(new_combo))

    return dp


coin_value_list, coin_count_list, target = [1, 2, 5], [0, 5, 3], 10
dp = find_all_combo(coin_value_list, coin_count_list, target)

print("With Coins:")
for i in range(len(coin_count_list)):
    print("{} cents: {}x".format(coin_value_list[i], coin_count_list[i]))

print("ways to form {} cents:".format(target))

for sol in dp[target]:
    print(sol)


