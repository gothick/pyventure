from abc import ABC, abstractmethod
from typing import Hashable, Optional

class IVerbable(ABC):
    @abstractmethod    
    def do_verb(self, verb: Hashable, noun: Hashable = None, environment_rules: dict = {}, extras: dict = {})  -> (bool, Optional[str]):
        pass
