from pydantic import BaseModel, Field

class IncompleteText(BaseModel):
    text: str = Field(description="生成的挖空的文本内容")
    blank_num: int = Field(description="需要填空的数量")