import agents.skill_agent

import agents.executor_agent


agent = agents.executor_agent.build_and_compile_agent()
#agents.executor_agent.invoke_agent(agent, "Please list the pods on the default namespace")

#agents.executor_agent.invoke_agent(agent, "Get the pods on the default namespace.")

#agents.executor_agent.invoke_agent(agent, "Get details of this pod: example-deployment-annotations-788cb86dff-d8xhp on the default namesapce")


agents.executor_agent.invoke_agent(agent, "Please check the customer notification service.")