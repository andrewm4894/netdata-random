import requests
from datetime import datetime

host = '127.0.0.1:19999'
file_path = '/etc/netdata/python.d/anomaliespoc.conf'
#host = '35.193.228.190:19999/'
#file_path = 'anomaliespoc.conf'
url = f'http://{host}/api/v1/info'
r = requests.get(url)
children = r.json()['mirrored_hosts']

with open(file_path, "w+") as f:
    f.write(f"# file generated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

for child in children:

    config = f"""
{child}:
    name: {child}
    url: 'http://127.0.0.1:19999/host/{child}/api/v1/allmetrics?format=json'
    suffix: '_km'
    thold: 99.0
    display_family: true
    update_every: 1
    priority: 85
    autodetection_retry: 10
    """
    with open(file_path, "a") as f:
        f.write(config)


