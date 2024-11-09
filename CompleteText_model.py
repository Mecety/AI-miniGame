from pydantic import BaseModel, Field

class CompleteText(BaseModel):
    completeText1: str = Field(description="补全空之后的文本内容")
    completeText2: str = Field(description="补全文本后根据填空内容进行改写的文本内容")

