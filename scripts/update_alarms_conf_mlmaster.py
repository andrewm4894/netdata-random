import requests
from datetime import datetime

host = '127.0.0.1:19999'
file_path = '/etc/netdata/python.d/alarms.conf'
url = f'http://{host}/api/v1/info'
r = requests.get(url)
children = sorted(r.json()['mirrored_hosts'])

with open(file_path, "w+") as f:
    f.write(f"# file generated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

for child in children:

    config = f"""
{child}:
    url: 'http://127.0.0.1:19999/host/{child}/api/v1/alarms?all'
    status_map:
      CLEAR: 0
      WARNING: 1
      CRITICAL: 2
    collect_alarm_values: true
    alarm_status_chart_type: 'stacked'
    """
    with open(file_path, "a") as f:
        f.write(config)
