from pydantic import ConfigDict
from synthetic_open_schema_model.base import Check, CheckSpec, DNSHostname


class SslCheckSpec(CheckSpec):
    model_config = ConfigDict(extra="forbid")
    hostname: DNSHostname 
    checks: list

class SslCheck(Check):
    model_config = ConfigDict(extra="forbid")
    
    spec: SslCheckSpec 