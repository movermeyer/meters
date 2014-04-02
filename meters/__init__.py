import importlib
import threading
import inspect
import logging


##### Private objects #####
_logger = logging.getLogger(__name__)

_is_running = False
_meters = {}
_handlers = []
_placeholders = {}

_control_lock = threading.Lock()


##### Public objects #####
prefix = ""


##### Public methods #####
def add_meter(name, obj):
    _meters[name] = obj
    return obj

def get_meter(name):
    return _meters[name]

def add_handler(obj):
    assert hasattr(obj, "start")
    assert hasattr(obj, "stop")
    _handlers.append(obj)

def add_placeholder(name, obj):
    _placeholders[name] = obj
    return obj


###
def configure(config):
    global prefix
    prefix = config.get("common", {}).get("prefix", prefix)

    for (name, attrs) in config.get("placeholders", {}).items():
        add_placeholder(name, _init_object(attrs, enable_kwargs=False))

    for attrs in config.get("handlers", {}).values():
        add_handler(_init_object(attrs))

    for (name, attrs) in config.get("meters", {}).items():
        add_meter(name, _init_object(attrs))

def clear():
    global _meters
    global _handlers
    global _placeholders
    stop()
    _meters = {}
    _handlers = []
    _placeholders = {}


###
def start():
    with _control_lock:
        global _is_running
        assert not _is_running, "Attempt to double start()"

        _logger.debug("Starting metrics threads")
        for handler in _handlers:
            _logger.debug("Starting handler %s...", handler)
            handler.start(dump)

        _is_running = True
        _logger.debug("All metrics were started")

def stop():
    with _control_lock:
        global _is_running
        assert _is_running, "Attempt to double stop()"

        _logger.debug("Perform a manual stop metrics...")
        for handler in _handlers:
            _logger.debug("Stopping handler %s...", handler)
            handler.stop()
        _is_running = False

        _logger.debug("All metrics were stopped")

def dump():
    try:
        placeholders = _get_placeholders_cache()
        results = {}
        for (name, meter) in dict(_meters).items():
            try:
                meter_value = meter()
            except Exception:
                _logger.warning("An exception occured while processing metric %s::%s", meter, name, exc_info=True)
                meter_value = None
            if isinstance(meter_value, dict): # For meters with multiple arrows (values)
                for (arrow, value) in meter_value.items():
                    results[_format_metric_name((name, arrow), placeholders)] = value
            else:
                results[_format_metric_name(name, placeholders)] = meter_value
        return results
    except Exception:
        _logger.exception("An exception occured while dumping metrics")
        return {}

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

def _get_placeholders_cache():
    # TODO: lazy placeholders
    return {
        key: ( value() if callable(value) else value )
        for (key, value) in dict(_placeholders).items()
    }

def _format_metric_name(parts, placeholders):
    if not isinstance(parts, (list, tuple)):
        parts = (parts,)
    name =  ".".join(filter(None, (prefix,) + parts)) # Apply the global prefix
    return name.format(**placeholders)

