import redis

r = redis.Redis(host='localhost', port=6380, decode_responses=True)

def redis_set(user, key, value):
    r.hset(f'{user}', mapping={f'{key}': f'{value}'})

def redis_set_allcats(user, val):
    r.lpush(f'{user}cats', *val)

def redis_get(user, key,):
    return r.hget(f'{user}', f'{key}')

def redis_get_allcats(user):
    l = r.hget(f'{user}', 'allcats')
    return l

def redis_exists(user, key):
    return r.hexists(user, key)

def redis_exists_allcats(user):
    return r.exists(f'{user}cats')

def redis_del(user, key):
    r.hdel(f'{user}', f'{key}')

# delete all keys in a hash
def redis_del_all(user):
    for key in r.scan_iter(user):
        r.delete(key)
# test_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
# test_string = 'test_string'
# test_int = 1234567890


# print(r.hdel('marto', 'dashdata'))
# redis_set('test', 'list', test_list)
# redis_set('test', 'string', test_string)
# redis_set('test', 'int', test_int)

# s = (redis_get('marto', 'allcats'))
# #print(type(s))
# #convert to list
# s = s[1:-1]
# s = s.split(',')
# print(s)
# print(redis_get('test', 'string'))
# print(redis_get('test', 'int'))
# print(redis_get('test', 'list'))