# Challenge 00 - Ready, Set, Connect

**[Home](../README.md)** - [Next Challenge >](./Challenge-01.md)

## Introduction

Northstar Support needs a copilot that can find trustworthy answers across several data sources. Your browser-hosted Codespace will run the notebooks, Microsoft Foundry will run your agents, and Elastic will host the data and MCP tools.

> **Draft notice:** This workshop has not been tested. Ask your event organizer for the confirmed service/region/model configuration before provisioning resources.

## Common Prerequisites

- An enabled [Azure subscription](../../000-HowToHack/WTH-Common-Prerequisites.md#azure-subscription).
- A [GitHub Codespaces account and available usage](https://docs.github.com/en/codespaces/overview).
- An [Elastic Cloud account](https://cloud.elastic.co/registration).

## Description

### Before the event

1. Sign in to Azure, or investigate the [Azure free-account offer](https://azure.microsoft.com/free/). Confirm an enabled subscription, model quota, and permissions with your administrator. Trial credits do not guarantee access to every model.
2. Create or identify an Elastic **Elasticsearch Serverless** project. The organizer must confirm that your account can enable native Context Engine in the intended Kibana space, create AI Indices, run KI-generation automations, and use the required inference services. A generic Serverless trial is not proof of access.
3. Confirm your Azure region supports the selected model, remote MCP, and [Foundry risk and safety evaluation](https://learn.microsoft.com/en-us/azure/foundry/concepts/evaluation-regions-limits-virtual-network). Do not assume an existing project's region supports all three.
4. Confirm Azure permissions: resource creation if deploying; Foundry agent/evaluation access for notebook work; and connection-management permission for storing Elastic MCP credentials. An administrator must grant any missing roles.

### In your workspace

1. Open the student-only Codespaces workspace supplied by your coach, or unpack Resources.zip in an equivalent Python/Jupyter environment. Do not expose a public Codespaces port: Foundry connects directly to Elastic's hosted MCP endpoint.
2. Open `notebooks/00-Setup.ipynb` and select the provided Python kernel. Packages and Azure CLI are supplied by the devcontainer.
3. Copy `.env.sample` to `.env`, choose a unique `WORKSHOP_ID`, and enter local configuration. Keep secrets out of chat, screenshots, notebook cells, and Git. The notebook reads configuration without printing credentials.
4. Sign in with Azure CLI. Choose **attach existing** to reuse an approved Foundry project/model, or explicitly opt in to the provided **create new** deployment script. Do not deploy into a shared resource group.
5. Supply the Elastic endpoints and setup API key. Run the provided data loader to populate four workshop indices. It uses stable document IDs and refuses indices without this workshop's ownership metadata.
6. Configure separate read-only Foundry MCP connections for the baseline and Optimus using the supplied connection guidance. The baseline key must not read AI Index backing data. Inspect the advertised MCP tool names rather than guessing them.
7. Record the readiness evidence in the setup notebook. Unavailable native Context Engine or evaluation access is a blocker to that learning objective, not a reason to substitute simulated success.

## Success Criteria

- Verify that your notebook kernel imports the supplied libraries and Azure CLI targets the intended enabled subscription.
- Verify that four workshop source indices contain the bundled records.
- Show that native Context Engine is enabled in the intended Kibana space and that workflow/inference access is available.
- Verify that Foundry can use your deployed model and discover Elastic MCP tools using a scoped connection.
- Show which checks are complete and which remain unverified, including evaluation access.
- Demonstrate where credentials are stored and which resources you will clean up.

## Learning Resources

- [Elastic Context Engine quickstart](https://www.elastic.co/docs/explore-analyze/ai-features/context-engine/quickstart)
- [Elastic MCP endpoint and authentication](https://www.elastic.co/docs/explore-analyze/ai-features/agent-builder/mcp-server)
- [Connect Foundry agents to MCP endpoints](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/model-context-protocol)
- [Foundry evaluation region support](https://learn.microsoft.com/en-us/azure/foundry/concepts/evaluation-regions-limits-virtual-network)

## Tips

- Your Elasticsearch URL and Kibana URL are different. Include the intended space in Kibana API requests.
- Resource deployment permissions are different from model and agent data-plane permissions.
- Use a dedicated workshop project where possible. A setup credential should never become an agent's runtime credential.
