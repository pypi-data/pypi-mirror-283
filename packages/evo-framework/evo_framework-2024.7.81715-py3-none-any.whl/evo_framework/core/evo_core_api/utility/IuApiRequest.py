#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 Internation	https://github.com/cyborg-ai-git # 
#========================================================================================================================================

from evo_framework.core import *
import lz4.frame
import gzip
from evo_framework.entity.EObject import EObject
from evo_framework.core.evo_core_type.entity.EvoMap import EvoMap
from evo_framework.core.evo_core_api.entity import *

from evo_framework.core.evo_core_api.entity.EnumApiAction import EnumApiAction
from evo_framework.core.evo_core_api.entity.EnumApiCrypto import EnumApiCrypto
from evo_framework.core.evo_core_api.entity.EnumApiCompress import EnumApiCompress
from evo_framework.core.evo_core_api.utility.IuApi import IuApi
from evo_framework.core.evo_core_crypto import *
from evo_framework.core.evo_core_log import *
from evo_framework.core.evo_core_key import *
from evo_framework.core.evo_core_system import *

from evo_framework.core.evo_core_binary.utility.IuBinary import IuBinary
from evo_framework.core.evo_core_setting.control.CSetting import CSetting
from evo_framework.core.evo_core_text.utility.IuText import IuText
from PIL import Image
#import magic
import importlib
import subprocess

# ---------------------------------------------------------------------------------------------------------------------------------------
class IuApiRequest(object):
 # ---------------------------------------------------------------------------------------------------------------------------------------       
    @staticmethod
    def newERequest(id, 
                    publicKey ,
                    secretKey, 
                    data:bytes, 
                    chunk:int=1,
                    chunkTotal=1,
                    enumApiCrypto:EnumApiCrypto = EnumApiCrypto.ECC, 
                    ) -> ERequest:
        try:
          
            hashData = IuCryptHash.toSha256Bytes(data)
            sign = IuCryptEC.sign_data(hashData, secretKey)
                
            eRequest = ERequest()
            eRequest.id = id
            eRequest.cipher = os.urandom(44)
            eRequest.pk = publicKey
            eRequest.enumApiCrypto = EnumApiCrypto.ECC
            eRequest.time = IuKey.generateTime()
            eRequest.hash = hashData
            eRequest.sign = sign
            
             # TODO:crypt data with eRequest chiper
            if len(data) > 1024:
                eRequest.enumApiCompress = EnumApiCompress.LZ4
                eRequest.data = lz4.frame.compress(data)
            else:
                eRequest.enumApiCompress = EnumApiCompress.NONE
                eRequest.data = data
            
            return eRequest
        except Exception as exception:
            IuLog.doException(__name__, exception)
            raise exception
# ---------------------------------------------------------------------------------------------------------------------------------------       
    @staticmethod
    def newEResponse(id, 
                    publicKey ,
                    secretKey, 
                    data:bytes, 
                    chunk:int=1,
                    chunkTotal=1,
                    enumApiCrypto:EnumApiCrypto = EnumApiCrypto.ECC, 
                    ) -> EResponse:
        try:
          
            hashData = IuCryptHash.toSha256Bytes(data)
            sign = IuCryptEC.sign_data(hashData, secretKey)
            eResponse = EResponse()
            eResponse.id = id
          
            eResponse.chunk = chunk
            eResponse.chunkTotal = chunkTotal
            eResponse.hash = hashData
            eResponse.sign = sign
            # eResponse.pk = self.eApiConfig.publicKey

            # TODO:crypt data with eRequest chiper
            if len(data) > 1024:
                eResponse.enumApiCompress = EnumApiCompress.LZ4
                eResponse.data = lz4.frame.compress(data)
            else:
                eResponse.enumApiCompress = EnumApiCompress.NONE
                eResponse.data = data
            
            return eResponse
        except Exception as exception:
            IuLog.doException(__name__, exception)
            raise exception
        
 # ---------------------------------------------------------------------------------------------------------------------------------------      
    @staticmethod
    def toERequest(         
                    data:bytes, 
                    publicKey = None,
                    enumApiCrypto:EnumApiCrypto = EnumApiCrypto.ECC, 
                    enumApiCompress = EnumApiCompress.LZ4  
                    ) -> ERequest:
        try:
          
            eRequest = IuApi.toEObject(ERequest(), data)

            if isinstance(eRequest, ERequest):
                if len(eRequest.id) < 64:
                    raise Exception(f"NOT_VALID_ID_{eRequest.id}")

                # TODO:decrypt data with eRequest chiper
                
                if eRequest.enumApiCompress == EnumApiCompress.NONE:
                    pass
                
                elif eRequest.enumApiCompress == EnumApiCompress.LZ4:
                    eRequest.data = lz4.frame.decompress(eRequest.data)
                    
                elif eRequest.enumApiCompress == EnumApiCompress.GZIP:
                    eRequest.data = gzip.decompress(eRequest.data)
                

                hash = IuCryptHash.toSha256Bytes(eRequest.data)

                IuLog.doVerbose(
                    __name__,
                    f"CHUNK HASH: {eRequest.chunk} {hash!r} hash:{ eRequest.hash!r} { eRequest.hash==hash}",
                )
                if hash != eRequest.hash:
                    raise Exception(
                        f"NOT_VALID_HASH_{ eRequest.hash.hex()}_{hash.hex()}"
                    )

                if not eRequest.pk:
                    raise Exception("NOT_VALID_PK")
                
                IuLog.doVerbose(__name__, f"checkSign: {eRequest}")
                # signSha256 = IuCryptHash.toSha256Bytes(eRequest.id.encode() + hash)
                signSha256 = IuCryptHash.toSha256Bytes(hash)
                
                
                #TODO:get from PKE
                if publicKey is None:
                    publicKey= eRequest.pk
                
                isValid = IuCryptEC.verify_data(
                    eRequest.hash, eRequest.sign, publicKey
                )
                
                
                IuLog.doVerbose(
                    __name__,
                    f"checkSign: {eRequest.id} {signSha256!r} isValid:{isValid}",
                )
                
                if not isValid:
                    raise Exception("NOT_VALID_SIGN")
            
                return eRequest
            
            else:
                raise Exception("ERROR_NOT_VALID|eRequest|")
        
        except Exception as exception:
            IuLog.doException(__name__, exception)
            raise exception
        
# ---------------------------------------------------------------------------------------------------------------------------------------      
    @staticmethod
    def toEResponse(         
                    data:bytes, 
                    publicKey = None,
                    enumApiCrypto:EnumApiCrypto = EnumApiCrypto.ECC, 
                    enumApiCompress = EnumApiCompress.LZ4  
                    ) -> EResponse:
        try:
          
            eResponse = IuApi.toEObject(EResponse(), data)

            if isinstance(eResponse, EResponse):
                if len(eResponse.id) < 64:
                    raise Exception(f"NOT_VALID_ID_{eResponse.id}")

                # TODO:decrypt data with eRequest chiper
                
                if eResponse.enumApiCompress == EnumApiCompress.NONE:
                    bytesChunk = eResponse.data
                
                elif eResponse.enumApiCompress == EnumApiCompress.LZ4:
                    bytesChunk = lz4.frame.decompress(eResponse.data)
                    
                elif eResponse.enumApiCompress == EnumApiCompress.GZIP:
                    bytesChunk = gzip.decompress(eResponse.data)
                

                hash = IuCryptHash.toSha256Bytes(bytesChunk)

                IuLog.doVerbose(
                    __name__,
                    f"CHUNK HASH: {eResponse.chunk} {hash!r} hash:{ eResponse.hash!r} { eResponse.hash==hash}",
                )
                if hash != eResponse.hash:
                    raise Exception(
                        f"NOT_VALID_HASH_{ eResponse.hash.hex()}_{hash.hex()}"
                    )

                IuLog.doVerbose(__name__, f"checkSign: {eResponse}")
                # signSha256 = IuCryptHash.toSha256Bytes(eRequest.id.encode() + hash)
                signSha256 = IuCryptHash.toSha256Bytes(hash)
                
                isValid = IuCryptEC.verify_data(
                    eResponse.hash, eResponse.sign, publicKey
                )
                   
                IuLog.doVerbose(
                    __name__,
                    f"checkSign: {eResponse.id} {signSha256!r} isValid:{isValid}",
                )
                
                if not isValid:
                    raise Exception("NOT_VALID_SIGN")
            
                return eResponse
            
            else:
                raise Exception("ERROR_NOT_VALID|eResponse|")
        
        except Exception as exception:
            IuLog.doException(__name__, exception)
            raise exception