meters - Yet another metrics library
===========================
[![Build Status](https://travis-ci.org/yandex-sysmon/meters.svg?branch=master)](https://travis-ci.org/yandex-sysmon/meters)
[![Coverage Status](https://coveralls.io/repos/yandex-sysmon/meters/badge.png)](https://coveralls.io/r/yandex-sysmon/meters)
[![Latest Version](https://img.shields.io/pypi/v/meters.svg)](https://pypi.python.org/pypi/meters/)

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
            "uname": "meters.shortcuts.get_node",
            "app":   "meters.shortcuts.get_app",
        },

        "common": {
            "prefix": "servers.{uname}.{env[USER]}.{app}",
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
            "time.now": time.time,
        },
    })

# Catch all messages
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
logging.getLogger().addHandler(handler)
logging.getLogger().setLevel(logging.DEBUG)

foo = meters.add_meter("foo", meters.scales.shared.Value(float))
meters.start()

count = 0
while True:
    foo.set(math.sin(count))
    time.sleep(1)
    count += 1

```

The result will be the following metrics:
```python
servers.reki.mdevaev.foo=0.0
servers.reki.mdevaev.proc.la.la1=0.87
servers.reki.mdevaev.proc.la.la15=0.71
servers.reki.mdevaev.proc.la.la5=0.81
servers.reki.mdevaev.proc.self.cstime=0.0
servers.reki.mdevaev.proc.self.cutime=0.0
servers.reki.mdevaev.proc.self.rss=10048.0
servers.reki.mdevaev.proc.self.stime=0.01
servers.reki.mdevaev.proc.self.utime=0.11
servers.reki.mdevaev.proc.self.vsize=2091663.36
servers.reki.mdevaev.proc.stat.cpu.guest=0
servers.reki.mdevaev.proc.stat.cpu.guest_nice=0
servers.reki.mdevaev.proc.stat.cpu.idle=27298939
servers.reki.mdevaev.proc.stat.cpu.iowait=176185
servers.reki.mdevaev.proc.stat.cpu.irq=61
servers.reki.mdevaev.proc.stat.cpu.nice=1386
servers.reki.mdevaev.proc.stat.cpu.softirq=7285
servers.reki.mdevaev.proc.stat.cpu.steal=0
servers.reki.mdevaev.proc.stat.cpu.system=3463200
servers.reki.mdevaev.proc.stat.cpu.user=7594520
servers.reki.mdevaev.py_objects.gc_objects=9082
servers.reki.mdevaev.py_rusage.ru_idrss=0
servers.reki.mdevaev.py_rusage.ru_inblock=0
servers.reki.mdevaev.py_rusage.ru_isrss=0
servers.reki.mdevaev.py_rusage.ru_ixrss=0
servers.reki.mdevaev.py_rusage.ru_majflt=0
servers.reki.mdevaev.py_rusage.ru_maxrss=7372
servers.reki.mdevaev.py_rusage.ru_minflt=788
servers.reki.mdevaev.py_rusage.ru_msgrcv=0
servers.reki.mdevaev.py_rusage.ru_msgsnd=0
servers.reki.mdevaev.py_rusage.ru_nivcsw=2
servers.reki.mdevaev.py_rusage.ru_nsignals=0
servers.reki.mdevaev.py_rusage.ru_nswap=0
servers.reki.mdevaev.py_rusage.ru_nvcsw=3
servers.reki.mdevaev.py_rusage.ru_oublock=0
servers.reki.mdevaev.py_rusage.ru_stime=0.0
servers.reki.mdevaev.py_rusage.ru_utime=0.003333
servers.reki.mdevaev.py_threads.alive_threads=3
servers.reki.mdevaev.time.now=1395266477.651378
```

