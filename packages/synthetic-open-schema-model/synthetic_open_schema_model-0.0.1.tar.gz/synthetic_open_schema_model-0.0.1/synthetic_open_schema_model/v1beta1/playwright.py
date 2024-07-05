from typing import Optional

from pydantic import ConfigDict
from synthetic_open_schema_model.base import Check, CheckSpec


class PlaywrightCheckSpec(CheckSpec):
    script: Optional[str] = None
    script_file: Optional[str] = None
    
    # checks: Optional[HttpExpectList] = []
    
    

class PlaywrightCheck(Check):
    model_config = ConfigDict(extra="forbid")
    
    spec: PlaywrightCheckSpec