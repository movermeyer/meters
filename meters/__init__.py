import importlib
import threading
import time


##### Private objects #####
_meters = {}
_handlers = []
#_watcher = _Watcher() # XXX: See bellow


##### Public methods #####
def add_meter(name, meter):
    assert callable(meter), "Meter must be a callable object"
    _meters[name] = meter
    return meter

def get_meter(name):
    return _meters[name]


###
def add_handler(handler):
    assert hasattr(handler, "set_dumper")
    assert hasattr(handler, "start")
    assert hasattr(handler, "stop")
    assert hasattr(handler, "is_alive")
    handler.set_dumper(dump)
    _handlers.append(handler)

def configure(config):
    for handler_attrs in config.get("handlers", {}).values():
        handler_attrs = dict(handler_attrs)
        handler_class = _get_class(handler_attrs.pop("class"))
        add_handler(handler_class(**handler_attrs))

    for (meter_name, meter_attrs) in config.get("meters", {}).items():
        meter_attrs = dict(meter_attrs)
        meter_class = _get_class(meter_attrs.pop("class"))
        add_meter(meter_name, meter_class(**meter_attrs))


###
def start(auto_stop=True):
    for handler in _handlers:
        handler.start()
    if auto_stop:
        _watcher.start()

def stop():
    if _watcher.is_alive():
        _watcher.stop()
    else:
        _inner_stop()

def dump():
    results = {}
    for (name, meter) in _meters.items():
        meter_value = meter()
        if isinstance(meter_value, dict): # For meters with multiple arrows (values)
            for (arrow, value) in meter_value.items():
                results[_format_name(".".join((name, arrow)))] = value
        else:
            results[_format_name(name)] = meter_value
    return results

def is_running_hook():
    # Usually, MainThread lives up to the completion of all the rest.
    # We need to determine when it is completed and to stop sending and receiving messages.
    # For our architecture that is enough.
    return threading._shutdown.__self__.is_alive() # pylint: disable=W0212


##### Private methods #####
def _get_class(path):
    path = path.split(".")
    assert len(path) >= 2, "Required package.class"
    module_name = ".".join(path[:-1])
    cls = getattr(importlib.import_module(module_name), path[-1])
    return cls

def _format_name(name):
    # TODO: Implement fqdn, node
    return name


###
def _inner_stop():
    for handler in _handlers:
        handler.stop()


##### Private classes #####
class _Watcher(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self._stop_loop = False

    def start(self):
        self._stop_loop = False
        threading.Thread.start(self)

    def stop(self):
        self._stop_loop = True

    def run(self):
        while not self._stop_loop and is_running_hook():
            time.sleep(1)
        _inner_stop()

_watcher = _Watcher()

