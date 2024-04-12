from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class SubmitFeedbackResponse(BaseModel):
    """
    Confirmation of the successful feedback submission. Includes a reference to the submitted feedback.
    """

    success: bool
    message: str
    feedback_id: Optional[str] = None


async def submit_feedback(
    user_id: str, prompt_id: str, rating: int, comments: Optional[str]
) -> SubmitFeedbackResponse:
    """
    Endpoint for users to submit feedback on a prompt refinement.

    Args:
    user_id (str): Unique identifier for the user submitting the feedback.
    prompt_id (str): Identifier of the prompt associated with this feedback.
    rating (int): Numerical rating provided by the user for the prompt refinement quality (1-5).
    comments (Optional[str]): Optional textual comments detailing user feedback on the refinement.

    Returns:
    SubmitFeedbackResponse: Confirmation of the successful feedback submission. Includes a reference to the submitted feedback.

    This function will attempt to create a feedback entry in the database associated with the given prompt and user.
    If the operation is successful, it returns a SubmitFeedbackResponse with success=True and the feedback_id.
    If the operation fails (e.g., user or prompt not found, invalid rating), it returns a SubmitFeedbackResponse with success=False.
    """
    user = await prisma.models.User.prisma().find_unique(where={"id": user_id})
    prompt = await prisma.models.Prompt.prisma().find_unique(where={"id": prompt_id})
    if not user or not prompt:
        return SubmitFeedbackResponse(
            success=False, message="User or prompt not found."
        )
    if rating < 1 or rating > 5:
        return SubmitFeedbackResponse(
            success=False, message="Rating must be between 1 and 5."
        )
    try:
        feedback = await prisma.models.Feedback.prisma().create(
            data={
                "userId": user_id,
                "promptId": prompt_id,
                "rating": rating,
                "content": comments if comments else "",
            }
        )
        return SubmitFeedbackResponse(
            success=True,
            message="Feedback submitted successfully.",
            feedback_id=feedback.id,
        )
    except Exception as e:
        return SubmitFeedbackResponse(
            success=False, message=f"Failed to submit feedback: {str(e)}"
        )
