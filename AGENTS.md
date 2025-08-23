# Agent Instructions

This document outlines the standard operating procedures for an AI agent interacting with this repository. The agent's primary role is to assist users in either running existing workflows or in developing new ones.

---

## Guiding Principles

-   **Clarity:** Always provide clear and concise instructions.
-   **Safety:** Prioritize user safety by explaining commands before execution.
-   **Proactiveness:** Anticipate user needs and offer assistance accordingly.

---

## Scenarios

There are two primary scenarios the agent should be prepared to handle:

1.  **Running a Workflow**
2.  **Implementing or Enhancing a Workflow**

### 1. Running a Workflow

When a user wants to run an existing workflow, the agent must perform the following steps:

#### a. Prerequisite Verification

Before attempting to execute any part of a workflow, the agent must verify the user's environment:

1.  **Check for Virtual Environment:**
    -   Verify the existence of a `.venv` directory in the project root.
    -   If it doesn't exist, guide the user to create one:
        ```bash
        python3 -m venv .venv
        source .venv/bin/activate
        ```

2.  **Check for Installed Libraries:**
    -   Verify that the packages listed in `requirements.txt` are installed within the virtual environment.
    -   If not, instruct the user to install them:
        ```bash
        pip install -r requirements.txt
        ```

3.  **Check for `ffmpeg` (if required):**
    -   If the workflow involves video processing, check if `ffmpeg` is installed and accessible in the system's PATH.
    -   If not, provide instructions for installing it based on the user's operating system (refer to the `README.md` for installation guides).

#### b. Workflow Execution

Once the prerequisites are met, the agent can proceed with running the workflow:

-   **Follow the Workflow:** Adhere strictly to the steps outlined in the corresponding `.workflow.md` file located in the `workflows/` directory.
-   **Execute Specific Steps:** If the user requests to run only a specific step from the workflow, the agent should execute that step in isolation, ensuring all inputs for that step are available.

### 2. Implementing or Enhancing a Workflow

When a user wants to create a new workflow or improve an existing one, the agent should assist in the development process.

#### a. Workflow Definition (`workflows/*.workflow.md`)

-   **Step-by-Step Instructions:** Guide the user in creating or modifying a `.workflow.md` file within the `workflows/` directory. The instructions should be clear, sequential, and written in a way that an AI agent can easily parse and execute them.
-   **Inputs and Outputs:** Ensure that each step clearly defines its expected inputs and outputs.

#### b. Scripting (`scripts/*.py`)

-   **Python Scripts:** Assist the user in writing Python scripts in the `scripts/` directory that will serve as the tools for the workflow.
-   **Virtual Environment:** All code should be written with the assumption that it will be executed within the project's virtual environment.
-   **Dependency Management:** Use `pip` and `requirements.txt` to manage all Python dependencies.
-   **Best Practices:** Encourage the use of modular functions, clear variable names, and error handling.