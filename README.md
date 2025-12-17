This repository contains a client and server codebase. 

## Server Repository:

This codebase contains a list of laws (`docs/laws.pdf`) taken from the fictional series “Game of Thrones” (randomly pulled from a wiki fandom site... unfortunately knowledge of the series does not provide an edge on this assignment). Your task is to implement a new service (described in take home exercise document) and provide access to that service via a FastAPI endpoint running in a docker container. Please replace this readme with the steps required to run your app.

## Client Repository 

In the `frontend` folder you'll find a light NextJS app with it's own README including instructions to run. Your task here is to build a minimal client experience that utilizes the service build in part 1.



To run:
BE: `python -m uvicorn app.main:app --host localhost --port 8000 --reload`
FE: `cd frontend/ && npm run dev`


Reflective Response:
Q: What unique challenges do you foresee in developing and integrating AI regulatory agents for legal compliance from a full-stack perspective? How would you address these challenges to make the system robust and user-friendly?


A: 
Security: 
    - Should be cautious where queries of sensitive nature are relayed/recorded.
    - The underlying training data and/or document store giving context may be private/proprietary.
    - Likely need to be designed with auditing in mind,
        - both for internal troubleshooting, e.g. how/why a given response is produced at a given point in time (model, context, query)
        - and for external audit, e.g. SOC2
    - Standard (OWASP) security measures
    - Be cautious about the security beneath connected MCP servers
        - e.g. the recent Next js vulnerability (via React2Shell) could allow unauthenticated remote code execution, and depending on conncted MCP servers could leverage underlying LLMs to fish out unexpected data or prompt to run injected server side code.
        - Citation: https://nextjs.org/blog/CVE-2025-66478

Law Interpretation and LLM Jitter:
    - Asking an LLM to interpret and/or cite laws requires the LLM reasonably "understands" the laws in it's operating context. This is nontrivial even for humans (which is why lawyers exist).
    - The laws may be amended or appended to over time. Responses should try to stay up to date, but also probably safe to cite timestamps/versions the LLM is operating against.
    - Responses may be targeted for certain real-world contexts (regional jurisdictions, company specific contracts, etc), which the LLM may not immediately catch, or even be privy to.
    - LLMs can hallucinate via misinterpreting data in it's context, or not being "well tuned" to the context it is interpreting. 
        - e.g. From this sample Westeros example, for query "What if I poach an egg?"
        - received response "If you poach a thing (poaching) and are caught, you might be forced to join the Night's Watch on the Wall as punishment for the crime (poachers are among those who could be forced to join) [Source 3]. Once you join, the oath you swear washes away your crimes and debts are forgiven [Source 4]. However, breaking the oath or refusing to follow orders can be punishable by death, and women are not allowed to join [Source 4]."
        - Clearly it is anchoring on a citation regarding poaching animals, not properly interpreting poaching is also a form of cooking. (Granted, there might be some wiggle room in this context to poach, as in steal, a dragon egg).
    - Ideally should have lawyers (or well informed humans) engage with and middle-man any LLM-law operations. They may operate faster / on larger volumes of data wth the AI assist, but should still sanity check whatever the AI spits out.

UI/UX
    - Dependin on the LLM's underlying model, context, and query params, it can process and return a large volume of data (more per unit time than a human can). 
        - This can be an efficiency pro for the human, but can also be a volume con. The data should be parsed, seperated, and summarized to help the human wade through the responses. (Raw data citations should be recorded/returned to be able to troubleshoot why/where the LLM produced a given response from).
    - Give additional consideration to how much we direct the human to "one-shot" queries vs back-and-forth on a topic (the latter can cause more drift/jitter/hallucinations).
    - Should try to provide confidendce scores on responses instead of being (interpreted as) 100% affirmative/confident.
    - Should be cautious about letting end user arbitrarily query the LLM (especially because of things like the React2Shell vulnerability, which could allow unintended data fishing, or remote code execution).


        

