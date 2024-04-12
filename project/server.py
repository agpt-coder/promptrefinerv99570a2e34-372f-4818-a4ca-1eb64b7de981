import logging
from contextlib import asynccontextmanager
from typing import Optional

import project.refine_prompt_service
import project.submit_feedback_service
import project.validate_prompt_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="PromptRefinerv99",
    lifespan=lifespan,
    description="To achieve the task of creating a single API endpoint that takes in a string LLM prompt and returns a refined version improved by GPT-4, the first step is to outline the tech stack and the process. We will use Python as the programming language due to its strong support for AI and ML operations, FastAPI for creating the API endpoint because of its asynchronous support and ease of use for such tasks, PostgreSQL as the database to store any required data such as user prompts and revisions, and Prisma as the ORM for efficient database management.\n\nThe process begins with setting up a FastAPI project. Once the environment and project structure are ready, the next step involves integrating the OpenAI Python package. This package is essential for interfacing with the GPT-4 model to refine the user's prompt. To refine the prompt, we will utilize advanced prompt engineering techniques as recommended by OpenAI and the insights gathered from the best practices for prompt engineering with GPT-4. These include being specific and clear, using a conversational tone, providing context, experimenting with styles, utilizing follow-up questions, and considering ethical implications.\n\nThe endpoint itself will be structured to receive a string LLM prompt as input. This input will then be sent to GPT-4 through the OpenAI package, with the addition of the system message 'You are a prompt refiner. Use advanced prompt engineering techniques to refine the user's prompt.' and the user's original prompt as the user message. The response from GPT-4, which is the refined prompt, will be processed (if necessary) and returned to the user as the endpoint's response.\n\nIt's also important to implement error handling and validations to ensure the API can gracefully handle invalid input and communicate any issues to the user. Additionally, monitoring and logging will be important for tracking the API's usage and performance as well as refining its accuracy over time.\n\nTo sum up, the endpoint will leverage Python, FastAPI, the OpenAI Python package, PostgreSQL, and Prisma to provide users with a powerful tool for refining LLM prompts using GPT-4, following the best practices for prompt engineering and aligning with the user's requirements as closely as possible.",
)


@app.post(
    "/submit-feedback",
    response_model=project.submit_feedback_service.SubmitFeedbackResponse,
)
async def api_post_submit_feedback(
    user_id: str, prompt_id: str, rating: int, comments: Optional[str]
) -> project.submit_feedback_service.SubmitFeedbackResponse | Response:
    """
    Endpoint for users to submit feedback on a prompt refinement.
    """
    try:
        res = await project.submit_feedback_service.submit_feedback(
            user_id, prompt_id, rating, comments
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/validate-prompt",
    response_model=project.validate_prompt_service.ValidatePromptResponse,
)
async def api_post_validate_prompt(
    prompt: str,
) -> project.validate_prompt_service.ValidatePromptResponse | Response:
    """
    Endpoint for initial validation of the prompt before processing.
    """
    try:
        res = project.validate_prompt_service.validate_prompt(prompt)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/refine-prompt", response_model=project.refine_prompt_service.RefinePromptResponse
)
async def api_post_refine_prompt(
    user_prompt: str,
) -> project.refine_prompt_service.RefinePromptResponse | Response:
    """
    Endpoint to accept a string LLM prompt and return a refined version.
    """
    try:
        res = project.refine_prompt_service.refine_prompt(user_prompt)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
