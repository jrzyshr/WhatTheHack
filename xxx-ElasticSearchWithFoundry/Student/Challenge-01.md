# Challenge 01 - Connect Foundry Agent to Elastic

[< Previous Challenge](./Challenge-00.md) - **[Home](../README.md)** - [Next Challenge >](./Challenge-02.md)

## Pre-requisites

- Completed Challenge 00: your Elastic sample indices and ES|QL MCP tools exist in Kibana.
- Your Elastic **Kibana URL** and **Elastic API key** from Challenge 00.
- Your Azure lab credentials.

## Introduction

A support agent must decide which data to use before it can answer. Index names and mappings describe structure, but they do not always explain business meaning. The Model Context Protocol (MCP) lets Microsoft Foundry call Elastic tools without embedding a database client in the model.

Agent Mole is going to have to dig around blindly in your data to find the answers. It is our baseline, not a deliberately bad agent. It is connected to the Elastic MCP endpoint that exposes the individual workshop indices, so it has to discover which data to query before it can answer. In this challenge you will build it in the Microsoft Foundry portal, test it, and measure what it costs to answer questions.

> **Draft notice:** Portal menu labels change frequently. If a label below does not match what you see, look for the closest equivalent or ask your coach. Items shown as `<PLACEHOLDER>` will be provided by your event organizer.

## Description

### Create Agent "Mole"

- Open [Microsoft Foundry](https://ai.azure.com) and sign in with the Azure credentials from your lab environment. Make sure the **New Foundry** experience toggle is on, if one is shown.
- Select the Foundry project provided by your lab environment. `<PLACEHOLDER: lab project name, or instructions to create one>`
- **Deploy a model** to power the agent:
  - Go to **Models + endpoints** (or **Model catalog**) and select **Deploy a base model**.
  - Search for `gpt-5-mini` (a small, low-cost reasoning model) and select **Confirm**. If it is unavailable in your lab region or quota, use the model your coach recommends. `<PLACEHOLDER: confirmed model for the lab>`
  - Select **Deploy** using the **Global Standard** deployment type and the default settings.
  - Wait until the deployment status is **Succeeded**.
- **Create the agent:**
  - Go to **Agents** and select **Create agent** (or **New agent**).
  - Name the agent `Mole` (Foundry may not accept spaces in agent names).
  - Select the model deployment you just created.
  - In the **Instructions** box, paste the system prompt provided below:

    `<PLACEHOLDER: Agent Mole system prompt>`

  - Save the agent.
- **Get the Elastic MCP URL** from Kibana:
  - Open your Kibana URL in another browser tab.
  - Open **Agent Builder**, go to **Tools**, and select **Manage MCP** (or **MCP server**), then **Copy MCP Server URL**.
  - If you cannot find the button, build the URL yourself: `<YOUR_KIBANA_URL>/api/agent_builder/mcp`.

  `<PLACEHOLDER: Screenshot showing where to copy the MCP server URL in Kibana>`

- **Connect the agent to Elastic:**
  - Back in your agent in Foundry, find **Tools** and select **Add**, then choose **Custom** and **Model Context Protocol (MCP)**.
  - Enter a name such as `elastic-mcp` and paste the **MCP server URL** as the remote MCP endpoint.
  - Set the authentication to **Key-based**. Add a credential with the key name `Authorization` and the value `ApiKey <your Elastic API key>` (replace the placeholder with your encoded key from Challenge 00; keep the word `ApiKey` and the space).
  - Select **Connect** (or **Create**) and confirm the Elastic tools are listed. If the tool list shows an error, re-check the URL and key.
  - Leave tool approval enabled so that you can inspect each call.

  `<PLACEHOLDER: Screenshot of the completed MCP tool connection in Foundry>`

### Test Agent "Mole"

- Open the agent in the **Playground** (use **Try in playground** or the chat pane next to the agent).
- Ask the agent each of these sample queries in a **new conversation** each time:

  `<PLACEHOLDER: list of sample queries>`

- When the agent asks for approval to run an MCP tool, expand the request, review the tool name and arguments, and approve it only if it is a read-only call against your workshop data.
- After each answer, expand the tool-call details in the response to see which Elastic tools were called and in what order.
- Verify the answer is based on Elastic data by finding the same records in Kibana **Discover** (or the index **Documents** tab).
- Ask at least one question the sample data cannot answer, and observe whether the agent says so instead of guessing.

### Observe Agent "Mole"

Observe how many calls and tokens the agent needed. You will compare these numbers with Agent Optimus in the next challenge.

- In the Playground, open the details for a response (for example **View run info**, **Thread info**, or **Metrics**) and note the **input tokens**, **output tokens**, and **total tokens** where shown.
- In your Foundry project, open **Tracing** (under **Observability**). Open the trace for a conversation and count how many MCP tool calls were made before the final answer. `<PLACEHOLDER: instructions to enable tracing/Application Insights, if not pre-configured by the lab>`
- Look for aggregate token and cost metrics in **Monitoring** (under **Observability**), or in **Models + endpoints** by selecting your model deployment and opening its **Metrics** tab.
- As an alternative for cost, open your subscription in the Azure portal under **Cost Management**. Cost data can lag by many hours, so token counts are the more reliable measure in a short workshop.
- Record your observations in a table like this for each sample query:

  | Query | MCP calls | Input tokens | Output tokens | Total tokens | Answer correct and supported? |
  | --- | --- | --- | --- | --- | --- |
  | `<query>` | | | | | |

## Success Criteria

- Verify that a Foundry agent named for **Mole** exists with a deployed model and the system prompt.
- Verify that the agent has an Elastic MCP tool connected, with the Elastic tools listed.
- Demonstrate at least one answer that uses data returned by a successful Elastic MCP tool call.
- Show that the answer matches records you found in Kibana.
- Show your table of MCP calls and input, output, and total tokens for each sample query, or identify which telemetry was unavailable.
- Demonstrate that the agent can acknowledge a question the data cannot answer.

## Learning Resources

- [Connect Foundry agents to MCP server endpoints](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/model-context-protocol)
- [Set up MCP server authentication in Foundry](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/mcp-authentication)
- [Elastic Agent Builder MCP server](https://www.elastic.co/docs/explore-analyze/ai-features/agent-builder/mcp-server)
- [Elastic Agent Builder built-in tools](https://www.elastic.co/docs/explore-analyze/ai-features/agent-builder/tools/builtin-tools-reference)

## Tips

- Only approve expected, read-only calls. Check the server, tool, and arguments before approving.
- Treat the Elastic API key like a password. Do not paste it in chat or screenshots.
- A low token count is not success if the answer was guessed or retrieval failed.
- Tool calls and model tokens are different measurements. MCP tool discovery can also add overhead.

## Advanced Challenges

- Ask the same question in several fresh conversations and compare the variation without picking only the cheapest result.
- Ask a new support question and explain why the agent picks a different index.
