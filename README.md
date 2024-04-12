---
date: 2024-04-12T18:34:31.674903
author: AutoGPT <info@agpt.co>
---

# PromptRefinerv99

To achieve the task of creating a single API endpoint that takes in a string LLM prompt and returns a refined version improved by GPT-4, the first step is to outline the tech stack and the process. We will use Python as the programming language due to its strong support for AI and ML operations, FastAPI for creating the API endpoint because of its asynchronous support and ease of use for such tasks, PostgreSQL as the database to store any required data such as user prompts and revisions, and Prisma as the ORM for efficient database management.

The process begins with setting up a FastAPI project. Once the environment and project structure are ready, the next step involves integrating the OpenAI Python package. This package is essential for interfacing with the GPT-4 model to refine the user's prompt. To refine the prompt, we will utilize advanced prompt engineering techniques as recommended by OpenAI and the insights gathered from the best practices for prompt engineering with GPT-4. These include being specific and clear, using a conversational tone, providing context, experimenting with styles, utilizing follow-up questions, and considering ethical implications.

The endpoint itself will be structured to receive a string LLM prompt as input. This input will then be sent to GPT-4 through the OpenAI package, with the addition of the system message 'You are a prompt refiner. Use advanced prompt engineering techniques to refine the user's prompt.' and the user's original prompt as the user message. The response from GPT-4, which is the refined prompt, will be processed (if necessary) and returned to the user as the endpoint's response.

It's also important to implement error handling and validations to ensure the API can gracefully handle invalid input and communicate any issues to the user. Additionally, monitoring and logging will be important for tracking the API's usage and performance as well as refining its accuracy over time.

To sum up, the endpoint will leverage Python, FastAPI, the OpenAI Python package, PostgreSQL, and Prisma to provide users with a powerful tool for refining LLM prompts using GPT-4, following the best practices for prompt engineering and aligning with the user's requirements as closely as possible.

## What you'll need to run this
* An unzipper (usually shipped with your OS)
* A text editor
* A terminal
* Docker
  > Docker is only needed to run a Postgres database. If you want to connect to your own
  > Postgres instance, you may not have to follow the steps below to the letter.


## How to run 'PromptRefinerv99'

1. Unpack the ZIP file containing this package

2. Adjust the values in `.env` as you see fit.

3. Open a terminal in the folder containing this README and run the following commands:

    1. `poetry install` - install dependencies for the app

    2. `docker-compose up -d` - start the postgres database

    3. `prisma generate` - generate the database client for the app

    4. `prisma db push` - set up the database schema, creating the necessary tables etc.

4. Run `uvicorn project.server:app --reload` to start the app

## How to deploy on your own GCP account
1. Set up a GCP account
2. Create secrets: GCP_EMAIL (service account email), GCP_CREDENTIALS (service account key), GCP_PROJECT, GCP_APPLICATION (app name)
3. Ensure service account has following permissions: 
    Cloud Build Editor
    Cloud Build Service Account
    Cloud Run Developer
    Service Account User
    Service Usage Consumer
    Storage Object Viewer
4. Remove on: workflow, uncomment on: push (lines 2-6)
5. Push to master branch to trigger workflow
