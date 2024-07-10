#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 Internation    https://github.com/cyborg-ai-git |
#========================================================================================================================================
from datetime import datetime, timezone
import uuid
import time
from evo_framework.core.evo_core_crypto.utility.IuCryptHash import IuCryptHash
from evo_framework.core.evo_core_text.utility.IuText import IuText

class IuKey:
    countNonce = 0
    prefixHex:bytes = b'H'
    @staticmethod
    def generateId(input_string:str = None, size: int = 32, isHash:bool = False) ->bytes:
        IuKey.countNonce +=1 
        if  IuText.StringEmpty(input_string):
            #current_time_ns = time.time_ns()
            #input_string = str(current_time_ns)
            iD = IuKey.prefixHex + IuCryptHash.toSha256Bytes(f"{uuid.uuid1()}{IuKey.countNonce}")[:size]
        else:
            if isHash:
                iD = IuKey.prefixHex + IuCryptHash.toSha256Bytes(f"{input_string}")[:size]
            else:
                iD = input_string.encode("UTF-8") #IuCryptHash.toSha256Bytes(input_string)
            
        return iD
    
    @staticmethod
    def generateTime():
        now = datetime.now(timezone.utc)  # Get the current time in UTC
        epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)  # The Unix epoch time in UTC
        time_delta = now - epoch
        timeUtc = int(time_delta.total_seconds() * 1000)  # Convert to milliseconds
        return timeUtc
    
    @staticmethod
    def toString(id: bytes) -> str:
        if not id:
            return "NOT_VALID_ID"
        else:
            if id[0] == ord(IuKey.prefixHex) and len(id) == 33:
                return id.hex()
            else:
                return id.decode("UTF-8")
              