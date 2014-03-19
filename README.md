meters - Yet another metrics library
===========================
Tracks server state and statistics, allowing you to see what your server is
doing. It can also send metrics to Graphite for graphing or to a file for crash forensics.
It has flexible scalability.

### Installation ###
From [PyPI](https://pypi.python.org/pypi/meters):
```
pip install meters
```

### Complete example of usage ###
```python
import math
import time
import logging

import meters
import meters.scales.shared

meters.configure({
        "placeholders": {
            "env":   "os.environ",
            "uname": "platform.uname",
        },

        "handlers": {
            "graphite-server-a": {
                "class":   "meters.handlers.graphite.GraphiteHandler",
                "url":     "tcp://graphite-a.example.com:2025",
                "timeout": 1,
                "period":  1,
            },
            "graphite-server-b": {
                "class":   "meters.handlers.graphite.GraphiteHandler",
                "url":     "udp://graphite-b.example.com:2025",
                "timeout": 1,
                "period":  1,
            },
            "log": "meters.handlers.log.LoggingHandler",
        },
        "meters": {
            "{env[USER]}.{uname[1]}.proc.la":    "meters.scales.procfs.LoadAverage",
            "{env[USER]}.{uname[1]}.proc.stat":  "meters.scales.procfs.Stat",
            "{env[USER]}.{uname[1]}.proc.self":  "meters.scales.procfs.SelfStat",
            "{env[USER]}.{uname[1]}.py_threads": "meters.scales.python.Threads",
            "{env[USER]}.{uname[1]}.py_objects": "meters.scales.python.Objects",
            "{env[USER]}.{uname[1]}.py_rusage" : {
                "class": "meters.scales.python.Resources",
                "who":   "RUSAGE_CHILDREN",
            },
            "{env[USER]}.{uname[1]}.now": time.time,
        },
    })

# Catch all messages
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
logging.getLogger().addHandler(handler)
logging.getLogger().setLevel(logging.DEBUG)

foo = meters.add_meter("{env[USER]}.{uname[1]}.foo", meters.scales.shared.Value(float))
meters.start()

count = 0
while True:
    foo.set(math.sin(count))
    time.sleep(1)
    count += 1

```

