import redis
import boto3  #AWS SDK for Python to upload data into AWS bucket
import json 

#Elasticache endpoint
#redis-01.7abc2d.0001.usw2.cache.amazonaws.com:6379
redis_host= 'redis-01.7abc2d.0001.usw2.cache.amazonaws.com'
redis_port= 6379
redis_password= 'elasticachepassword'

# AWS Key and Secret to acccess S3 bucket
AWS_ACCESS_KEY = 'YOUR_ACCESS_KEY'
AWS_SECRET_KEY = 'YOUR_SECRET_KEY'
AWS_REGION = 'us-west-2'
S3_BUCKET = 'redis-cache-dump-bucket'

#To connect to Elasticache cluster
r = redis.Redis(host=redis_host, port=redis_port, password=redis_password)

#Function to fetch data from the redis cluster
def redis_dump():
    keys = r.keys('*')  #To fetch keys
    data = {}   #Intialize dictionary
    for key in keys:          #This loop will put all keys data variable one by one 
        data[key] = r.get(key)
    return data 

# Connect to S3
s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY, region_name=AWS_REGION)


if __name__ == "__main__":
    redis_data = redis_dump()

    # Convert data to JSON format
    json_data = json.dumps(redis_data)
    
    # Write JSON data to a file
    json_file_path = 'redis_data.json'
    with open(json_file_path, 'w') as json_file: #  The with statement ensures that the file is properly closed after writing, even if an exception occurs during the process
        json_file.write(json_data)               #  writes the JSON data in the variable to the opened file

    # Upload the JSON file to S3
    try:
        s3.upload_file(json_file_path, S3_BUCKET, json_file_path)   
        print(f"JSON file '{json_file_path}' uploaded to S3 bucket '{S3_BUCKET}' with key '{json_file_path}'.")    # Here key means object key which is getting stored inside S3 bucket redis-cache-dump-bucket 
    except Exception as e:
        print(f"Error uploading JSON file to S3: {e}")