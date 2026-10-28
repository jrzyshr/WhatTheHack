# Challenge 02 - Build the Context Engine

[< Previous Challenge](./Challenge-01.md) - **[Home](../README.md)** - [Next Challenge >](./Challenge-03.md)

## Pre-requisites

- Completed Challenge 01 and recorded your Agent Brute Force results.
- Your Codespace from Challenge 00 with a populated `.env` file.
- Native Context Engine available in your Kibana space.

## Introduction

Agent Brute Force had to discover your data before it could answer. Elastic's Context Engine moves that recurring interpretation out of the agent's question-answering loop. Its automations generate **Knowledge Indicators (KIs)** with reusable descriptions, limitations, and query guidance. One **AI Index** can hold context about several source indices; it does not merge or replace their source documents.

In this challenge you will build the AI Index and its KIs, and retrieve the MCP endpoint that Agent Optimus will use in the next challenge. Building and refreshing context has a cost, so reduced per-question discovery is a hypothesis to measure, not a given.

## Description

- Open `notebooks/02-Context-Engine.ipynb` in your Codespace and select the provided Python kernel.
- Follow the notebook to configure a native AI Index with your four workshop sources and run the metadata-generation automation.
- Inspect the generated KIs. Be ready to explain one useful routing clue and one limitation.
- Retrieve the **Context Engine MCP endpoint**. The notebook prints it in its final cell. You can also locate it in Kibana under **Agent Builder**. Copy it somewhere safe: you will need it in Challenge 03.

## Success Criteria

- Show a native Context Engine AI Index and KIs covering more than one workshop source.
- Demonstrate how a KI helps select an index or construct a source query.
- Verify that you have the Context Engine MCP endpoint URL for Challenge 03.
- Explain why AI Index creation and refresh cost is separate from per-question token use.
- Demonstrate that a KI is reusable context, not a security boundary or an automatically current source record.

## Learning Resources

- [Context Engine concepts](https://www.elastic.co/docs/explore-analyze/ai-features/context-engine/concepts)
- [Context Engine quickstart](https://www.elastic.co/docs/explore-analyze/ai-features/context-engine/quickstart)
- [Retrieve context from an AI Index](https://www.elastic.co/docs/explore-analyze/ai-features/context-engine/retrieve-context-from-ai-index)
- [AI Index routing walkthrough](https://www.elastic.co/search-labs/blog/ai-index-building-context-agents)

## Tips

- Inspect the AI Index's actual destination and fields. Do not assume a name prefix alone creates a managed Context Engine resource.
- Installing an automation is not the same as running it. Check the execution status before inspecting KIs.
- Do not paste your Elastic API key into notebook cells or chat.

## Advanced Challenges

- Change a source's metadata, regenerate its KI, and explain the impact of stale context.
- Explore when repeated usage could offset KI generation and refresh costs.
