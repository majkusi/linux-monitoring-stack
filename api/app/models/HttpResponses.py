from pydantic import BaseModel
import datetime
class HttpResponses(BaseModel):
    time_stamp: datetime.datetime
    http:int
    mtls_no_cert:int
    mtls_cert:int