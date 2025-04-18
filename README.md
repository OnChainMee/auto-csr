# auto-csr

_Proof of concept for agent AI customer service representative bot._

Maryville Universisty of St. Louis
COSC 643 - Ethics of Artificial Intelligence
Spring 2025

## Project Description

Providing customer service comes with a significant cost for many companies. This cost comes at a time when there is increasing pressure to reduce expenses to drive growth and profitability. At the same time, the expectations from consumers for high quality, around-the-clock assistance has grown (Carter, 2024). 

This project will demonstrate using agentic artificial intelligence (agentic AI) to automate customer service. By using agentic AI, companies can deliver high quality, personalized, and responsive customer service in a way that helps control expenses and scales. 

Agentic AI is the use of AI to create autonomous AI agents that are capable of independent action (AI agents). This form of AI itself depends on other AI such as machine learning and generative AI. Agentic AI differs from AI such as machine learning (which makes predictions or performs clustering) and generative AI (which generates content like text and images) in that it takes actions based on input. 

Acting based on input is similar to how human customer service representatives operate. Given a customer request (for instance, in a phone call, email, chat) the customer representative will take some action – collect more information, send a return shipping label, or provide store credit. 

This project will demonstrate how agentic AI can be used to both service customer requests as well as help human customer service representatives more effectively respond to customers.

## Project Plan 

Creating a sophisticated, full featured agentic AI customer service implementation would take resources (significantly) outside the time allotted for this class. However, the scope for the agent can be constrained so that the concept of the technology can be demonstrated and reveal the connection to ethical AI. 

To constrain the problem space, the agent will be an email-based agent that is capable of a fixed number of customer service tasks. Upon receiving an email, the AI agent will process the message to determine what action to take. The agent may augment the information contained in the email with other data, such as the user’s profile and purchase history. The available actions will be constrained to just a handful, such as replying for more information, replying and passing the issues on to a human representative, or replying and taking some direct action. 

Most of the intelligence from the agent will come from using a large language model (LLM) as the reasoning facility. The LLM will be provided with the support email text as input and possibly be augmented by other information (e.g., user profile retrieved via API call). The prompt for the LLM will contain the user’s message, any supporting data, and a list of actions available to the agent. The LLM will respond with whichever action it deems to be appropriate. 

The LLM will then be prompted to write a reply to the user. This reply will confirm the receipt of the user’s request and inform the user what action will be taken. If the required action needs more than just an email reply, the agent will do so (via API integration). 

This project will use Amazon Web Services for AI capabilities (such as for the LLM) and hosting for other required services. Any of the downstream services needed will be mocked so that the focus of the project is the creation of the AI agent. Email or a simple Web user interface will be used to demonstrate the customer service AI agent.

## Project Design



## Connection to Ethical AI

The agentic AI customer service agent will show how AI can be developed ethically and treat people with a sense of decency. Ethical treatment and decency will extend to both the users of the agentic AI agent and the human service agents that work alongside it. 

The AI agent will be designed to treat users with a sense of decency by acknowledging that users’ time is precious, and each user has a need that agent may be able to help with. To that end, the AI agent should be as helpful as possible. However, there may be many situations where the agent is unable to assist or uncertain what to do. In that case, the agent should collect and summarize all available information so that the inquiry can be handled by a human agent. 

The AI agent will disclose that it is a non-human entity so that users are aware that they are being serviced by AI. Furthermore, the users will always have an option to switch to a human agent for any reason, such as if they prefer interacting with a person or feel the AI agent is not meeting their needs. 

The goal of the AI agent is not to replace human customer service representatives, but to offload routine inquiries and make the human agents more efficient. For example, the AI agent can collect and summarize information so that the human agent can focus on solving the customer’s problem and spend less time hunting for data. This better together approach acknowledges the value of the human agent and has the potential to make their job more satisfying by helping customers with non-routine issues. 

This approach aligns with my personal ethical framework. First, this approach demonstrates honesty and transparency by informing users that they are being served by an AI agent. Also, users are given the choice to use AI or opt out. Instead of replacing humans (and their jobs), humans are enhanced by having AI in the system. 

## References

Carter, Rebekah. (2024, June 28). AI Customer Support: The Use Cases, Best Practices, & Ethics. CX Today. https://www.cxtoday.com/contact-center/ai-customer-support-the-use-cases-best-practices-ethics/
