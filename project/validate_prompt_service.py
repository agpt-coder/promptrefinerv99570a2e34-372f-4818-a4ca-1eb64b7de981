from typing import List, Optional

from pydantic import BaseModel


class ValidatePromptResponse(BaseModel):
    """
    Response model for the outcome of the prompt validation process. Contains fields to indicate whether the prompt is valid, and any error messages or suggestions if invalid.
    """

    isValid: bool
    errorMessage: Optional[str] = None
    suggestions: Optional[List[str]] = None


def validate_prompt(prompt: str) -> ValidatePromptResponse:
    """
    Endpoint for initial validation of the prompt before processing.

    Validates the user's input prompt to ensure it is a non-empty string. If the validation fails, it provides an error message and possible suggestions for correction.

    Args:
        prompt (str): The user's input prompt to be validated. Must be a non-empty string.

    Returns:
        ValidatePromptResponse: Response model for the outcome of the prompt validation process. Contains fields to indicate whether the prompt is valid, and any error messages or suggestions if invalid.
    """
    if not prompt:
        return ValidatePromptResponse(
            isValid=False,
            errorMessage="Prompt cannot be empty.",
            suggestions=["Please provide a prompt for processing."],
        )
    if len(prompt) < 10:
        return ValidatePromptResponse(
            isValid=False,
            errorMessage="Prompt is too short.",
            suggestions=[
                "Consider providing more detail in your prompt for better results."
            ],
        )
    return ValidatePromptResponse(isValid=True)
