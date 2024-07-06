from therix.core.agent import Agent
from therix.core.inference_models import (
    GroqLlama370b
)
import sys
from therix.core.trace import Trace

GROQ_API_KEY=''


agent = Agent(name="Default QNA Agent")
(
        agent.add(GroqLlama370b(config={"groq_api_key": GROQ_API_KEY}))
        .save()
    )


print(agent.id)

ans = agent.invoke(question="What is the difference between eating an apple and eating a cake?")
print(ans)