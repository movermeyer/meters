import re
import urllib.parse
import socket
import pickle
import struct
import threading
import logging
import time

from . import ThreadedHandler


##### Private objects #####
_logger = logging.getLogger(__name__)


##### Public classes #####
class GraphiteHandler(ThreadedHandler):
    def __init__(self, dumper, period=5, url="tcp://localhost:2004", timeout=None):
        ThreadedHandler.__init__(self, dumper, period)

        parsed_url = urllib.parse.urlparse(url)
        if not parsed_url.scheme: # Empty or None
            # Parse host:port with default protocol
            url = "tcp://" + url
            parsed_url = urllib.parse.urlparse(url)

        self._sock_type = {
            "tcp": socket.SOCK_STREAM,
            "udp": socket.SOCK_DGRAM,
        }[parsed_url.scheme.lower()]
        self._host = ( parsed_url.hostname or "localhost" )
        self._port = ( parsed_url.port or 2004 )

        self._url = "{}://{}:{}".format(parsed_url.scheme.lower(), self._host, self._port)
        self._timeout = timeout


    ### Override ###

    def shot(self, metrics):
        # TODO: Add queue for unsended metrics
        threading.Thread(target=lambda: self._send(metrics)).start()


    ### Private ###

    def _send(self, metrics):
        # See for details:
        #   http://graphite.readthedocs.org/en/latest/feeding-carbon.html#the-pickle-protocol

        now = int(time.time())
        plains = [
            (re.sub(r"[^\w\.]", "_", name), (now, value))
            for (name, value) in metrics.items()
            if value is not None # Filter failed metrics
        ]
        if len(plains) == 0:
            _logger.debug("Passed the empty metrics list")
            return

        data = pickle.dumps(plains, protocol=2)
        header = struct.pack("!L", len(data))
        message = header + data

        _logger.debug("Sending metrics to %s; message size: %d", self._url, len(message))
        sock = self._connect()
        try:
            sock.sendall(message) # pylint: disable=E1103
        finally:
            sock.close()
        _logger.debug("Data successfully sended to %s!", self._url)

    def _connect(self):
        rejects = []
        sock = None
        for res in socket.getaddrinfo(self._host, self._port, socket.AF_UNSPEC, self._sock_type):
            (af, _, _, _, sock_addr) = res
            try:
                _logger.debug("Connecting to %s...", self._url)
                sock = socket.socket(af, self._sock_type)
                if self._timeout is not None:
                    sock.settimeout(self._timeout) # pylint: disable=E1103
                    sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, struct.pack('LL', self._timeout, 0)) # pylint: disable=E1103
                    sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDTIMEO, struct.pack('LL', self._timeout, 0)) # pylint: disable=E1103
                sock.connect(sock_addr) # pylint: disable=E1103
            except Exception as err:
                rejects.append("Cannot connect to {}: {}".format(self._url, err))
                _logger.debug(rejects[-1], exc_info=True)
                try:
                    sock.close()
                except Exception:
                    pass
                sock = None
            if sock is not None:
                break
        if sock is None:
            raise OSError("Cannot connect to Graphite\n" + ("\n".join(rejects)))
        return sock

