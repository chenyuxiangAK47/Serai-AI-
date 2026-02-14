from cachetools import TTLCache

# 1000 entries, each expires in 10 minutes
cache = TTLCache(maxsize=1000, ttl=600)
