from pydantic import BaseModel


class AbstractLambdaProcessorResponse(BaseModel):
    success: bool
    res: dict


class AbstractLambdaHandlerCallbackResponse(BaseModel):
    success: bool
    res: dict
