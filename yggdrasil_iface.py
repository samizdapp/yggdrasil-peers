import socket as s
import json


class YggdrasilQuery():
    SELF = {"request": "getSelf"}
    PEERS = {"request": "getPeers"}
    def NODEINFO(key): return {"request": "getNodeInfo", "key": key}

    def REMOTE_SELF(key):
        return {"request": "debug_remoteGetSelf", "key": key}

    def REMOTE_PEERS(key):
        return {"request": "debug_remoteGetPeers", "key": key}


yqq = YggdrasilQuery


class YggdrasilConnection():
    """Represents a connection to the Yggdrasil daemon."""

    def __init__(self, family, address):
        self.socket = s.socket(family, s.SOCK_STREAM)
        self.socket.connect(address)

        self.props = self.query(yqq.SELF)
        self.neighbours = self.query(yqq.PEERS)

        self.key = list(self.props.values())[0]["key"]
        self.groups = self.query(yqq.NODEINFO(self.key))

    @classmethod
    def fromSocket(cls, path="/var/run/yg/yg.sock"):
        return cls(s.AF_UNIX, path)

    @classmethod
    def fromServer(cls, host="localhost", port=9001):
        return cls(s.AF_INET, (host, port))

    def query(self, query):
        # Always keep the connection to the yggdrasil daemon open.
        query["keepalive"] = True
        self.socket.send(json.dumps(query).encode("utf-8"))

        res = json.loads(self.socket.recv(1024*15))

        if res["status"] == "success":
            # Remove the nesting of response->msg->...
            return list(res["response"].values())[0]
        else:
            raise ConnectionError("Query failed.")
