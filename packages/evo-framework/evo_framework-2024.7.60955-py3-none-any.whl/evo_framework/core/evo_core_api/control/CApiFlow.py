logo: str = """
#========================================================================================================================================
#                                                                                                                                       #
#                                 00000                                                                                                 #
#                                00   00                                                                                                #
#                 0000          0     0                                                                                                 #
#                800  007        0     0                                     0000                                                       #
#                0      7       00 00000                  4800000008         0  0                                      800008   6882    #
#                0     000  006 0 00                    580        08        0  0                                     80    0      8    #
#                800000  0000 00000                    28   00000   0000  0000  000000000000000000000000000000000    80  9  09  9  8    #
#                     000   0    00     8006           8   04   8000   0000  0        00        00              0    0   0   09 9  8    #
#                      0  0       0000000  083         8   8     8800   00  00  0000      0000   0   00  0000   0   00  000   0 9  8    #
#            58000800000          00    0    3         28  0088800 000  0   00  00 00     00 00  0  00   0000   0  00         089  8    #
#            8    00   00         00000     83          8     0     800    000   000   0   000   0  000         0  0   00000   08  8    #
#                  0000000      000   8000084           3880      008 00  00 0  0    0000      000  0 000   0   0  0  08   90   9  8    #
#            8     0     00000000                          68000008  00  00  000000000  00000000 0000 0  0000  00  0000     68088882    #
#            4800008         0  00                                   0   0                            00      00                        #
#                           000  000                                 00000                             00000000                         #
#                           0 0    0                                                                                                    #
#                           0      0                                                                                                    #
#                           00000000                                                                                                    #
#                                                                                                                                       #
# CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International       https://github.com/cyborg-ai-git     #
#========================================================================================================================================
"""
from evo_framework.core import *
from evo_framework.entity.EObject import EObject
from evo_framework.core.evo_core_type.entity.EvoMap import EvoMap
from evo_framework.core.evo_core_log.utility.IuLog import IuLog
from evo_framework.core.evo_core_api.entity.EApiConfig import EApiConfig
from evo_framework.core.evo_core_key.utility.IuKey import IuKey
from evo_framework.core.evo_core_crypto.utility.IuCryptEC import IuCryptEC
from evo_framework.core.evo_core_crypto.utility.IuCryptHash import IuCryptHash
from evo_framework.core.evo_core_log.utility.IuLog import IuLog
from evo_framework.core.evo_core_system.utility.IuSystem import IuSystem
from evo_framework.core.evo_core_convert.utility.IuConvert import IuConvert
from evo_framework.core.evo_core_setting.control.CSetting import CSetting
from evo_framework.core.evo_core_log.utility.IuLog import IuLog
from evo_framework.core.evo_core_api.entity.EActionTask import EActionTask
from evo_framework.core.evo_core_api.entity.ERequest import ERequest
from evo_framework.core.evo_core_api.entity.ERequestInfo import ERequestInfo
from evo_framework.core.evo_core_api.entity.EResponse import EResponse
from evo_framework.core.evo_core_api.entity.EApi import EApi
from evo_framework.core.evo_core_api.entity.EAction import EAction
from evo_framework.core.evo_core_api.entity.EnumApiAction import EnumApiAction
from evo_framework.core.evo_core_api.entity.EnumApiCrypto import EnumApiCrypto
from evo_framework.core.evo_core_api.entity.EnumApiCompress import EnumApiCompress
from evo_framework.core.evo_core_api.entity.EnumApiType import EnumApiType
from evo_framework.core.evo_core_api.entity.EnumApiVisibility import EnumApiVisibility
from evo_framework.core.evo_core_setting.utility.IuSettings import IuSettings
from evo_framework.core.evo_core_totp.utility.IuTotp import IuTotp
from evo_framework.core.evo_core_api.utility.IuApi import IuApi
from evo_framework.core.evo_core_file.utility.IuFile import IuFile
from evo_framework.core.evo_core_api.utility.IuApiRequest import IuApiRequest
import lz4.frame
import requests
from functools import partial


# ---------------------------------------------------------------------------------------------------------------------------------------
# CApi
# ---------------------------------------------------------------------------------------------------------------------------------------
class CApiFlow:
    __instance = None

    def __init__(self):
        if CApiFlow.__instance is not None:
            raise Exception("ERROR_SINGLETON")
        else:
            super().__init__()
            CApiFlow.__instance = self
            self.version = "20240411"
            self.path = os.path.dirname(os.path.abspath(__file__))
            self.__url_server = "https://cyborgai-api.fly.dev"
            # self.__url_server= 'http://127.0.0.1:8000'
            self.__pk_server = "1de18b4372c9aff7e0b893ded10baea4a20d4352612e6883d1623a0b105d8bb5591ceab0818838fd82752dca9454df963cc37407e173a258ee700f3e4bcde2ff"  # pinning

            self.__url_cyborgai = f"{ self.__url_server}/v2/set_node/"
            self.eApiConfig: EApiConfig = EApiConfig()
            self.mapFileHandler = {}
            self.mapEFileConfig = EvoMap()
            self.isSetEConfig: bool = False
            self.mapEAction: EvoMap = EvoMap()
            self.mapERequestInfo: EvoMap = EvoMap()
            self.isEndPoint = False
            self.strSettingsStart: str = None
            self.pathTemp: str = None

    # ---------------------------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def getInstance():
        if CApiFlow.__instance is None:
            cObject = CApiFlow()
        return CApiFlow.__instance

    # ---------------------------------------------------------------------------------------------------------------------------------------
    def doInit(self, isEndPoint=False):
        try:
            self.pathTemp = CSetting.getInstance().doGet("CYBORGAI_PATH_TMP")
            
            if self.pathTemp is None:
                self.pathTemp = "/tmp/cyborgai/chunk"
                IuLog.doWarning(__name__, f"PATH_TMP:{self.pathTemp}")
            
            IuFile.doCreateDirs(self.pathTemp)

            self.isEndPoint = isEndPoint
            CSetting.getInstance().doInit()
            # @TODO:add to PostQuantum Crypto
            self.eApiConfig.enumApiCrypto = EnumApiCrypto.ECC
            self.eApiConfig.os = IuSystem.get_os_info()
            print(logo)
            self.__doGenenerateCryptoKey()

            if not self.isEndPoint:
                pass
            else:
                IuLog.doVerbose(
                    __name__,
                    f"\nPUBLICK KEY:\n{IuConvert.toHex(self.eApiConfig.publicKey)}",
                )

        except Exception as exception:
            IuLog.doException(__name__, exception)
            raise Exception

    # ---------------------------------------------------------------------------------------------------------------------------------------
    async def doInitEApiConfig(self):
        try:
            IuLog.doVerbose(__name__, f"eApiConfig:\n{self.eApiConfig}\n")

            if not self.isEndPoint:
                if self.eApiConfig.enumApiVisibility != EnumApiVisibility.LOCAL:
                    eResponseCyborgAI = await self.__doSetEApiConfig()
                    self.eApiConfig.cyborgaiToken = eResponseCyborgAI.data.decode("utf-8")
                    IuLog.doVerbose(
                        __name__, f"cyborgai peerID:{  self.eApiConfig.cyborgaiToken}"
                    )
                else:
                    IuLog.doWarning(
                        __name__, "LOCAL PEER NO CALL TO REGISTER THE PEER"
                    )
                    self.eApiConfig.cyborgaiToken = f"{self.eApiConfig.remoteUrl}"

        except Exception as exception:
            IuLog.doException(__name__, exception)
            raise Exception

    # ---------------------------------------------------------------------------------------------------------------------------------------
    def doGenerateTotp(self) -> str:
        try:
            randBase32 = IuTotp.doGenerateRand()
            urlTotp = IuTotp.doGenerateUrl(
                randBase32, self.eApiConfig.label, f"CyborgAI_{self.eApiConfig.label}"
            )
            return urlTotp
        except Exception as exception:
            IuLog.doException(__name__, exception)
            raise exception

    # ---------------------------------------------------------------------------------------------------------------------------------------
    def __doGenenerateCryptoKey(self):
        try:
            if self.eApiConfig.enumApiCrypto == EnumApiCrypto.ECC:
                privateKeyStr = CSetting.getInstance().doGet("CYBORGAI_SK")

                if privateKeyStr is None:
                    sk, pk = IuCryptEC.generate_key_pair()
                    IuLog.doVerbose(__name__, f"key generate :{sk} {pk}")
                    self.eApiConfig.secretKey = sk
                    self.eApiConfig.publicKey = pk.to_string()
                    self.eApiConfig.isFirstStart = True
                    # IuLog.doVerbose(__name__, f"\nSECRET KEY:\n{IuConvert.toBase64(sk.to_string())}\nATTENTION NOT SHARE")
                    skBase64 = IuConvert.toBase64(sk.to_string())
                    totp = self.doGenerateTotp()  
                    cyborgaiID = IuCryptHash.toSha256(self.eApiConfig.publicKey)
                    mapSettings = {"CYBORGAI_ID": cyborgaiID, "CYBORGAI_SK": skBase64, "CYBORGAI_ADMIN_OTP": totp}

                    self.eApiConfig.strBase64Start = IuSettings.doEncryptSettings(mapSettings)
                else:
                    sk, pk = IuCryptEC.get_key_pair(privateKeyStr)
                    IuLog.doVerbose(__name__, f"key regenerate :{sk} {pk}")
                    self.eApiConfig.secretKey = sk
                    self.eApiConfig.publicKey = pk.to_string()
                    self.eApiConfig.isFirstStart = False

            else:
                # TODO:add PQ crypto
                raise Exception(f"NOT_VALID_{self.eApiConfig.enumApiCrypto}")

            IuLog.doVerbose(__name__, f"sk,{self.eApiConfig.secretKey}")
            self.eApiConfig.id = IuCryptHash.toSha256(self.eApiConfig.publicKey)
            self.eApiConfig.doGenerateTime()

            if self.eApiConfig.secretKey is None:
                raise Exception("NOT_VALID_PRIVATE_KEY")

        except Exception as exception:
            IuLog.doException(__name__, exception)
            raise

    # ---------------------------------------------------------------------------------------------------------------------------------------
    async def __doSetEApiConfig(self) -> EResponse:
        try:
            IuLog.doVerbose(__name__, f"self{self.eApiConfig}")
            
            data=self.eApiConfig.toBytes()
            eRequest = IuApiRequest.newERequest(
                                                id=self.eApiConfig.id,
                                                publicKey=self.eApiConfig.publicKey,
                                                secretKey=self.eApiConfig.secretKey,
                                                data=data
                                                )
            
            IuLog.doDebug(__name__, f"cyborgai eRequest:{eRequest}")
            
            dataERequest = eRequest.toBytes()

            headers = {
                "Content-Type": "application/binary",
                # 'Authorization': 'Bearer YourAuthToken',
            }
            IuLog.doDebug(__name__, f"self.__url_cyborgai:{self.__url_cyborgai}")

            response = requests.post(
                self.__url_cyborgai, data=dataERequest, headers=headers
            )
            IuLog.doDebug(__name__, f"response.status_code:{response.status_code}")

            if response.status_code == 200:
                dataPack = response.content
                dataLength = struct.unpack("<l", dataPack[:4])[0]
                dataEResponse = dataPack[4:4+dataLength]
                
                pkServer = IuConvert.fromHex(self.__pk_server)
                
                eResponse = IuApiRequest.toEResponse( data=dataEResponse, publicKey=pkServer)

                self.eApiConfig.cyborgaiToken = eResponse.data.decode()
                self.isSetEConfig = True
                return eResponse
            
            else:
                raise Exception(
                    f"ERROR_FAILED_REGISTER_PEER_TO_CYBORGAI:{response.status_code}"
                )

        except Exception as exception:
            IuLog.doError(__name__, f"{exception}")
            raise

    # ---------------------------------------------------------------------------------------------------------------------------------------
    async def onRequest(
        self, dataERequest: bytes, checkSign: bool = False
    ):  # -> Tuple[ERequestInfo, bytes]:
        try:
            # dataDecompressed = lz4.frame.decompress(dataERequest)
            eRequest = IuApiRequest.toERequest(data=dataERequest)

            IuLog.doVerbose(__name__, f"eRequest:{eRequest}")
            file_path = f"/tmp/{eRequest.id}.eam"
            bytesChunk = eRequest.data
            
            if eRequest.chunk == eRequest.chunkTotal:
                dataReturn = None
                if eRequest.id in self.mapFileHandler:
                    file = self.mapFileHandler[eRequest.id]
                    await file.write(bytesChunk)
                    await file.flush()
                    file.close()
                    del self.mapFileHandler[eRequest.id]
                    # channel.send(dataResponse)

                    async with aiofiles.open(file_path, mode="rb") as file:
                        dataReturn = await file.read()
                    IuLog.doDebug(__name__, f"COMPLETE CHUNK:{len(dataReturn)}")

                else:
                    dataReturn = bytesChunk

                eRequestInfo = ERequestInfo()
                eRequestInfo.id = eRequest.id
                eRequestInfo.pk = eRequest.pk
                eRequestInfo.cipher = eRequest.cipher
                eRequestInfo.doStartTime()

                self.mapERequestInfo.doSet(eRequestInfo)

                return (eRequestInfo, dataReturn)

            else:
                if eRequest.id not in self.mapFileHandler:
                    file = await aiofiles.open(file_path, mode="ab")
                    self.mapFileHandler[eRequest.id] = file

                file = self.mapFileHandler[eRequest.id]
                await file.write(bytesChunk)
                await file.flush()

        except Exception as exception:
            IuLog.doException(__name__, exception)
            raise Exception

    # ---------------------------------------------------------------------------------------------------------------------------------------
    async def onResponse(
        self,
        eRequestInfo: ERequestInfo,
        data: bytes,
        chunk: int = 1,
        chunkTotal: int = 1,
        isComplete: bool = True,
    ) -> bytes:
        try:
            IuLog.doDebug(__name__, f"onResponse:{eRequestInfo} isComplete:{isComplete}")

            eResponse = IuApiRequest.newEResponse(
                                                id=eRequestInfo.id,
                                                publicKey=self.eApiConfig.publicKey, 
                                                  secretKey=self.eApiConfig.secretKey,
                                                  data=data,
                                                  chunk=chunk,
                                                  chunkTotal=chunkTotal
                                                  )

            dataEResponse = eResponse.toBytes()

            if dataEResponse is None:
                raise Exception("ERROR_NOT_VALID_ERESPONSE")

            IuLog.doVerbose(
                __name__, f"eResponse {len(data)} {len(dataEResponse)} {eResponse}"
            )

            if isComplete:
                eRequestInfo.doStopTime()
                IuLog.doVerbose(
                    __name__,
                    f"response:{eRequestInfo.id} time: {eRequestInfo.elapsedTimeStr} ",
                )
                self.mapERequestInfo.doDel(eRequestInfo.id)
            else:
                IuLog.doVerbose(
                    __name__,
                    f"response:{eRequestInfo.id} partial time: {eRequestInfo.doGetElapsedPartial()} ",
                )

            dataPack = struct.pack("<l", len(dataEResponse)) + dataEResponse
            return dataPack

        except Exception as exception:
            IuLog.doException(__name__, exception)
            raise

    # ---------------------------------------------------------------------------------------------------------------------------------------
    def doSetEApi(self, eApi: EApi):
        try:
            self.eApiConfig.mapEApi.doSet(eApi)
        except Exception as exception:
            IuLog.doException(__name__, exception)
            raise

    # ---------------------------------------------------------------------------------------------------------------------------------------
    def doGetEApi(self, action) -> EApi:
        try:
            eApi = self.eApiConfig.mapEApi.doGet(action)

            if isinstance(eApi, EApi):
                return eApi

            else:
                raise Exception(f"NOT_VALID_api_{action}")
        except Exception as exception:
            IuLog.doException(__name__, exception)
            raise 

    # ---------------------------------------------------------------------------------------------------------------------------------------
    def doPrintMapEApi(self):
        try:
            listStr = ""
            count = 1
            for key in self.eApiConfig.mapEApi.keys():
                eApi: EApi = self.eApiConfig.mapEApi.doGet(key)
                callback = eApi.callback
                idApi = str(eApi.id)
                countStr = str(count).ljust(4, " ")
                listStr = "\n".join(
                    [
                        listStr,
                        (
                            f"{countStr} {idApi}:\n" 
                            + f"\t\tinput: {eApi.input}\n" 
                            + f"\t\toutput: {eApi.output}\n" 
                            + f"\t\tcallback: {callback.__module__}.{callback.__name__}\n"   
                            ),
                    ]
                )
                count += 1

            IuLog.doInfo("api", f"{listStr}\n")

        except Exception as exception:
            IuLog.doException(__name__, exception)
            raise 

    # ---------------------------------------------------------------------------------------------------------------------------------------
    async def onAction(self, eApi: EApi, eActionTask: EActionTask):
        try:
            eActionTask.eActionOutput = await eApi.callback(eActionTask.eActionInput)
            return eActionTask.eActionOutput
        except Exception as exception:
            IuLog.doException(__name__, exception)
            raise exception

    # ---------------------------------------------------------------------------------------------------------------------------------------
    async def onActionStream(self, eApi: EApi, eActionTask: EActionTask):
        try:
            async for eActionOutput in eApi.callback(eActionTask.eActionInput):
                yield eActionOutput
        except Exception as exception:
            IuLog.doException(__name__, exception)
            raise 

    # ---------------------------------------------------------------------------------------------------------------------------------------
    async def onActionCallBack(self, eApi: EApi, eActionTask: EActionTask):
        try:
            eActionTask.eActionOutput = await eApi.callback(eActionTask.eActionInput)
            await eActionTask.evoCallback(eActionTask)
        except Exception as exception:
            IuLog.doException(__name__, exception)
            raise 

    # ---------------------------------------------------------------------------------------------------------------------------------------
    async def onActionStreamCallback(self, eApi: EApi, eActionTask: EActionTask):
        try:
            async for eActionOutput in eApi.callback(eActionTask.eActionInput):
                eActionTask.eActionOutput = eActionOutput
                await eActionTask.evoCallback(eActionTask)
        except Exception as exception:
            IuLog.doException(__name__, exception)
            raise 

    # ---------------------------------------------------------------------------------------------------------------------------------------
    async def doActionCallBack(self, eActionTask: EActionTask):
        try:
            IuLog.doDebug(__name__, f"OnActionThread: {eActionTask}")
            eApi = self.doGetEApi(eActionTask.action)
            
            self.run_in_background(self.onActionStreamCallback, eApi, eActionTask)

        except Exception as exception:
            IuLog.doException(__name__, exception)
            raise 

    # ---------------------------------------------------------------------------------------------------------------------------------------
    def start_async_loop(self, loop):
        try:
            asyncio.set_event_loop(loop)
            loop.run_forever()
        except Exception as exception:
            IuLog.doException(__name__, exception)

    # ---------------------------------------------------------------------------------------------------------------------------------------
    def run_in_background(self, target, actionFunc, eActionTask: EActionTask):
        try:
            eActionTask.loop = asyncio.new_event_loop()
            eActionTask.threadBackground = threading.Thread(
                target=self.start_async_loop, args=(eActionTask.loop,), daemon=True
            )
            eActionTask.threadBackground.start()
            self.mapEAction.doSet(eActionTask)

            if asyncio.iscoroutinefunction(target):
                coroutine = partial(target, actionFunc, eActionTask)
                asyncio.run_coroutine_threadsafe(coroutine(), eActionTask.loop)
            else:
                raise TypeError(
                    f"target function {target.__name__} must be an asynchronous function"
                )
        except Exception as exception:
            IuLog.doException(__name__, exception)

    # ---------------------------------------------------------------------------------------------------------------------------------------
    async def doStop(self):
        try:
            for eAction in self.mapEAction.__dictionary.values:
                try:
                    if isinstance(eAction, EActionTask):
                        if eAction.loop:
                            asyncio.run_coroutine_threadsafe(
                                eAction.loop.stop(), eAction.loop
                            )
                            eAction.threadBackground.join()
                            eAction.loop = None
                            eAction.threadBackground = None
                except Exception as exception:
                    IuLog.doException(__name__, exception)
        except Exception as exception:
            IuLog.doException(__name__, exception)

    # ---------------------------------------------------------------------------------------------------------------------------------------
    async def doEAction(self, dataERequest) -> EAction:
        try:
            IuLog.doDebug(__name__, f"doEAction: {len(dataERequest)}")
            eRequestInfo, dataInput = await self.onRequest(dataERequest, checkSign=True)
            IuLog.doDebug(__name__, f"eRequestInfo: {eRequestInfo}")
            IuLog.doDebug(__name__, f"dataInput length: {len(dataInput)}")
            eAction = IuApi.toEObject(EAction(), dataInput)
            if isinstance(eAction, EAction):
                try:
                    eApi = self.doGetEApi(eAction.action)
                    eActionTask = EActionTask()
                    eActionTask.id = eRequestInfo.id
                    eActionTask.doGenerateTime()
                    eActionTask.action = eAction.action
                    eActionTask.eActionInput = eAction
                    
                    async for eActionOutput in self.onActionStream(
                        eApi, eActionTask
                    ):
                        isComplete = False
                        if (
                            eAction.enumApiAction == EnumApiAction.COMPLETE
                            or eAction.enumApiAction == EnumApiAction.ERROR
                            or eAction.enumApiAction == EnumApiAction.NONE
                        ):
                            isComplete = True

                        dataAction = eActionOutput.toBytes()
                        IuLog.doDebug(__name__, f"eActionOutput:{eActionOutput}")
                        dataResponse = await self.onResponse(
                            eRequestInfo, dataAction, isComplete=isComplete
                        )
                        IuLog.doInfo(
                            __name__,
                            f"{eAction.action} id:{eActionOutput.id} len:{len(dataResponse)} {eRequestInfo.doGetElapsedPartial()}",
                        )
                        yield dataResponse
                except Exception as exception:
                    IuLog.doException(__name__, exception)
                    eAction.doSetError(f"{exception}")
                    dataResponse = await self.onResponse(
                        eRequestInfo, eAction.toBytes()
                    )
                    yield dataResponse
            else:
                raise Exception("ERROR_NOT_VALID|eAction|")
            
        except Exception as exception:
            IuLog.doException(__name__, exception)
            raise 
