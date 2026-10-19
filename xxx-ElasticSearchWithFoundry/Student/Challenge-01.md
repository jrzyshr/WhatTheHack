# Challenge 01 - Meet Agent Brut Force

[< Previous Challenge](./Challenge-00.md) - **[Home](../README.md)** - [Next Challenge >](./Challenge-02.md)

## Pre-requisites

Complete Challenge 00 with working source data, a Foundry model deployment, and a read-only Elastic MCP connection.

## Introduction

A support agent must decide which data to use before it can answer. Index names and mappings describe structure, but they do not always explain business meaning. MCP lets Foundry call Elastic tools without embedding a database client in the model.

Agent Brut Force is our baseline, not a deliberately bad agent. Let it use normal discovery and retrieval tools; do not force it to scan every index.

## Description

Use `notebooks/01-Brut-Force.ipynb` in the supplied Codespace or Resources.zip. Complete the MCP tool selection, create a Foundry agent using the provided system prompt, and answer the bundled support questions with source references.

- Limit the tool list to discovery and read-only queries against your workshop sources.
- Collect actual tool calls, service-reported token usage, and final answers in fresh conversations.
- Inspect whether a query needs source discovery, current data, or an honest out-of-scope answer.

Before running a question, predict its likely source. Afterwards, explain a discovery call to your coach and record whether the final answer is correct and supported. Preserve these runs for the Optimus comparison.

## Success Criteria

- Show a Foundry agent named for **Agent Brut Force** with the scoped Elastic MCP connection.
- Verify that at least one answer uses data returned by a successful Elastic MCP call.
- Show source references supporting the answer, not just a plausible response.
- Show the recorded tool trace and input/output/total token usage, or explicitly identify missing telemetry.
- Demonstrate that the baseline cannot retrieve KIs and can acknowledge an unsupported question.

## Learning Resources

- [Elastic built-in tools](https://www.elastic.co/docs/explore-analyze/ai-features/agent-builder/tools/builtin-tools-reference)
- [Microsoft Foundry MCP integration](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/model-context-protocol)
- [ES|QL query language](https://www.elastic.co/docs/explore-analyze/query-filter/languages/esql)

## Tips

- Only approve expected, read-only calls. Check the server, tool, and arguments.
- A low token count is not success if the answer was guessed or retrieval failed.
- Tool calls and model tokens are different measurements. MCP tool discovery can also have overhead.

## Advanced Challenges

- Ask a new support question and explain why it selects a different index.
- Repeat a question in fresh conversations and compare variation without cherry-picking the cheapest result.
