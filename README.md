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
        "common": {
            "prefix": "servers.{env[USER]}.{uname[1]}",
        },

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
            "proc.la":    "meters.scales.procfs.LoadAverage",
            "proc.stat":  "meters.scales.procfs.Stat",
            "proc.self":  "meters.scales.procfs.SelfStat",
            "py_threads": "meters.scales.python.Threads",
            "py_objects": "meters.scales.python.Objects",
            "py_rusage" : {
                "class": "meters.scales.python.Resources",
                "who":   "RUSAGE_CHILDREN",
            },
            "!local.now": time.time, # ! - Disable global prefix
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

The result will be the following metrics:
```python
local.now=1395253385.465558
servers.mdevaev.reki.mdevaev.reki.foo=0.0
servers.mdevaev.reki.proc.la.la1=0.46
servers.mdevaev.reki.proc.la.la15=1.14
servers.mdevaev.reki.proc.la.la5=0.98
servers.mdevaev.reki.proc.self.cstime=0.0
servers.mdevaev.reki.proc.self.cutime=0.0
servers.mdevaev.reki.proc.self.rss=9824.0
servers.mdevaev.reki.proc.self.stime=0.0
servers.mdevaev.reki.proc.self.utime=0.09
servers.mdevaev.reki.proc.self.vsize=2090475.52
servers.mdevaev.reki.proc.stat.cpu.guest=0
servers.mdevaev.reki.proc.stat.cpu.guest_nice=0
servers.mdevaev.reki.proc.stat.cpu.idle=32537196
servers.mdevaev.reki.proc.stat.cpu.iowait=198023
servers.mdevaev.reki.proc.stat.cpu.irq=59
servers.mdevaev.reki.proc.stat.cpu.nice=1375
servers.mdevaev.reki.proc.stat.cpu.softirq=7146
servers.mdevaev.reki.proc.stat.cpu.steal=0
servers.mdevaev.reki.proc.stat.cpu.system=3213874
servers.mdevaev.reki.proc.stat.cpu.user=7361767
servers.mdevaev.reki.py_objects.gc_objects=8603
servers.mdevaev.reki.py_rusage.ru_idrss=0
servers.mdevaev.reki.py_rusage.ru_inblock=0
servers.mdevaev.reki.py_rusage.ru_isrss=0
servers.mdevaev.reki.py_rusage.ru_ixrss=0
servers.mdevaev.reki.py_rusage.ru_majflt=0
servers.mdevaev.reki.py_rusage.ru_maxrss=7156
servers.mdevaev.reki.py_rusage.ru_minflt=786
servers.mdevaev.reki.py_rusage.ru_msgrcv=0
servers.mdevaev.reki.py_rusage.ru_msgsnd=0
servers.mdevaev.reki.py_rusage.ru_nivcsw=2
servers.mdevaev.reki.py_rusage.ru_nsignals=0
servers.mdevaev.reki.py_rusage.ru_nswap=0
servers.mdevaev.reki.py_rusage.ru_nvcsw=3
servers.mdevaev.reki.py_rusage.ru_oublock=0
servers.mdevaev.reki.py_rusage.ru_stime=0.0
servers.mdevaev.reki.py_rusage.ru_utime=0.003333
servers.mdevaev.reki.py_threads.alive_threads=3
```

