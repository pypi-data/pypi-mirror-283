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
    @staticmethod
    def generateId(input_string:str = None):
        IuKey.countNonce +=1 
        if  IuText.StringEmpty(input_string):
            current_time_ns = time.time_ns()
            input_string = str(current_time_ns)
            iD = IuCryptHash.toSha256(f"{input_string}{IuKey.countNonce}")
        else:
            iD = IuCryptHash.toSha256(input_string)
        return iD
    
    @staticmethod
    def generateTime():
        now = datetime.now(timezone.utc)  # Get the current time in UTC
        epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)  # The Unix epoch time in UTC
        time_delta = now - epoch
        timeUtc = int(time_delta.total_seconds() * 1000)  # Convert to milliseconds
        return timeUtc
       
        
        
        
        