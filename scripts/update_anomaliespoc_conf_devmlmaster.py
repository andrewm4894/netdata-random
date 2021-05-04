"""
# get script
wget https://raw.githubusercontent.com/andrewm4894/netdata-random/main/scripts/update_conf.py
# add to cron
crontab -e
# comand to run every 5 minutes
*/5 * * * * sudo python3 /home/andrewmaguire/update_conf.py
# add to cron via comand line
crontab -l | { cat; echo "*/5 * * * * sudo python3 update_conf.py"; } | crontab -
"""

import requests
from datetime import datetime

host = '127.0.0.1:19999'
file_path = '/etc/netdata/python.d/anomaliespoc.conf'
url = f'http://{host}/api/v1/info'
r = requests.get(url)
children = sorted(r.json()['mirrored_hosts'])

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
    display_prefix: true
    display_chart: true
    update_every: 5
    priority: 85
    autodetection_retry: 10
    """
    with open(file_path, "a") as f:
        f.write(config)


