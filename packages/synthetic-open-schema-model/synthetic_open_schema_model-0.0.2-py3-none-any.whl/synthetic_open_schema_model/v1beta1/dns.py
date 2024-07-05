from enum import Enum
from typing import Optional

from ..base import Check, DNSHostname, CheckSpec, BaseExpect, Time
from pydantic import ConfigDict, HttpUrl, IPvAnyAddress, field_serializer


Headers = dict[str, str]

class DnsRecordType(str, Enum):
    A = "A"  # Host address (IPv4)
    AAAA = "AAAA"  # IPv6 address

    # Alias records
    CNAME = "CNAME"  # Canonical name (alias for another hostname)
    ALIAS = "ALIAS"  # Alias (similar to CNAME, less common)

    # Mail exchange records
    MX = "MX"  # Mail exchange server

    # Resource records
    NS = "NS"  # Nameserver
    PTR = "PTR"  # Pointer record
    SOA = "SOA"  # Start of authority

    # Service location records (SRV, NAPTR)
    SRV = "SRV"  # Service record
    NAPTR = "NAPTR"  # Naming authority pointer record

    # Text records
    TXT = "TXT"  # Text record
    SPF = "SPF"  # Sender Policy Framework record

    # Other common types
    HINFO = "HINFO"  # Host information
    CAA = "CAA"  # Certificate authority authorization
    AAAAAAA = "AAAAAAA"  # Experimental IPv6 address record (not widely used)
    

class HttpExpectType(str, Enum):
    duration = "duration"
    size = "size"
    statusCode = "statusCode"
    text = "text"
    headers = "headers"

 
class HttpExpect(BaseExpect):
    type: HttpExpectType
    type: str


HttpExpectList = list[HttpExpect]


class DnsCheckSpec(CheckSpec):
    model_config = ConfigDict(extra="forbid")

    hostname: DNSHostname
    resolver: list[IPvAnyAddress]
    recordType: DnsRecordType
     
    checks: Optional[HttpExpectList] = []
    

class DnsCheck(Check):
    model_config = ConfigDict(extra="forbid")

    spec: DnsCheckSpec
