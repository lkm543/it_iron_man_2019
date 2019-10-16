import random

pool_reward = 0
try_times = 10000
mine_time = 0

# RBPPS Miner
for i in range(try_times):
    luck = 1
    while(True):
        if random.randint(0,100) == 0:
            # Mine Block!
            pool_reward += 100
            mine_time += luck
            break
        luck += 1
print(f"Expect RBPPS miner: {pool_reward/mine_time}")

miner_reward = 0
pool_reward = 0
mine_time = 0
# RBPPS + PPS Miner and Pool
for i in range(try_times):
    luck = 1
    while(True):
        if random.randint(0,100) == 0:
            # Mine Block!
            if luck < 100:
                miner_reward += 100
                pool_reward += 100
                mine_time += luck
                break
            else:
                if random.randint(0,1) == 0:
                    miner_reward += 200*(100/(100+luck))
                    pool_reward += 200*(luck/(100+luck))
                    miner_reward += luck - 100
                    mine_time += luck
                    break
        luck += 1
print(f"Expect RBPPS + PPS miner: {miner_reward/mine_time}")
print(f"Expect RBPPS + PPS pool: {pool_reward/mine_time}")