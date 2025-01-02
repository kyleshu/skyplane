from skyplane.api.client import SkyplaneClient

logs = list()
with open(sys.argv[1], newline='') as infile:
    data = csv.reader(infile, delimiter=",")
    for row in data:
        req_id = int(row[0])
        timestamp = int(row[1]) / 1000
        req_type = row[2]
        obj_id = row[3]
        etag = row[4]
        versions = row[5].split('/')
        cur_version = int(row[6])
        logs.append([req_id, timestamp, req_type, obj_id, etag, versions, cur_version])

client = skyplane.SkyplaneClient()
total_reqs = len(logs)
cur_idx = 0
start_time = time.time()
expire_time = int(sys.argv[3])

while cur_idx < total_reqs:
    elapsed = time.time() - start_time
