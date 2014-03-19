import resource
import threading
import gc


##### Public classes #####
class Resources:
    def __init__(self, who=resource.RUSAGE_SELF): # pylint: disable=E1101
        if isinstance(who, str): # For text configuration
            who = getattr(resource, who)
        self._who = who

    def __call__(self):
        ru = resource.getrusage(self._who)
        return {
            name: getattr(ru, name)
            for name in dir(ru)
            if name.startswith("ru_")
        }

class Threads:
    def __call__(self):
        return {
            "alive_threads": threading.active_count(),
        }

class Objects:
    def __call__(self):
        return {
            "gc_objects": len(gc.get_objects()),
        }

