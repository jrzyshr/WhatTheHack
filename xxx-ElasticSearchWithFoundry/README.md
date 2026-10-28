# What The Hack - Context Quest: From Mole to Optimus

> **Authoring draft - not delivery-ready.** Service access, SDK compatibility, deployment, notebooks, and performance have not been tested. Native Context Engine trial eligibility and the Foundry indirect-attack evaluation mapping must be confirmed before an event.

## Introduction

Your fictional company, Precision Labs, keeps CRM accounts, support tickets, and knowledge base (KB) articles in Elasticsearch. Precision's Support Copilot is built and hosted in Microsoft Foundry.

We're going to learn how to connect a Foundry agent to an Elasticsearch datastore using the Model Context Protocol (MCP). And then we're going to learn how you can use Elastic Context Engine to optimize your agent's performance and token usage.

Meet **Agent Mole**, measure its discovery work, and help **Agent Optimus** use Knowledge Indicators (KIs) from a single AI Index to navigate multiple sources. Then introduce a harmless instruction hidden in a retrieved document: can your agent use the facts without following the document's commands? Use Microsoft Foundry evaluation to investigate. Your goal is a grounded, explainable support answer, not just a smaller token count.

## Learning Objectives

- Connect a Microsoft Foundry agent to Elasticsearch through Elastic MCP with scoped, read-only access.
- Explain how native Context Engine automations turn source data into reusable KIs in an AI Index.
- Use one AI Index to describe multiple source indices while preserving access to current source records.
- Compare discovery calls, service-reported tokens, answer correctness, and latency without assuming guaranteed savings.
- Evaluate an agent response to an indirect prompt injection and distinguish evaluation from runtime filtering.

## Challenges

- Challenge 00: **[Ready, Set, Connect](Student/Challenge-00.md)** - Prepare your own environments and launch the supplied notebook workspace.
- Challenge 01: **[Connect Foundry Agent to Elastic](Student/Challenge-01.md)** - Build a Foundry agent with Elastic MCP and collect a discovery baseline.
- Challenge 02: **[Build the Context Engine](Student/Challenge-02.md)** - Create an AI Index and Knowledge Indicators, and retrieve the Context Engine MCP endpoint.
- Challenge 03: **[Rise of Agent Optimus](Student/Challenge-03.md)** - Build a Foundry agent on the Context Engine and compare it with Agent Mole.
- Challenge 04: **[Trust the Evidence, Not Its Instructions](Student/Challenge-04.md)** - Evaluate prompt-injection resistance using retrieved Elastic data.

## Prerequisites

- Basic Python, Jupyter notebook, JSON, and search concepts; no deep Elasticsearch experience is assumed.
- A GitHub account with access to GitHub Codespaces and a modern browser.
- Your own enabled Azure subscription, suitable model quota, and permission to create or use a Microsoft Foundry project.
- Your own Elastic Cloud Serverless project with native Context Engine, workflow, and inference access.
- Account signup, access verification, and quota checks completed before the event. Challenge 00 contains the preparation details.

Free trials may help with setup, but credits, quotas, supported regions, and experimental-feature eligibility are not guaranteed. Azure, Elastic inference, and Codespaces may incur charges. Use synthetic workshop data, not company or customer information.

## Repository Contents

Student resources include starter notebooks, bundled synthetic data, deployment assets, and a Codespaces configuration. The coach provides a student-only resource workspace or Resources.zip. Core challenges are cumulative; advanced tasks are optional.

## Contributors

- [Peter Laudati](https://github.com/jrzyshr) 
- GitHub Copilot (drafting assistance)
