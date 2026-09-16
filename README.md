## Learning Agentic AI using LangGraph
LangGraph is one of the most popular agentic AI frameworks available among others such as Microsoft AI Framework (MAF), CrewAI, OpenAI Agents SDK, etc.
It is developer friendly, easy to use, and supports varied features such as knowledge base, tools, observability, etc.

### Core Concepts:
**Node**: your activity OR discrete actions that you want the agent to do on your behalf. A node should only have one function. <br>
**Graph** : the relationship between nodes OR how one activity relates to another. <br>
**State**: the way information flows and deduced in the graph OR the way one part of the graph knows about activities happening in another part of the graph.

### Tools
1. Knowledge Base
2. Record Keeping:

   Multiple changes can be handled per account. Each change is stored in the **Changes** table. Each change should 
   an old state and a new state. This could be old credit card and new credit card, old cellular plan and new cellular 
   plan, etc. The columns of the **changes** table are:
    <br> <br>
   a. **Change_ID** : The primary key which identifies each record in the table uniquely. <br><br>
   b. **Change_Type** : Whether the change relates to insurance, cellular plan, etc. <br><br>
   c. **Old_State_ID** : Which can be used to look up **State** table. <br><br>
   d. **New_State_ID** : Which can be used to look up **State** table. <br><br>
   e. **Created_At** : Date and time at which the change record was created. <br><br>
   f. **Status** : Status of the change; whether or not it is completed. <br><br>
   g. **Change_Description** : Description about the change. <br><br>
    <br>
    Similarly, the state table stores info about both new and old states for pertaining to some change.
    This lets us pre-fill some states such as known cellular plans from known cellular companies such as lite, pro, max,
    etc. Its columns are:

    a. **State_ID** : the primary key <br><br> b. **Candidate_Name** : the entity responsible for providing the service related to the change. <br><br> c. **Price** : Price of the service <br><br>
    d. **Price Type**: Whether the price is weekly, monthly, etc. <br><br> e. **Unique Value**: Info about the state regarding what services the user can have.