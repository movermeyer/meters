# Based on https://github.com/nikicat/yasd/blob/master/yasd/procstat.py
# See "man 5 proc" for details


import os


##### Public classes #####
class Stat:
    def __call__(self):
        with open("/proc/stat") as stat_file:
            cpu_stats = stat_file.readline().split()
        results = {}
        for (count, name) in enumerate((
                "user",       # Time spent in user mode.
                "nice",       # Time spent in user mode with low priority (nice).
                "system",     # Time spent in system mode.
                "idle",       # Time spent in the idle task. This value should be USER_HZ times the second entry in the /proc/uptime pseudo-file.
                "iowait",     # (2.5.41) Time waiting for I/O to complete.
                "irq",        # (2.6.0-test4) Time servicing interrupts.
                "softirq",    # (2.6.0-test4) Time servicing softirqs.
                "steal",      # (2.6.11) Stolen time, which is the time spent in other operating systems when running in a virtualized environment.
                "guest",      # (2.6.24) Time spent running a virtual CPU for guest operating systems under the control of the Linux kernel.
                "guest_nice", # (2.6.33) Time spent running a niced guest (virtual CPU for guest operating systems under the control of the Linux kernel).
            )):
            try:
                metric = cpu_stats[count + 1]
            except IndexError:
                break
            results["cpu." + name] = int(metric)
        return results

class SelfStat:
    def __call__(self):
        jiffies_per_sec = os.sysconf("SC_CLK_TCK") # Clock ticks per second... jiffies (Hz)
        page_size = os.sysconf("SC_PAGE_SIZE") // 1024
        with open("/proc/self/stat") as stat_file:
            proc_stats = stat_file.readline().split()
        return {
            "utime":  int(proc_stats[13]) // jiffies_per_sec, # Amount of time that this process has been scheduled in user mode.
            "stime":  int(proc_stats[14]) // jiffies_per_sec, # Amount of time that this process has been scheduled in kernel mode.
            "cutime": int(proc_stats[15]) // jiffies_per_sec, # Amount of time that this process's waited-for children have been scheduled in user mode.
            "cstime": int(proc_stats[16]) // jiffies_per_sec, # Amount of time that this process's waited-for children have been scheduled in kernel mode
            "vsize":  int(proc_stats[22]) // jiffies_per_sec, # Virtual memory size in bytes.
            "rss":    int(proc_stats[23]) * page_size, # Resident Set Size in bytes.
        }

class LoadAverage:
    def __call__(self):
        with open("/proc/loadavg") as loadavg_file :
            averages = tuple(map(float, loadavg_file.readline().split()[:3]))
        return dict(zip(("la1", "la5", "la15"), averages))

