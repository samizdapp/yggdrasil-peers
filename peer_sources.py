from abc import ABC, abstractmethod

from http.client import HTTPSConnection
from lxml.html import parse
from lxml.etree import XPath

import sys
import random
from collections import defaultdict

from yggdrasil_iface import yqq


class PeerSource(ABC):
    """Parent class of all the ways peers can be discovered.

    Attributes:
        resource: The fetched resource.
        peers: A collection of extracted peers.
    """

    @abstractmethod
    def fetch(self):
        """Grab the latest resource from the network."""

    @abstractmethod
    def extract(self, resource=None):
        """Return a list of peers from the last requested resource.

        Args:
            resource: Use this resource instead (optional).
        """

    @abstractmethod
    def write(self, fd=sys.stdout):
        """Write the contents of this object to a configuation file.

        Args:
            fd: A file descriptor (default stdout).
        """

    def perform(self):
        """Perform all steps in sequence with their defaults."""
        self.fetch()
        self.extract()
        self.write()


class PublicPeers(PeerSource):
    """First hops scraped from configured directory websites.

    Attributes:
        resource: The parsed web page.
        peers: A list of extracted peers.
        directory: The location of the page containing active peers.
        find: An XPath object that extracts peers from the directory.

    Variables:
        OVERLAP: The minimum number of peers that remain between
    subsequent calls (constant).
    """

    directory = "publicpeers.neilalexander.dev"
    find = XPath("//tr[@class='statusgood']/td[@id='address']/text()")
    OVERLAP = 3

    def __init__(self, dx=()):
        if len(dx) == 2:
            self.directory, self.find = dx
            if type(self.find) == str:
                self.find = XPath(self.find)

    def fetch(self):
        conn = HTTPSConnection(self.directory)
        conn.request("GET", "/index.html")
        self.resource = parse(conn.getresponse())
        conn.close()

    def extract(self, resource=None):
        if not resource:
            resource = self.resource
        first_hops = self.find(resource)
        self.peers = random.sample(first_hops,
                                   len(first_hops) // 2 + self.OVERLAP)
        return self.peers

    def write(self, fd=sys.stdout):
        # Yggdrasil recommends configuring only 2-3 peers.
        fd.writelines(", \n".join(self.peers[:3]))

        if fd is not sys.stdout:
            fd.close()


class CrawledPeers(PeerSource):
    """Peers that have been discovered after crawling the network.

    Attributes:
        resource: A dictionary of Yggdrasil keys to NodeInfo.
        # peers: A collection of extracted samizdApp peers.
        cohorts: A dictionary of cohorts to members.

    Variables:
        MAX_DEPTH: The furthest nodes to be reached.
    """

    MAX_DEPTH = 2

    def __init__(self, ygg):
        self.ygg = ygg

    def fetch(self):
        self.resource = dict()

        keys = [data["key"] for data in self.ygg.neighbours.values()]
        depth = 0

        while depth < self.MAX_DEPTH:
            depth += 1
            key = keys.pop()
            nodeInfo = self.ygg.query(yqq.NODEINFO(key))

            if "samizdapp" in nodeInfo.keys():
                depth += 1  # Reduce search space as cohort members are found.
                self.resource[key] = nodeInfo

            children = self.ygg.query(yqq.REMOTE_PEERS(key))["keys"]
            keys += children

    def extract(self, resource=None):
        self.cohort = defaultdict(list)

        for key, info in self.resource.items():
            for group in info["samizdapp"]["groups"]:
                if group in self.ygg.groups:
                    self.cohort[group].append(key)

    def write(self, fd=sys.stdout):
        fd.write("# Samizdapp negotiated peers:\n")
        for protocol, cohort in self.cohort.items():
            fd.write(f"## Protocol: {protocol}\n")

            for addr, name in cohort:
                fd.write(f"{addr}\t{name}\n")

        if fd is not sys.stdout:
            fd.close()
