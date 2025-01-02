import sys
import csv
import time

from skyplane.api.client import SkyplaneClient

logs = list()
with open(sys.argv[1], newline='') as infile:
    data = csv.reader(infile, delimiter=",")
    for row in data:
        req_id = int(row[0])
        timestamp = int(row[1]) / 1000
        req_type = row[2]
        etag = row[3]
        size = row[4]
        logs.append([req_id, timestamp, req_type, etag, size])

client = SkyplaneClient()
total_reqs = len(logs)
start_time = time.time()
expire_time = int(sys.argv[4])
last_execute_time = -1
dp = None
job_id = None

vm_results = list()
trasnfer_results = list()

with open(sys.argv[2], newline='a') as outfile1, open(sys.argv[3], newline='a') as outfile2:
    writer1 = csv.writer(outfile1)
    writer2 = csv.writer(outfile2)
    for log in logs:
        while start_time + log[1] < time.time():
            if dp is not None and time.time() - last_execute_time > expire_time:
                client.deprovision(dp)
                dp = None
                job_id = None
                writer1.writerow([time.time() - start_time, 'stop'])
        if dp is None:
            writer1.writerow([time.time() - start_time, 'start'])
            job_id, dp, duration, vm_duration = client.copy_with_no_deprov(src=f's3://motivation.us-east-1/{log[0]}.dat',
                                                                           dst=f's3://motivation.test.us-east-2/{log[0]}.dat')
            last_execute_time = time.time()
        else:
            job_id, dp, duration, vm_duration = client.copy_with_dp(src=f's3://motivation.us-east-1/{log[0]}.dat',
                                                                    dst=f's3://motivation.test.us-east-2/{log[0]}.dat',
                                                                    job_id=job_id,
                                                                    dp=dp)
            last_execute_time = time.time()
        writer2.writerow([time.time() - start_time, time.time() - start_time - log[1], duration])
