# Challenge 00 - Prerequisites - Ready, Set, GO!

**[Home](../README.md)** - [Next Challenge >](./Challenge-01.md)

## Introduction

You have been contracted to deploy, monitor and manage an online shopping website in Azure for a start-up company called "eShopOnWeb".  After evaluating the requirements, you develop a solution in Azure that includes an Azure environment that consists of (2) Azure resource groups that include a VNet, subnets, NSG(s), LB(s), NAT rules, scale set and a fully functional .NET Core Application (eShopOnWeb) to monitor.

Upon successful testing, you present your solution to company's leadership for approval along with the PowerShell, CLI and/or Azure Cloud Shell options for quick deployment. 

They were very excited about how quickly you are able to deploy the solution, and give you the green light to proceed.

## Prerequisites

You will need an Azure Subscription with sufficient RBAC roles assigned to complete the challenges at the subscription scope.

You can complete this entire hack in a web browser using the [Azure Portal](https://portal.azure.com), [Datadog Portal](https://datadog.com), and [Azure Cloud Shell](https://shell.azure.com).

However, if you work with Azure and on a regular basis, these are tools you should consider having installed on your local workstation:

- [Azure Subscription](../../000-HowToHack/WTH-Common-Prerequisites.md#azure-subscription)
- [Windows Subsystem for Linux](../../000-HowToHack/WTH-Common-Prerequisites.md#windows-subsystem-for-linux)
- [Managing Cloud Resources](../../000-HowToHack/WTH-Common-Prerequisites.md#managing-cloud-resources)
  - [Azure CLI](../../000-HowToHack/WTH-Common-Prerequisites.md#azure-cli)
    - [Note for Windows Users](../../000-HowToHack/WTH-Common-Prerequisites.md#note-for-windows-users)
    - [Azure PowerShell CmdLets](../../000-HowToHack/WTH-Common-Prerequisites.md#azure-powershell-cmdlets)
- [Visual Studio Code](../../000-HowToHack/WTH-Common-Prerequisites.md#visual-studio-code)
  - [VS Code plugin for ARM Templates](../../000-HowToHack/WTH-Common-Prerequisites.md#visual-studio-code-plugins-for-arm-templates)
  - [VS Code plugin for Bicep](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-bicep)

### Student Resources

Your coach will provide you with a `Resources.zip` file that contains resource files you will use to complete some of the challenges for this hack.  

If you have installed all of the tools listed above on your local workstation, you should unpack the `Resources.zip` file there too.

If you plan to use the Azure Cloud Shell, you should upload the `Resources.zip` file to your cloud shell first and then unpack it there.

## Description

For this challenge, you will deploy the eShopOnWeb application and its underlying infrastructure resources to Azure using a set of pre-developed Bicep templates. Once the application and its infrastructure are deployed, you will complete the hack's challenges using Datadog to monitor it.

### Deploy Resources

You will find the provided `main.bicep` template and its associated script files in the `/Challenge-00/` folder of the `Resources.zip` file provided to you by your coach. 

Navigate to this location in your Azure Cloud Shell or Windows Terminal. You may use either the [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/?msclkid=6b97242fb99411ec83659823c955fa16) or the [PowerShell Az module](https://docs.microsoft.com/en-us/powershell/azure/install-az-ps) to deploy the Bicep template.

#### Use Azure CLI

1. Log into your Azure Subscription with the Azure CLI: 
    ```bash
    az login
    ```
    **NOTE:** If you are using the Azure Cloud Shell, you can skip this step as the Azure CLI is already logged into your Azure subscription.

1. Deploy the template by running the following Azure CLI command from wherever you have unpacked the `/Challenge-00/` folder:

    ```bash
    az deployment sub create --name "<deploymentName>" --location "<azure-region>" -f main.bicep --verbose
    ```
    
    - We recommend you use your initials for the  `<deploymentName>` value.
    - The `<azure-region>` value must be one of the pre-defined Azure Region names. You can view the list of available region names by running the following command: `az account list-locations -o table`
    - You will be prompted to enter values for the local admin Username and Password for the Azure virtual machines and scale set instances.  Enter a username and password that adheres to [Azure VM Username Requirements](https://docs.microsoft.com/en-us/azure/virtual-machines/windows/faq#what-are-the-username-requirements-when-creating-a-vm-) and [Azure VM Password Requirements](https://docs.microsoft.com/en-us/azure/virtual-machines/windows/faq#what-are-the-password-requirements-when-creating-a-vm-)

#### Use PowerShell with the AZ Module

1. Log into your Azure Subscription with the PowerShell:

    ```PowerShell
    Connect-AzAccount -Tenant '<Tenant ID>' -Environment 'AzureCloud' -Subscription '<Subscription ID>'
    ```

    **NOTE:** If you are using the Azure Cloud Shell, you can skip this step as PowerShell is already logged into your Azure subscription.

1. Deploy the template by running the following PowerShell command from wherever you have unpacked the `/Challenge-00/` folder:

    ```PowerShell
    New-AzDeployment -Name "<deploymentName>" -Location "<azure-region>" -TemplateUri "main.bicep" -Verbose
    ```
    - We recommend you use your initials for the  `<deploymentName>` value.
    - The `<azure-region>` value must be one of the pre-defined Azure Region names. You can view the list of available region names by running the following command: `az account list-locations -o table`
    - You will be prompted to enter values for the local admin Username and Password for the Azure virtual machines and scale set instances.  Enter a username and password that adheres to [Azure VM Username Requirements](https://docs.microsoft.com/en-us/azure/virtual-machines/windows/faq#what-are-the-username-requirements-when-creating-a-vm-) and [Azure VM Password Requirements](https://docs.microsoft.com/en-us/azure/virtual-machines/windows/faq#what-are-the-password-requirements-when-creating-a-vm-)

### View Deployed Resources

- Once the deployment has completed, navigate to the Public IP Address resource, **pip-wth-monitor-web-d-eu** , in the Azure Portal.  
- In the Overview blade, copy the DNS name to your clipboard.  
- Open a web browser, paste your DNS name in the address bar and press ENTER.  Your browser should render the eShopOnWeb site. 

![Webpage of the eShopOnWeb site](../Images/00-23-Eshoponweb-Webpage.png)

## Success Criteria

- Verify you can see the website deployed
- Verify the resources contained in architecture diagram below are present in your own Azure subscription.

![Hack Diagram](../Images/monitoringhackdiagram1.png)

## Learning Resources

- [Get Started with Azure PowerShell](https://docs.microsoft.com/en-us/powershell/azure/get-started-azureps?view=azps-6.4.0)
- [Get Started with Azure Command-Line Interface (CLI)](https://docs.microsoft.com/en-us/cli/azure/get-started-with-azure-cli)
- [Overview of Azure Cloud Shell](https://docs.microsoft.com/en-us/azure/cloud-shell/overview)

## Tips

- Make sure the Admin password adheres to the Azure password policy
- Make sure you are logged into the correct subscription and you have the at least contributors role access.  
- Make sure you have the compute capacity in the region you are deploying to and request an increase to the limit if needed.