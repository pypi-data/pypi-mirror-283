from typing import Optional, TypedDict, Literal, Dict, List, Any

from typing_extensions import NotRequired


class CORSRules(TypedDict):
    corsRuleName: str
    allowedOrigins: List[str]
    allowedOperations: List[Literal['b2_download_file_by_name', 'b2_download_file_by_id', 'b2_upload_file', 'b2_upload_part']]
    allowedHeaders: NotRequired[List[str]]
    exposeHeaders: NotRequired[List[str]]
    maxAgeSeconds: int    


LifeCycleRules = TypedDict('LifeCycleRules', {
    'daysFromHidingToDeleting': Optional[int],
    'daysFromUploadingToHiding': Optional[int],
    'fileNamePrefix': str
})


class BucketPayload(TypedDict):
    accountId: str
    bucketId: str
    bucketName: str
    bucketType: str
    bucketInfo: Dict[Any, Any]
    corsRules: List[CORSRules]
    fileLockConfiguration: 
    defaultServerSideEncryption: 
    lifecycleRules: LifeCycleRules
    replicationConfiguration: Dict[Any, Any]
    revision: int
    options: List[str]



class Bucket:
    """Represents a Backblaze B2 bucket
    
    Attributes
    ----------

    """

    __slots__ = ('')

    def __init__(
        
    )