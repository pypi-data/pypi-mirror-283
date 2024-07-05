from motleycrew.common.utils import ensure_module_is_installed

try:
    from aider.coders import Coder
    from aider.models import Model
except ImportError:
    Coder = None
    Model = None

from langchain.tools import Tool
from langchain_core.pydantic_v1 import BaseModel, Field

from motleycrew.common import Defaults
from motleycrew.tools import MotleyTool


class AiderTool(MotleyTool):

    def __init__(self, model: str = None, **kwargs):
        """Tool for code generation using Aider.

        Args:
            model (str): model name
            **kwargs:
        """
        ensure_module_is_installed("aider")

        model = model or Defaults.DEFAULT_LLM_NAME
        llm_model = Model(model=model)
        coder = Coder.create(main_model=llm_model, **kwargs)

        langchain_tool = create_aider_tool(coder)
        super(AiderTool, self).__init__(langchain_tool)


class AiderToolInput(BaseModel):
    """Input for the Aider tool.

    Attributes:
        with_message (str):
    """

    with_message: str = Field(description="instructions for code generation")


def create_aider_tool(coder: Coder):
    """Create langchain tool from Aider Coder.run() method

    Returns:
        Tool:
    """
    return Tool.from_function(
        func=coder.run,
        name="aider tool",
        description="Tool for code generation that has access to the provided repository. "
        "Ask it to make changes in the code: fix bugs, add features, write tests etc. "
        "It doesn't run the code by itself.",
        args_schema=AiderToolInput,
    )
