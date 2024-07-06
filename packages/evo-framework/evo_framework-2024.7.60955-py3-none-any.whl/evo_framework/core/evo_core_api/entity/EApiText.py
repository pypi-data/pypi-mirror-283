#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 Internation    https://github.com/cyborg-ai-git | 
#========================================================================================================================================

from evo_framework.entity.EObject import EObject
from evo_framework.core.evo_core_type.entity.EvoMap import EvoMap

#========================================================================================================================================
"""EApiText

    EApiFile DESCRIPTION
    
"""
class EApiText(EObject):

    VERSION:str="313906d45c2af1534c8b04aea0c2aae2d51bed22adf9b9d2557a2b338421bb4d"

    def __init__(self):
        super().__init__()
        
        self.header:str = None
        self.language:str = None
        self.text:str = None
        self.isComplete:bool = None
        self.isError:bool = None
        self.tokenTot:int = 0
  
    def toStream(self, stream):
        super().toStream(stream)
        
        self._doWriteStr(self.header, stream)
        self._doWriteStr(self.language, stream)
        self._doWriteStr(self.text, stream)
        self._doWriteBool(self.isComplete, stream)
        self._doWriteBool(self.isError, stream)
        self._doWriteInt(self.tokenTot, stream)
        
    def fromStream(self, stream):
        super().fromStream(stream)
        
        self.header = self._doReadStr(stream)
        self.language = self._doReadStr(stream)
        self.text = self._doReadStr(stream)
        self.isComplete = self._doReadBool(stream)
        self.isError = self._doReadBool(stream)
        self.tokenTot = self._doReadInt(stream)
    
    def __str__(self) -> str:
        strReturn = "\n".join([
                super().__str__(),
                            
                f"\theader:{self.header}",
                f"\tlanguage:{self.language}",
                f"\ttext:{self.text}",
                f"\tisComplete:{self.isComplete}",
                f"\tisError:{self.isError}",
                f"\ttokenTot:{self.tokenTot}",
                            ]) 
        return strReturn
    