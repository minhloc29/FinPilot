import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# save cache
r.set("stock:NVDA:price", 875.23, ex=60)

# get cache
price = r.get("stock:NVDA:price")

print(price)

r.hset('user-session:123', mapping={
    'name': 'John',
    "surname": 'Smith',
    "company": 'Redis',
    "age": 29
})
# True

hihi = r.hgetall('user-session:123')
print(hihi)