import logging
from . import ThreadedHandler


##### Public classes #####
class LoggingHandler(ThreadedHandler):
    def __init__(self, logger=__package__, level=logging.INFO, extra="metrics", period=5):
        ThreadedHandler.__init__(self, period)
        self._logger = logging.getLogger(logger)
        self._level = level
        self._extra = extra

    def shot(self, metrics):
        msg = "\n----- BEGIN METERS -----\n{}\n----- END METERS -----\n".format(
            "\n".join(
                "{}={}".format(key, value)
                for (key, value) in metrics.items()
            )
        )
        self._logger.log(self._level, msg, extra={ self._extra: metrics })

