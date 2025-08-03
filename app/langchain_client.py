from langchain_google_vertexai.model_garden import ChatAnthropicVertex
from langchain_core.messages import HumanMessage, SystemMessage
import os

# project = os.environ["PROJECT_ID"] 
# location = os.environ["REGION"]

LOCATION="us-east5" # or "europe-west1"
PROJECT_ID="avey-research"

# Initialise the Model
model = ChatAnthropicVertex(
    model_name="claude-3-5-sonnet-v2@20241022",
    project=PROJECT_ID,
    location=LOCATION,
)


def get_langchain_response(prompt):
    raw_context = ("")
    context = SystemMessage(content=raw_context)
    human = HumanMessage(content=prompt)
    response = model.invoke([context, human])
    return response.content