# Challenge 03 - Rise of Agent Optimus

[< Previous Challenge](./Challenge-02.md) - **[Home](../README.md)** - [Next Challenge >](./Challenge-04.md)

## Pre-requisites

- Completed Challenge 02 and have the Context Engine MCP endpoint URL.
- Your Elastic API key from Challenge 00.
- Your Agent Brute Force results table from Challenge 01.

## Introduction

Agent Optimus uses the Context Engine and its AI Index to understand your data before retrieving it. You have already built an agent in Microsoft Foundry, so this challenge repeats those steps with a different MCP endpoint. Then you will measure whether the context-first approach changes how the agent works.

> **Draft notice:** Portal menu labels change frequently. Items shown as `<PLACEHOLDER>` will be provided by your event organizer.

## Description

### Create Agent "Optimus"

- Open [Microsoft Foundry](https://ai.azure.com) and select your lab project.
- Go to **Agents** and create a new agent named `Optimus`.
- Select the same model deployment you used for Agent Brute Force.
- In **Instructions**, paste the system prompt provided below:

  `<PLACEHOLDER: Agent Optimus system prompt>`

- Add a **Custom** **Model Context Protocol (MCP)** tool:
  - Use the **Context Engine MCP endpoint** you retrieved in Challenge 02 as the remote MCP endpoint.
  - Use **Key-based** authentication with the key name `Authorization` and the value `ApiKey <your Elastic API key>`.
  - Confirm the Context Engine tools are listed, and leave tool approval enabled.

### Test Agent "Optimus"

- Open Optimus in the **Playground**.
- Ask the same sample queries you used with Agent Brute Force, each in a **new conversation**:

  `<PLACEHOLDER: list of sample queries>`

- Review and approve each MCP call. Expand the tool-call details and note which context tools were called, and whether source data was still queried for current details.
- Verify the answers come from Elastic data and match the records in Kibana.
- Ask a question the data cannot answer and observe how Optimus responds.

### Observe Agent "Optimus"

- Collect the same measurements as in Challenge 01: MCP calls, input tokens, output tokens, and total tokens, using the response details and **Tracing**.
- Add Optimus rows to your results table next to the Agent Brute Force results.
- Compare correctness, citations, calls, tokens, and latency. Explain the tradeoff, even if savings are small or negative.

## Success Criteria

- Verify that a Foundry agent named **Optimus** exists with a deployed model and the Context Engine MCP tool connected.
- Demonstrate at least one answer that uses KI context from the AI Index and current data from Elastic.
- Show a side-by-side comparison of Brute Force and Optimus for the same questions.
- Explain the observed difference in calls and tokens, including any added overhead.
- Demonstrate that Optimus can acknowledge a question the data cannot answer.

## Learning Resources

- [Use Context Engine with agents](https://www.elastic.co/docs/explore-analyze/ai-features/context-engine/use-context-engine-with-agents)
- [Connect Foundry agents to MCP server endpoints](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/model-context-protocol)
- [Set up MCP server authentication in Foundry](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/mcp-authentication)

## Tips

- Compare the same questions, model deployment, and data. Use fresh conversations.
- A native context lookup may involve list, describe, and query calls. Success does not require exactly one call.
- A low token count is not success if the answer was guessed or retrieval failed.

## Advanced Challenges

- Answer a question that requires two sources while retaining document references.
- Repeat a question in several fresh conversations and compare variation without cherry-picking.
