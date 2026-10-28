# Challenge 00 - Ready, Set, Connect

**[Home](../README.md)** - [Next Challenge >](./Challenge-01.md)

## Introduction

Northstar Support needs a copilot that can find trustworthy answers across several data sources. In this challenge you will prepare the three environments used for the rest of the hack: an Azure lab subscription (Microsoft Foundry), an Elastic Serverless trial (data and MCP tools), and a GitHub Codespace (your developer environment). One deployment script, run from the Codespace terminal, will load the sample data and create the Elastic MCP tools for you.

> **Draft notice:** This workshop has not been tested. Items shown as `<PLACEHOLDER>` will be provided by your event organizer before the event.

## Common Prerequisites

- Access to the Azure lab environment provided for this event.
- A [GitHub account](https://github.com/signup) (use your personal account, not an enterprise managed account).
- An email address to create an [Elastic Cloud trial account](https://cloud.elastic.co/registration).

## Description

### Launch the Azure Lab Environment

The in-person lab proctor will tell you how to launch your Azure lab environment and will provide your lab credentials.

`<PLACEHOLDER: Azure lab launch instructions provided by the lab proctor>`

Gather the following from the lab environment and keep them handy. You will use them in the Codespace terminal:

1. Azure username (Spektra credentials)
2. Azure password
3. Azure subscription ID (if shown by the lab environment)

### Create an Elastic Serverless Trial Environment

1. Go to `<PLACEHOLDER: URL to create an Elastic trial>` and sign up for a free Elastic Cloud trial.
2. When prompted to create a project, choose **Elasticsearch** as the project type and use the default settings.
3. Wait for the project to finish creating, then open it.
4. Gather your **Elasticsearch endpoint URL** and your **Kibana URL**. They are different URLs, and you will need both.

   `<PLACEHOLDER: Screenshot showing where to find the Elasticsearch endpoint and Kibana URL>`

5. Create an **API key** for the deployment script:
   - In the project, go to **Developer Tools / API keys** (or search for "API keys" in the top search bar).
   - Click **Create API key**, give it a name such as `wth-setup`, and keep the default privileges.
   - Copy the **encoded** key value immediately. It is shown only once.

   `<PLACEHOLDER: Screenshot showing where to create and copy the Elastic API key>`

> **Warning:** Treat API keys like passwords. Do not paste them in chat, screenshots, or Git.

### Launch Development Environment

You will use [GitHub Codespaces](https://docs.github.com/en/codespaces/overview) as your development environment. A GitHub Codespace is a development environment hosted in the cloud that you access via a browser. All of the developer tools for this hack, including the Azure CLI and Python/Jupyter, are pre-installed.

GitHub Codespaces is available to every personal GitHub.com account, which includes a monthly free usage quota. You can check your balance on the [GitHub billing page](https://github.com/settings/billing/summary).

1. Open the Codespace for this hack: `<PLACEHOLDER: link to the hack's Codespace>`
2. Sign in with your **personal** GitHub account.
3. Verify the `Dev container configuration` is set to the one for this hack, then click **Create Codespace**.
4. Wait for Visual Studio Code to load in your browser. The first launch takes approximately 3-5 minutes.

**NOTE:** If you close the Codespace, return to [GitHub Codespaces](https://github.com/codespaces) to find and re-launch it.

### Deploy Cloud Resources and Sample Data

In this section, you will deploy the sample data for this hackathon.

From the **Terminal** in your Codespace, complete the following:

1. Log in to Azure with your lab credentials:

   ```bash
   az login
   ```

   The Codespace uses a device code. Open the URL shown, enter the code, and sign in with the Azure username and password from your lab environment. If your organization's policy blocks device-code login, open the Codespace in VS Code Desktop and run `CODESPACES=false az login`.

2. Add your Elastic values to the configuration file used by the setup scripts:

   ```bash
   cp .env.sample .env
   code .env
   ```

   Fill in your Elasticsearch endpoint URL, Kibana URL, and Elastic API key. Leave the other values as provided.

3. Run the deployment script. It sets up the Elastic sample data and creates the Elastic MCP tools backed by ES|QL queries:

   ```bash
   chmod +x infra/deploy.sh
   ./infra/deploy.sh
   ```

   Wait for the script to report success. If it fails, read the message, correct your `.env` file, and run it again.

### Verify Your Elastic Environment in Kibana

1. Open your **Kibana URL** in a browser and sign in.
2. Confirm the sample indices exist:
   - Open **Index Management** (search for "Index Management" in the top search bar) and select the **Indices** tab.
   - Find the four workshop indices whose names begin with `cq-`. Click each one and open the **Documents** tab (or use **Discover**) to confirm it contains records.

   `<PLACEHOLDER: Screenshot of the workshop indices in Index Management>`

3. Confirm the MCP tools exist:
   - Open **Agent Builder** from the navigation menu (or search for "Agent Builder") and go to **Tools**.
   - Find the ES|QL tools created by the script. Open one to review its description and query.

   `<PLACEHOLDER: Screenshot of the Tools list in Agent Builder>`

## Success Criteria

- Verify that you can sign in to the Azure lab environment and that `az account show` in the Codespace shows the lab subscription.
- Verify that your Elastic trial project exists and that you have your Elasticsearch URL, Kibana URL, and API key.
- Verify that your Codespace is running and that your `.env` file contains your Elastic values.
- Verify that `./infra/deploy.sh` completed without errors.
- Demonstrate in Kibana that the four workshop sample indices exist and contain documents.
- Demonstrate in Kibana that the ES|QL MCP tools exist in Agent Builder.

## Learning Resources

- [GitHub Codespaces Overview](https://docs.github.com/en/codespaces/overview)
- [Elastic Cloud Serverless](https://www.elastic.co/docs/deploy-manage/deploy/elastic-cloud/serverless)
- [Elastic Agent Builder tools](https://www.elastic.co/docs/explore-analyze/ai-features/agent-builder/tools)
- [Elastic API keys](https://www.elastic.co/docs/deploy-manage/api-keys/elasticsearch-api-keys)
- [Sign in with Azure CLI](https://learn.microsoft.com/en-us/cli/azure/authenticate-azure-cli)

## Tips

- Your Elasticsearch URL and Kibana URL are different. Use the Kibana URL to browse the web interface.
- The Elastic API key is shown only once. If you lose it, create a new one.
