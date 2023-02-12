# Challenge 01 - Monitor Virtual Machine performance with Azure Monitor Metrics

[< Previous Challenge](./Challenge-00.md) - **[Home](../README.md)** - [Next Challenge >](./Challenge-02.md)

## Introduction

After deploying your initial solution for eShopOnWeb, you want to make sure that the telemetry is collected from the VMs deployed and display the results on a dashboard for visualization and alerting purposes. By default Azure Monitoring collects only host-level metrics - like CPU utilization, disk and network usage - for all virtual machines without any additional software. For more insight into your virtual machines, you can collect guest-level metrics, logs and other diagnostic data using the Azure Diagnostics agent (extension).

To accomplish this task, you will have to understand the concept of performance counters (metrics), how to collect them into Azure Monitor Metrics store, how to configure Metric alerts, and display results in an Azure Dashboard.  

Once you have configured the dashboard, alerts, and counters to be collected, you will use two tools to simulate a load on the eShopOnWeb resources:
- HammerDB - A benchmarking and load testing tool for the world's most popular databases, including SQL Server.
- A custom script that produces CPU load on the eShopOnWeb website.

## Description

In the eShopOnWeb Azure environment, there are three compute resources to be aware of:
- **`vmss-wth-monitor-d-XX`** - Virtual Machine Scale Set (VMSS) hosting the eShopOnWeb web site
- **`vmwthdbdXX`** - Virtual Machine running SQL Server 2019 hosting the eShopOnWeb database
- **`vmwthvsdXX`** - Virtual Machine running Windows Server 2022 + Visual Studio 2022 + SQL Management Studio to act as a "jumpbox" that you will login to for administrative tasks.

>**Note** The "XX" in each resource name will vary based on the Azure region the eShopOnWeb Azure environment has been deployed to.

Azure Bastion has been configured to enable you to securely login to any of these VMs with a Remote Desktop session through a web browser. 

To login to a VM via Azure Bastion, navigate to the blade for any of these VMs in the Azure portal, click the "Connect" button, and select "Bastion". Use the username and password provided in Challenge 0.
 
### Set up Counters, Alerts, and Dashboard

In this challenge you need to complete the following management tasks:
>**Note** Use Azure portal, Bicep templates, Azure CLI or PowerShell to achieve your goals. While Azure portal is useful for learning purposes, deployment templates and scripts are crucial for most real-life scenarios.

- Create an empty database called “tpcc” on the SQL Server VM. Use SQL Auth with the username being "sqladmin" and password being whatever you used during deployment in Challenge 0.

	**HINT:** You can use SQL Management Studio on either the SQL Server VM or the Visual Studio VM, or SQL Server Object Explorer view in Visual Studio to create the database.

- Navigate to the blade of the SQL Server VM, click "Metrics" to open Azure Monitor Metrics explorer, and check what metrics are currently being collected.
- Enable guest-level monitoring for the SQL Server and send the below guest OS metrics to Azure Monitor:
	- Object: Memory
		- Counter: Available Bytes
		- Counter: Committed Bytes
	- Object: SQLServer:Databases
		- Counter: Active Transactions
		- Instance: tpcc
- From Azure Monitor create an Action group to send emails to your address.
- Create an Alert rule to be notified via email if "Active Transactions" metric goes over 40 on the SQL Server "tpcc" database.
- Create an Alert Rule to be notified via email if average CPU Utilisation goes over 75% on the Virtual Machine Scale Set.
- Suppress both alerts over the weekend.
- Create graphs for the SQL Server Active Transactions and the Virtual Machine Scale Set CPU Utilisation and pin both of them to your Azure Dashboard.

### Simulate Load on the eShopOnWeb Environment

Now that Azure Monitor is configured to monitor the eShopOnWeb resources, it is time to simulate load on the SQL Server database and the eShopOnWeb website:
- Use HammerDB to create a transaction load on the "tpcc" database on the SQL Server
    - Download and Install HammerDB tool on the Visual Studio VM 
    - See sample [Instructions for using HammerDB](./Resources/Challenge-01/UsingHammerDB.md) to generate load on the "tpcc" database.
- Simulate a CPU load on the VM Scale Set using the [cpuGenLoadwithPS.ps1](./Resources/Challenge-01/cpuGenLoadwithPS.ps1) script located in the `/Challenge-01` folder of the student resource package.
    - This script is designed to be run directly on the VM instances in the VMSS.
    - **HINT:** You will need to upload this script to the VMs in order to run it on each instance.

## Success Criteria

To complete this challenge successfully, you should be able to:

- Verify that you can collect the DB and CPU counters after load simulation and display them on a Dashboard.
- Verify the dashboard has the metric with a spike representing before and after the simulation.
- Show two fired alerts in the Portal and the email notifications received.

![enter image description here](https://github.com/msghaleb/AzureMonitorHackathon/raw/master/images/ch1_metric_spike.jpg)

## Learning Resources

- [Azure Monitor Agents Overview](https://learn.microsoft.com/en-us/azure/azure-monitor/agents/agents-overview)
- [Install and configure the Azure Diagnostics extension for Windows (WAD)](https://learn.microsoft.com/en-us/azure/azure-monitor/agents/diagnostics-extension-windows-install)
- [Azure Monitor Metrics](https://learn.microsoft.com/en-us/azure/azure-monitor/essentials/data-platform-metrics)
- [Azure Metric alerts](https://learn.microsoft.com/en-us/azure/azure-monitor/alerts/alerts-types#metric-alerts)
- [HammerDB](https://www.hammerdb.com)
- [Finding the counter](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.diagnostics/get-counter?view=powershell-5.1) 