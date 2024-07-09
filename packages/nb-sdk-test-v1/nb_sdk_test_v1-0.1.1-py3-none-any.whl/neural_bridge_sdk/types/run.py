from typing import Any, Dict, List

from neural_bridge_sdk.types.message import Message
from typing_extensions import TypedDict


class RunResult(TypedDict):
  """
  Results for running an agent.
  """

  run_id: str
  messages: List[Message]
  output: Dict[str, Any]
