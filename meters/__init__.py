import importlib
import threading
import inspect
import time


##### Private objects #####
_meters = {}
_handlers = []
_placeholders = {}
#_watcher = _Watcher() # XXX: See bellow


##### Public methods #####
def add_meter(name, meter):
    _meters[name] = meter
    return meter

def get_meter(name):
    return _meters[name]

def add_handler(handler):
    assert hasattr(handler, "set_dumper")
    assert hasattr(handler, "start")
    assert hasattr(handler, "stop")
    assert hasattr(handler, "is_alive")
    handler.set_dumper(dump)
    _handlers.append(handler)
    return handler

def add_placeholder(name, placeholder):
    _placeholders[name] = placeholder
    return placeholder


###
def configure(config):
    for (name, attrs) in config.get("placeholders", {}).items():
        add_placeholder(name, _init_object(attrs, False))

    for attrs in config.get("handlers", {}).values():
        add_handler(_init_object(attrs))

    for (name, attrs) in config.get("meters", {}).items():
        add_meter(name, _init_object(attrs))


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
    # TODO: lazy placeholders
    placeholders = { key: value() for (key, value) in _placeholders.items() }

    results = {}
    for (name, meter) in _meters.items():
        meter_value = meter()
        if isinstance(meter_value, dict): # For meters with multiple arrows (values)
            for (arrow, value) in meter_value.items():
                meter_name = "{}.{}".format(name, arrow).format(**placeholders)
                results[meter_name] = value
        else:
            results[name.format(**placeholders)] = meter_value
    return results

def is_running_hook():
    # Usually, MainThread lives up to the completion of all the rest.
    # We need to determine when it is completed and to stop sending and receiving messages.
    # For our architecture that is enough.
    return threading._shutdown.__self__.is_alive() # pylint: disable=W0212


##### Private methods #####
def _init_object(attrs, enable_kwargs=True):
    if isinstance(attrs, dict):
        assert enable_kwargs, "Keyword arguments is disabled for {}".format(attrs)
        attrs = dict(attrs)
        cls = attrs.pop("class")
    else:
        cls = attrs
        attrs = {}

    if isinstance(cls, str):
        path = cls.split(".")
        assert len(path) >= 2, "Required package.class, not {}".format(cls)
        module_name = ".".join(path[:-1])
        cls = getattr(importlib.import_module(module_name), path[-1])

    if inspect.isclass(cls):
        # Make objects from class
        obj = cls(**attrs)
    elif callable(cls):
        # Wrap non-class objects like a function to lambdas
        obj = ( lambda: cls(**attrs) )
    else:
        # Wrap variables to lambdas
        assert len(attrs) == 0, "Variables does not accepts keyword arguments"
        obj = ( lambda: cls )

    return obj


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

