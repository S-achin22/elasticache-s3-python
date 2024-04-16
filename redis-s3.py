import redis

#Elasticache endpoint
#redis-01.7abc2d.0001.usw2.cache.amazonaws.com:6379

redis_host= 'redis-01.7abc2d.0001.usw2.cache.amazonaws.com'
redis_port= 6379
redis_password= 'elasticachepassword'

#To connect to Elasticache cluster
r = redis.Redis(host=redis_host, port=redis_port, password=redis_password)

#Function to fetch data from the redis cluster

def redis_dump():
    keys = r.keys('*')  #To fetch keys
    data = {}   #Intialize dictionary
    for key in keys:          #This loop will put all keys data variable one by one 
        data[key] = r.get(key)
    return data 

if __name__ == "__main__":
    redis_data = redis_dump()

