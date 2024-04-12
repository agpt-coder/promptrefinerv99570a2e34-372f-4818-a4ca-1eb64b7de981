import os

import openai
from pydantic import BaseModel


class RefinePromptResponse(BaseModel):
    """
    Provides the refined version of the LLM prompt.
    """

    refined_prompt: str
    processing_status: str


openai.api_key = os.getenv("OPENAI_API_KEY")


def refine_prompt(user_prompt: str) -> RefinePromptResponse:
    """
    Endpoint to accept a string LLM prompt and return a refined version.

    This function sends the user's LLM prompt to GPT-4 via the OpenAI API for refinement, by including
    a system message that instructs GPT-4 to refine the given prompt using advanced prompt engineering techniques.
    The refined prompt is then returned within a RefinePromptResponse object.

    Args:
        user_prompt (str): Original LLM prompt submitted by the user for refinement.

    Returns:
        RefinePromptResponse: Provides the refined version of the LLM prompt and the processing status.
    """
    if not openai.api_key:
        return RefinePromptResponse(
            refined_prompt="OpenAI API key is not set.", processing_status="Failed"
        )
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are a prompt refiner. Use advanced prompt engineering techniques to refine the user's prompt.",
                },
                {"role": "user", "content": user_prompt},
            ],
        )  # TODO(autogpt): "ChatCompletion" is not a known member of module "openai". reportAttributeAccessIssue
        #   Found doccumentation for the module:
        #    To fix the error """"ChatCompletion" is not a known member of module "openai". reportAttributeAccessIssue"", you need to use the correct method for creating chat completion tasks in OpenAI's Python library as shown in the usage example extract:
        #
        #   ```python
        #   from openai import OpenAI
        #
        #   client = OpenAI(
        #       # This is the default and can be omitted
        #       api_key=os.environ.get("OPENAI_API_KEY"),
        #   )
        #
        #   chat_completion = client.chat.completions.create(
        #       messages=[
        #           {
        #               "role": "user",
        #               "content": "Say this is a test",
        #           }
        #       ],
        #       model="gpt-3.5-turbo",
        #   )
        #   ```
        #
        #   Ensure that you have correctly imported the `OpenAI` class from the `openai` module and are using the `chat.completions.create` method to create chat completions.
        if response.choices and len(response.choices) > 0:
            refined_prompt = response.choices[0].message["content"].strip()
            processing_status = "Completed"
        else:
            refined_prompt = "Failed to refine prompt."
            processing_status = "Failed"
        return RefinePromptResponse(
            refined_prompt=refined_prompt, processing_status=processing_status
        )
    except Exception as e:
        return RefinePromptResponse(
            refined_prompt=f"Error calling OpenAI API: {str(e)}",
            processing_status="Error",
        )
