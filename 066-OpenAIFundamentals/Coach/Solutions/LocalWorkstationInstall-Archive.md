# ARCHIVED 066-AI Fundamentals - Local Setup Instructions

##### Setup GitHub Copilot

For parts of this hack we will be relying heavily on GitHub Copilot for coding. Please setup [VS Code with GitHub Copilot](https://code.visualstudio.com/docs/copilot/setup-simplified?wt.md_id=AZ-MVP-5004796)


To work on your local workstation directly (not with dev containers), please ensure you have the following tools and resources before hacking:

- [Student Resources](#student-resources)
- [Visual Studio Code](#visual-studio-code)
- [Python](#python)
- [Conda Runtime](#conda)
- [Azure CLI (Optional)](#azure-cli-optional)

##### Student Resources

The Jupyter notebooks, starter code, and sample data sources for this hack are available in a Student Resources package.

- [Download and unpack the `Resources.zip`](https://aka.ms/wth/openaifundamentals/resources) package to your local workstation. 

The rest of the challenges will refer to the relative paths inside the `Resources.zip` file where you can find the various resources to complete the challenges.

##### Visual Studio Code

Visual Studio Code is a code editor which you will work with Jupyter notebooks.

- [Install VS Code](https://getvisualstudiocode.com)

##### Setup GitHub Copilot

For parts of this hack we will be relying heavily on GitHub Copilot for coding. Please setup [VS Code with GitHub Copilot](https://code.visualstudio.com/docs/copilot/setup-simplified?wt.md_id=AZ-MVP-5004796)

##### Python

- [Python Installation](https://www.python.org/downloads), version at least \>= 3.6, the minimum requirement for using OpenAI's GPT-3.5-based models, such as ChatGPT.

##### Conda

- Conda Installation, for project environment management and package management, version \>= conda 4.1.6. Anaconda distribution is a popular Python distribution, while Miniconda is the lightweight version of Anaconda.
  - [Anaconda](https://docs.anaconda.com/anaconda/install) OR [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
- Environment setup:
  - Open Anaconda Prompt or your favourite terminal and verify Python and Conda installations using `python --version` and `conda --version`
  - Create a project environment using Conda - `conda create --name <env_name>`
  - Activate Conda environment - `conda activate <env_name>`
  - Install required libraries and packages, provided in the form of a `requirements.txt` file in the root folder of the `Resources.zip` file. We recommend using pip or Conda in a virtual environment to do so. For example, you can run `pip install -r requirements.txt`
  - Open the project in VS Code using `code .`
  - If you are using Visual Studio Code, make sure you change your Python interpreter (CTRL+SHIFT+P) to select the project/virtual environment that you just created.

For more information, see [Jupyter Notebooks in VS Code](https://code.visualstudio.com/docs/datascience/jupyter-notebooks)

##### Azure CLI (Optional)

While it is not necessary for this hack, you may wish to use the Azure CLI to interact with Azure in addition to the Azure Portal.

- [Install Azure CLI](https://aka.ms/installazurecli)

#### Cloud Environment

There is a *THIRD* way of setting up a Jupyter Notebook environment if you don't want to set it up on your local workstation or use GitHub Codespaces. You can set one up in the cloud with Azure Machine Learning Studio and take advantage of Azure Compute power. 

For more information, see: [Run Jupyter Notebooks in your Workspace](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-run-jupyter-notebooks?view=azureml-api-2)

Once you have an Azure Machine Learning Studio Workspace set up, you can upload the contents of the `/notebooks` folder in your `Resources.zip` file to it. For more information on this, see: [How to create and manage files in your workspace](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-manage-files?view=azureml-api-2)
