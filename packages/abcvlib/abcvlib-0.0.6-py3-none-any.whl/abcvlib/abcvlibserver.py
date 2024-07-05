import inspect
import io
import json
import struct
import sys
import logging
import selectors
import traceback
from enum import Enum
from selectors import SelectorKey
from typing import List, Tuple, Type, Dict, Union, Any
import os
import socket
import re
from netifaces import ifaddresses, AF_INET
import pathlib

from smartphone_robot_flatbuffers import Episode


class ServerConfig(object):
    def __init__(self):
        # check if SMARTPHONE_ROBOT_CONFIG_PATH is set
        if "SMARTPHONE_ROBOT_CONFIG_PATH" in os.environ:
            self.config_path = os.environ["SMARTPHONE_ROBOT_CONFIG_PATH"]
        else:
            print(
                """
                SMARTPHONE_ROBOT_CONFIG_PATH is not set.
                This environmental variable should be set to a local copy of
                https://github.com/oist/smartphone-robot-android as a means
                to tie the android client to the python server. If this is
                the first time you are trying to set this up, please either
                download or clone that repo, and set the
                SMARTPHONE_ROBOT_CONFIG_PATH to the path of the
                config.json file within that local repo
                """
            )
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"{self.config_path} missing. ")
        else:
            with open(self.config_path) as f:
                self.config = json.load(f)

    def _get_host_from_gateway(self) -> str:
        """
        Get the host IP address by using the default gateway specified in config.ini
        @return: host ip address as a string
        """

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((self.config["DEFAULT"]["ip"], 80))
        host = s.getsockname()[0]
        s.close()
        return host

    def get_host(self) -> str:
        """
        Attempt to get the host ip automatically via iwgetid and regex magic
        This may not work across os's. Only tested on Ubuntu 20.4 so far. If
        that fails it will use the gateway specified in the config.ini
        @return: host ip address as string
        """
        try:
            host = self._ip_address_from_interface(self._get_wifi_interface())
        except AttributeError:
            host = self._get_host_from_gateway()

        return host

    def get_port(self) -> int:
        """
        get port specified in config.ini else return a default one
        @return: port number for host as int
        """

        if self.config["DEFAULT"]["port"] is not None:
            return int(self.config["DEFAULT"]["port"])
        else:
            return 3000

    @staticmethod
    def _get_wifi_interface() -> str:
        """
        Attempts to read the wifi interface name via iwgetid and regex parsing
        @return: wifi interface name as str
        """
        interface = re.search("[^ ]+", os.popen("iwgetid").read()).group(0)

        return interface

    @staticmethod
    def _ip_address_from_interface(interface: str) -> str:
        """
        Attempts to get the IPv4 address of the network interface given as an input param
        @param interface:
        @return: host ip address as str
        """
        host = ifaddresses(interface)[AF_INET][0]["addr"]
        return host

    def generate_gradle_config(self, host_ip: str, port: int):
        """
        Writes a config file in a format parsable by gradle to be used in Android for
        specifying the sever (host) ip address and port
        """
        with open(self.config_path, "r") as file:
            gradle_config = json.load(file)
            gradle_config["CUSTOM"] = {"ip": host_ip, "port": port}
        with open(self.config_path, "w") as file:
            json.dump(gradle_config, file, indent=4)


class ContentEncoding(Enum):
    UTF_8 = "utf-8"
    BINARY = "binary"


class ContentType(Enum):
    STRING = "string"
    FLATBUFFER = "flatbuffer"
    JSON = "json"
    FILES = "files"


class Response:
    def __init__(self):
        self.content_bytes = b""
        self.content_type = ContentType.FILES.value
        self.content_encoding: ContentEncoding = ContentEncoding.BINARY.value
        self.file_names: List[str] = []
        self.file_lengths: List[int] = []

    def _load_assets(self):
        for dirpath, dirnames, filenames in os.walk("./assets"):
            for filename in filenames:
                file: bytes = open(dirpath + "/" + filename, "rb").read()
                self.content_bytes += file
                self.file_lengths.append(len(file))
                self.file_names.append(filename)

    def default(self):
        self._load_assets()
        return self.to_dict()

    def to_dict(self) -> dict:
        contents: Dict[
            str, Union[Union[bytes, ContentEncoding, List[str], List[int]], Any]
        ] = {
            "content_bytes": self.content_bytes,
            "content_type": self.content_type,
            "content_encoding": self.content_encoding,
            "file_names": self.file_names,
            "file_lengths": self.file_lengths,
        }
        return contents

    def add_bytes(self, _bytes: bytes):
        self.content_bytes += _bytes

    def add_file(self, path: pathlib.Path):
        try:
            file: bytes = path.read_bytes()
        except FileNotFoundError:
            print(
                "You must specify the path to a valid file. Path given: {}".format(path)
            )
            raise
        else:
            self.content_bytes += file
            self.file_lengths.append(len(file))
            self.file_names.append(path.name)

    def add_dir(self, path: pathlib.Path):
        for dirpath, dirnames, filenames in os.walk(path, onerror=self.on_dir_error):
            for filename in filenames:
                file: bytes = open(dirpath + "/" + filename, "rb").read()
                self.content_bytes += file
                self.file_lengths.append(len(file))
                self.file_names.append(filename)

    @staticmethod
    def on_dir_error(err: OSError):
        try:
            raise NotADirectoryError("path supplied is not a directory.") from err
        except NotADirectoryError:
            f = inspect.stack()[2][0]
            traceback.print_stack(f)
            traceback.print_exc(chain=False, limit=0)

    def set_content_type(self, content_type: ContentType):
        self.content_type = content_type.value

    def set_content_encoding(self, encoding: ContentEncoding):
        self.content_encoding = encoding.value


class Message:
    def __init__(self, selector, sock, addr, **kwargs):
        self.selector = selector
        self.sock = sock
        self.addr = addr
        self._recv_buffer = b""
        self._send_buffer = b""
        self._jsonheader_len = None
        self.jsonheader = None
        self.decodedData = None
        self.response_created = False
        self.kwargs = kwargs

    def _set_selector_events_mask(self, mode):
        """Set selector to listen for events: mode is 'r', 'w', or 'rw'."""
        if mode == "r":
            events = selectors.EVENT_READ
        elif mode == "w":
            events = selectors.EVENT_WRITE
        elif mode == "rw":
            events = selectors.EVENT_READ | selectors.EVENT_WRITE
        else:
            raise ValueError(f"Invalid events mask mode {repr(mode)}.")
        self.selector.modify(self.sock, events, data=self)

    @staticmethod
    def _json_encode(obj, encoding):
        return json.dumps(obj, ensure_ascii=False).encode(encoding)

    @staticmethod
    def _json_decode(json_bytes, encoding):
        tiow = io.TextIOWrapper(io.BytesIO(json_bytes), encoding=encoding, newline="")
        obj = json.load(tiow)
        tiow.close()
        return obj

    @staticmethod
    def _flatbuffer_decode(flatbuffer_bytes):
        episode = Episode.Episode.GetRootAs(flatbuffer_bytes, 0)

        return episode

    def _create_message(
        self,
        *,
        content_bytes,
        content_type,
        content_encoding,
        file_names=None,
        file_lengths=None,
    ):

        jsonheader = {
            "byteorder": sys.byteorder,
            "content-type": content_type,
            "content-encoding": content_encoding,
            "content-length": len(content_bytes),
            "file-names": file_names,
            "file-lengths": file_lengths,
        }
        jsonheader_bytes = self._json_encode(jsonheader, "utf-8")
        message_hdr = struct.pack(">H", len(jsonheader_bytes))
        message = message_hdr + jsonheader_bytes + content_bytes
        return message

    def process_events(self, mask):
        if mask & selectors.EVENT_READ:
            self._read()
        if mask & selectors.EVENT_WRITE:
            self._write()

    def _read(self):
        try:
            # Should be ready to read
            data = self.sock.recv(134217728)
        except BlockingIOError:
            # Resource temporarily unavailable (errno EWOULDBLOCK)
            pass
        else:
            if data:
                self._recv_buffer += data
            else:
                raise RuntimeError("Peer closed.")

        if self._jsonheader_len is None:
            print("Reading protoheader from Client:" + str(self.addr))
            self._process_protoheader()

        if self._jsonheader_len is not None:
            if self.jsonheader is None:
                self._process_jsonheader()

        if self.jsonheader:
            if self.decodedData is None:
                self._process_msg()

    def _write(self):
        if self.decodedData:
            if not self.response_created:
                self._create_response()

        if self._send_buffer:
            # print("sending", repr(self._send_buffer), "to", self.addr)
            try:
                # Should be ready to write
                sent = self.sock.send(self._send_buffer)
            except BlockingIOError:
                # Resource temporarily unavailable (errno EWOULDBLOCK)
                pass
            else:
                self._send_buffer = self._send_buffer[sent:]
                # Close when the buffer is drained. The response has been sent.
                if sent and not self._send_buffer:
                    self.close()

    def close(self):
        print("closing connection to", self.addr)
        try:
            self.selector.unregister(self.sock)
        except Exception as e:
            print(
                "error: selector.unregister() exception for",
                f"{self.addr}: {repr(e)}",
            )

        try:
            self.sock.close()
        except OSError as e:
            print(
                "error: socket.close() exception for",
                f"{self.addr}: {repr(e)}",
            )
        finally:
            # Delete reference to socket object for garbage collection
            self.sock = None

    def _process_protoheader(self):

        print("Processing protoheader from Client:" + str(self.addr))

        hdrlen = 4
        if len(self._recv_buffer) >= hdrlen:
            self._jsonheader_len = struct.unpack(">I", self._recv_buffer[:hdrlen])[0]
            self._recv_buffer = self._recv_buffer[hdrlen:]

    def _process_jsonheader(self):
        print("Processing JSONheader from Client:" + str(self.addr))
        hdrlen = self._jsonheader_len
        if len(self._recv_buffer) >= hdrlen:
            self.jsonheader = self._json_decode(self._recv_buffer[:hdrlen], "utf-8")
            self._recv_buffer = self._recv_buffer[hdrlen:]
            for reqhdr in (
                "byteorder",
                "content-length",
                "content-type",
                "content-encoding",
            ):
                if reqhdr not in self.jsonheader:
                    raise ValueError(f'Missing required header "{reqhdr}".')
            print("Reading message contents from client " + str(self.addr))

    def _process_msg(self):
        content_len = self.jsonheader["content-length"]
        if not len(self._recv_buffer) >= content_len:
            return
        print("Received " + str(content_len) + "Bytes from client " + str(self.addr))
        data = self._recv_buffer[:content_len]
        self._recv_buffer = self._recv_buffer[content_len:]
        encoding = self.jsonheader["content-encoding"]
        if encoding == "json":
            self.decodedData = self._json_decode(data, encoding)
            print("received ", repr(self.decodedData), "from", self.addr)
            self._on_json_received(self.decodedData)
        if encoding == "flatbuffer":
            print("received flatbuffer from", self.addr)
            self.decodedData = self._flatbuffer_decode(data)
            self._on_episode_received(self.decodedData)
        else:
            # Binary or unknown content-type
            self.decodedData = data
            print(
                f'received {self.jsonheader["content-type"]} request from',
                self.addr,
            )
        # Set selector to listen for write events, we're done reading.
        self._set_selector_events_mask("w")
        print("selector mask set to write on " + str(self.addr))

    def _create_response(self):
        response = self._on_response_request()
        message = self._create_message(**response)
        self.response_created = True
        self._send_buffer += message

    def _on_episode_received(self, episode: Episode):
        """
        Some examples of how to unwrap flatbuffers. Make sure you enclose everythign in a try/catch and catch
        AttributeErrors in case you accidentally try to access data that hasn't been included into the flatbuffer (e.g.
        trying to access episode 7 even though only 6 have been recorded). This is similar to an IndexOutOfBounds error
        but as flatbuffers are binary objects rather than arrays, the access errors are different.
        try:
            print("-------------Example FlatBuffer Reads Start----------------")
            print("Total TimeSteps Length: " + str(episode.TimestepsLength()))
            print("WheelCounts recorded in TimeStep 0 for left wheel: " +
                  str(episode.Timesteps(0).WheelData().Left().TimestampsLength()))
            print("WheelCounts recorded in TimeStep 1 for left wheel: " +
                  str(episode.Timesteps(1).WheelData().Left().TimestampsLength()))
            print("WheelCounts recorded in TimeStep 2 for left wheel: " +
                  str(episode.Timesteps(2).WheelData().Left().TimestampsLength()))

            print("TimeStep 1 LeftWheel Timestamps Array: " +
                  str(episode.Timesteps(1).WheelData().Left().TimestampsAsNumpy()[0:10]))
            print("TimeStep 1 LeftWheel Distances Array: " +
                  str(episode.Timesteps(1).WheelData().Left().DistancesAsNumpy()[0:10]))
            print("TimeStep 1 RightWheel Distances Array: " +
                  str(episode.Timesteps(1).WheelData().Right().DistancesAsNumpy()[0:10]))
            print("TimeStep 1 LeftWheel Speeds Instantaneous Array: " +
                  str(episode.Timesteps(1).WheelData().Left().SpeedsInstantaneousAsNumpy()[0:10]))
            print("TimeStep 1 LeftWheel Speeds Buffered Array: " +
                  str(episode.Timesteps(1).WheelData().Left().SpeedsBufferedAsNumpy()[0:10]))
            print("TimeStep 1 LeftWheel Speeds Exp Avg Array: " +
                  str(episode.Timesteps(1).WheelData().Left().SpeedsExpavgAsNumpy()[0:10]))
            print("TimeStep 1 Tilt Angle Array: " +
                  str(episode.Timesteps(1).OrientationData().TiltangleAsNumpy()[0:10]))
            print("TimeStep 1 Tilt Angle Velocity Array: " +
                  str(episode.Timesteps(1).OrientationData().TiltvelocityAsNumpy()[0:10]))

            print("-------------Example FlatBuffer Reads End----------------")
        except (AttributeError, TypeError) as e:
            print("Tried to read data from flatbuffer than does not exist")
            print(e)
        @param episode:
        """
        pass

    def _on_json_received(self, json_data: json):
        pass

    def _on_response_request(self) -> dict:
        """
        Override this method to create a custom response
        This method is called after the server receives data from a client and is ready to write something back.
        @return: a dict like Response().to_dict()
        """
        response = Response().default()
        return response


class Server:
    def __init__(self, msg_type: Type[Message], **kwargs):
        self.msgType = msg_type
        self.kwargs = kwargs
        self.sel = selectors.DefaultSelector()

        # Create logs if not already present
        p = pathlib.Path("./logs/")
        if not p.is_dir():
            p.mkdir(parents=True, exist_ok=True)

        p = p / "logServer.log"
        if not p.is_file():
            p.touch()

        logging.basicConfig(
            filename=p,
            filemode="w",
            level=logging.DEBUG,
            format="%(asctime)s:  %(levelname)s: %(message)s",
        )
        server_config: ServerConfig = ServerConfig()
        host = server_config.get_host()
        port = server_config.get_port()
        server_config.generate_gradle_config(host, port)

        lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Avoid bind() exception: OSError: [Errno 48] Address already in use
        lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        lsock.bind((host, port))
        lsock.listen()
        logging.info("listening on %s : %s", host, port)
        lsock.setblocking(False)
        self.sel.register(lsock, selectors.EVENT_READ, data=None)
        logging.info("selector registered to read from any client")

    def _accept_wrapper(self, sock: socket, sel: selectors.DefaultSelector):
        conn, addr = sock.accept()  # Should be ready to read
        logging.info("accepted connection from %s", addr)
        conn.setblocking(False)
        message = self.msgType(sel, conn, addr, serverKwargs=self.kwargs)
        sel.register(conn, selectors.EVENT_READ, data=message)
        logging.info(
            "selector registered to read and message attached to %s", str(addr)
        )

    def start(self):
        try:
            while True:
                events: List[Tuple[SelectorKey, int]] = self.sel.select(
                    timeout=None
                )  # Debugger fires, but gets stuck when evaluating this.
                key: SelectorKey
                mask: int
                for key, mask in events:
                    if key.data is None:
                        self._accept_wrapper(key.fileobj, self.sel)
                    else:
                        message = key.data
                        try:
                            message.process_events(mask)
                        except Exception:
                            print(
                                "main: error: exception for %s",
                                f"{message.addr}:\n{traceback.format_exc()}",
                            )
                            message.close()
        except KeyboardInterrupt:
            print("caught keyboard interrupt, exiting")
        finally:
            self.sel.close()
