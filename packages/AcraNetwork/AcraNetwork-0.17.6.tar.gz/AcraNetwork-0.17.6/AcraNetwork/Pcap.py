"""
.. module:: pcap
    :platform: Unix, Windows
    :synopsis: Class to pack and unpack pcap files

.. moduleauthor:: Diarmuid Collins <dcollins@curtisswright.com>

"""

__author__ = "Diarmuid Collins"
__copyright__ = "Copyright 2018"
__maintainer__ = "Diarmuid Collins"
__email__ = "dcollins@curtisswright.com"
__status__ = "Production"


import struct
import os
import time
import warnings


class PcapRecord(object):
    """
    Class that can be used to store one pcap record. A Pcap file contains one or more PcapRecords

    :type sec: int
    :type usec: int
    :type incl_len: int
    :type orig_len: int
    :type _packet: str
    """

    def __init__(self):
        self.sec: int = 0  #: Second timestamp of the record. Epoch time
        self.usec: int = 0  #: Microsecond timestamp of the record
        self.incl_len: int = 0  #: The number of bytes captured and saved in the file
        self.orig_len: int = 0  #: The number of bytesas appearded on the network when captured
        self._payload: bytes = bytes()

    # Use a property on packet so that the length is triggered on it changing
    @property
    def packet(self):
        """
        The payload within the pcap record. Payload is more accurate

        :rtype: bytes
        """
        return self._payload

    @packet.setter
    def packet(self, p: bytes) -> None:
        self._payload = p
        self.incl_len = len(p)
        self.orig_len = self.incl_len

    @property
    def payload(self):
        """
        The payload within the pcap record.

        :rtype: bytes
        """
        return self._payload

    @payload.setter
    def payload(self, p: bytes) -> None:
        self._payload = p
        self.incl_len = len(p)
        self.orig_len = self.incl_len

    def unpack(self, buf: bytes) -> None:
        """
        Unpack the pcap header. Pass in a buffer containing the header

        :type buf: bytes
        """

        if struct.calcsize(Pcap.RECORD_HEADER_FORMAT) != len(buf):
            raise ValueError("Header buffer is not the correct size to be a Pcap record header")
        (self.sec, self.usec, self.incl_len, self.orig_len) = struct.unpack(Pcap.RECORD_HEADER_FORMAT, buf)

    def pack(self) -> bytes:
        """
        Pack a PcapRecord into a buffer

        :rtype: bytes

        """
        if (
            self.sec is None
            or self.usec is None
            or self.incl_len is None
            or self.orig_len is None
            or self.packet is None
        ):
            raise ValueError("Cannot build record with undefined fields in the payload")

        return struct.pack(Pcap.RECORD_HEADER_FORMAT, self.sec, self.usec, self.incl_len, self.orig_len) + self.packet

    def setCurrentTime(self) -> bool:
        return self.set_current_time()

    def set_current_time(self):
        """
        Convienece method to set the time of the PCAP record

        :rtype: bool
        """
        currenttime = time.time()
        self.usec = int((currenttime % 1) * 1e6)
        self.sec = int(currenttime)
        return True

    def __repr__(self):
        return "LEN:{} SEC:{} USEC:{}".format(self.orig_len, self.sec, self.usec)

    def __len__(self):
        return len(self._payload)


class Pcap(object):

    """
    Create a new Pcap object with the specified filename.
    Set the mode to define read, write or append

    :param filename: The PCAP filename
    :type filename: str


    :Keyword Arguments:
        * *mode* -- r: read w: write a: append


    Pcap files look like::

        -------------- --------------- ---------------- --------------- ---------------- -------
        Global Header | Record Header | Record payload | Record Header | Record payload | .....
        -------------- --------------- ---------------- --------------- ---------------- -------

    So after opening the file, iterate through the object to read the records


    Open a PCAP file for reading. Iterate through the records.

    The pcap can also be treated a list to select the relevant object.

    >>> p = Pcap(os.path.join("existing.pcap"))
    >>> print p.network
    0
    >>> for mypcaprecord in p:
    ...    print mypcaprecord.sec
    1111
    >>> import AcraNetwork.SimpleEthernet as SimpleEthernet
    >>> eth = SimpleEthernet.Ethernet()
    >>> eth.unpack(mypcaprecord.payload)
    >>> print eth
    >>> print p[0].sec
    1111

    Write a Pcap File

    >>> p = Pcap("new.pcap", mode='w')
    >>> r = PcapRecord()
    >>> r.set_current_time()
    >>> r.payload = eth.pack()
    >>> p.write(r)
    >>> p.close()

    """

    GLOBAL_HEADER_FORMAT = "<IhhiIII"
    RECORD_HEADER_FORMAT = "<IIII"
    RECORD_HEADER_SIZE = struct.calcsize(RECORD_HEADER_FORMAT)
    GLOBAL_HEADER_SIZE = struct.calcsize(GLOBAL_HEADER_FORMAT)

    def __init__(self, filename: str, **kwargs):
        self.filename: str = filename  #: The filename of the PCAP file
        self.mode: str = kwargs.get("mode", "r")  #: The file reading mode
        self._bufferring: int = kwargs.get("buffering ", -1)  #: The file reading mode
        # Global header fields
        self.magic: int = 0xA1B2C3D4  #: The magic_number which defines the file format. Leave as is.
        self.versionmaj: int = 2  #: File format major version. Currently 2
        self.versionmin: int = 4  #: File format minor version. Currently 4
        self.zone: int = 0  #: The timezone correction in seconds. 0 = GMT
        self.sigfigs: int = 0  #: Set to 0
        self.snaplen: int = 65535  #: snapshot length. Typically unchanged
        self.network: int = 1  #: Link-layer header type. http://www.tcpdump.org/linktypes.html
        self.filesize = 0

        try:
            self.fopen = open(filename, f"{self.mode}b", self._bufferring)
        except Exception as e:
            raise IOError(f"Failed to open {self.filename}. err={e}")

        if self.mode == "r":
            self._read_global_header()
        elif self.mode == "w":
            self._write_global_header()

        try:
            self.filesize = os.path.getsize(filename)
        except Exception as e:
            self.filesize = 0

    def flush(self):
        return self.fopen.flush()

    def _read_global_header(self) -> bool:
        """
        This method will read the pcap global header and unpack it and propogate the relevant attributes
        This should be the first method to call on reading a pcap] file

        :rtype: bool
        """

        header = self.fopen.read(Pcap.GLOBAL_HEADER_SIZE)
        (
            self.magic,
            self.versionmaj,
            self.versionmin,
            self.zone,
            self.sigfigs,
            self.snaplen,
            self.network,
        ) = struct.unpack(Pcap.GLOBAL_HEADER_FORMAT, header)

        return True

    def _write_global_header(self):
        """
        Write the global header to a new pcap file

        :rtype: None
        """
        header = struct.pack(
            Pcap.GLOBAL_HEADER_FORMAT,
            self.magic,
            self.versionmaj,
            self.versionmin,
            self.zone,
            self.sigfigs,
            self.snaplen,
            self.network,
        )
        self.fopen.write(header)
        self.filesize += len(header)
        return True

    def write(self, pcaprecord: PcapRecord):
        """
        Write the supplied pcaprecord to the pcap file

        :param pcaprecord: The Pcap Record to write
        :type pcaprecord: PcapRecord
        """

        _pkt = pcaprecord.pack()
        self.fopen.write(_pkt)
        self.filesize += len(_pkt)

    def close(self):
        """
        Close the current pcap file

        :rtype: None
        """
        self.fopen.close()

    def __iter__(self):
        return self

    def next(self):
        # read the pcap header to a new object
        pcaprecord = PcapRecord()
        try:
            pcaprecord.unpack(self.fopen.read(Pcap.RECORD_HEADER_SIZE))
        except:
            raise StopIteration

        try:
            pcaprecord.packet = self.fopen.read(pcaprecord.incl_len)
        except:
            raise StopIteration
        else:
            return pcaprecord

    __next__ = next

    def __getitem__(self, item):
        self.fopen.seek(Pcap.GLOBAL_HEADER_SIZE)
        for idx, rec in enumerate(self):
            if idx == item:
                return rec
