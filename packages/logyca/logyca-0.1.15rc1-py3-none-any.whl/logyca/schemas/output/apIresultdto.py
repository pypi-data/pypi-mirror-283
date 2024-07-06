from logyca.schemas.output.apifilterexceptiondto import ApiFilterExceptionDTO
from logyca.schemas.output.tokensdto import TokensDTO
from pydantic import BaseModel,Field
from typing import Any
from uuid import UUID, uuid4

class APIResultDTO(BaseModel):
        resultToken:TokensDTO=Field(default=TokensDTO(),description="Gets or sets object with result")
        resultObject:Any=Field(default=None,description="Gets or sets object with result")
        apiException:ApiFilterExceptionDTO=Field(description="Gets or sets error")
        resultMessage:str=Field(default='',description="Gets or sets result of negative or positive message")
        dataError:bool=Field(default=True,description="Gets or sets a value indicating whether gets or sets a value if it is data error")
        def __init__(self, **kwargs):
                kwargs['dataError'] = False
                kwargs['apiException'] = ApiFilterExceptionDTO()
                super().__init__(**kwargs)

class ValidationError(BaseModel):
        detailError: str = Field(default="")
        transactionId: str = Field(default="")

class APIResultDTOExternal(APIResultDTO):
        validationErrors: list[ValidationError] | None = Field(default=[])
        traceAbilityId: UUID  = Field(default=uuid4)
