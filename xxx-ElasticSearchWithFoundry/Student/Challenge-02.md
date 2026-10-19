# Challenge 02 - Give Optimus Context

[< Previous Challenge](./Challenge-01.md) - **[Home](../README.md)** - [Next Challenge >](./Challenge-03.md)

## Pre-requisites

Complete Challenge 01 and retain its baseline evidence. Native Context Engine must be available.

## Introduction

Context Engine moves recurring interpretation out of the agent's question-answering loop. Its automations generate **Knowledge Indicators (KIs)** with reusable descriptions, limitations, and query guidance. One AI Index can hold context about several source indices; it does not merge or replace their source documents.

Optimus uses these KIs to choose a source before retrieving current details. Building and refreshing context has a cost, so reduced per-question discovery is a hypothesis to measure.

## Description

Use `notebooks/02-Optimus.ipynb` and the supplied `elastic/context-automation.md` brief. Configure a native AI Index with your workshop sources, run the native metadata-generation automation, and inspect the resulting KIs. Explain one useful routing clue and one limitation before connecting Optimus.

- Give Optimus access to the registered AI Index and the original source data through the scoped MCP connection.
- Use the supplied context-first system prompt with your AI Index's actual description/schema.
- Compare the same questions, model deployment, source snapshot, and result limits against fresh baseline runs.

Record correctness, citations, discovery/context/source calls, tokens, and latency. Explain the observed tradeoff even if savings are small or negative. Native context retrieval may involve list, describe, and query calls; success does not require exactly one call or a fixed reduction.

## Success Criteria

- Show a native Context Engine AI Index and KIs covering more than one workshop source.
- Demonstrate how a KI helps select an index or construct a source query.
- Verify that Optimus retrieves KI context through MCP and current details from source data when needed.
- Show paired measurements and correctness/citation checks for the same questions.
- Explain why AI Index creation/refresh cost is separate from per-question token use.
- Demonstrate that a KI is reusable context, not a security boundary or automatically current source record.

## Learning Resources

- [Context Engine concepts](https://www.elastic.co/docs/explore-analyze/ai-features/context-engine/concepts)
- [Context Engine quickstart](https://www.elastic.co/docs/explore-analyze/ai-features/context-engine/quickstart)
- [Retrieve context from an AI Index](https://www.elastic.co/docs/explore-analyze/ai-features/context-engine/retrieve-context-from-ai-index)
- [AI Index routing walkthrough](https://www.elastic.co/search-labs/blog/ai-index-building-context-agents)

## Tips

- Inspect the AI Index's actual destination and fields. Do not assume a name prefix alone creates a managed Context Engine resource.
- Both agents need the same source evidence; only Optimus receives reusable context.
- Adding an AI Index to an Elastic agent does not by itself configure a Foundry agent.

## Advanced Challenges

- Change a source's metadata, regenerate its KI, and explain the impact of stale context.
- Answer a question that requires two sources while retaining document references.
- Explore when repeated usage could offset KI generation and refresh costs.
