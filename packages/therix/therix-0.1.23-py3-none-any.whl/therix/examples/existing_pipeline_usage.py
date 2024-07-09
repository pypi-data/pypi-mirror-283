from therix.core.agent import Agent
import sys

#Executing an existing agent with session id 



if len(sys.argv) > 1:
    agent = Agent.from_id(sys.argv[1])
    question = sys.argv[2]
    session_id = None

    if len(sys.argv) < 4:
        pass
    else:
        session_id = sys.argv[3]  

    ans = agent.invoke(question, session_id)
    print(ans)
else:
    agent_id = 'your agent id'
    question = 'your question to the language model'
    session_id = 'session id for the ongoing session'
   
    agent = Agent.from_id(agent_id)

    ans = agent.invoke(question, session_id)
    print(ans)

