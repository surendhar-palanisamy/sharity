import time

from hashlib import sha256
max_nonce = 10000000
# difficulty level 
prefix_zeros = 3


def hasher(text):
    return sha256(text.encode('ascii')).hexdigest()


def mine(transactions, previous_hash, time_data):
    start = time.time()
    print('Mining started...', start)
    prefix_str = '0'*prefix_zeros
    nonce = 1

    for nonce in range(max_nonce):
        text = transactions + \
            previous_hash+str(nonce)+str(time_data)
        new_hash = hasher(text)
        if new_hash.startswith(prefix_str):
            print('Nonce for the block', nonce)
            total_time = str(time.time()-start)
            # print('total time taken for the block to be mined', total_time)
            return new_hash, nonce
    raise BaseException('Too much work with max nonce', max_nonce)


# if __name__ == '__main__':
#     sender = 'Suren'
#     receiver = 'Suren2'
#     cash = 10
#     transactions = str(sender) + str(receiver)+str(cash)
#     difficulty = 3

#     previous_hash = 'b5d4045c3f466fa91fe2cc6abe79232a1a57cdf104f7a26e716e0a1e2789df78'
#     new_hash = mine(5, transactions, previous_hash, difficulty)

#     print(new_hash)


def validator(previous_block):
    transactions = str(previous_block.sender) + \
        str(previous_block.receiver) + str(previous_block.cash)
    time_data = str(previous_block.date_created)
    previous_hash = str(previous_block.previous_hash)
    nonce = str(previous_block.nonce)
    text = transactions+previous_hash+nonce+time_data
    validated_hash = hasher(text)
    return validated_hash
