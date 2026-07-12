from server import mcp, types
from shared.prompts import MAIL_FORMAT_TEMPLATE_PROMPT


@mcp.prompt()
def draft_job_email(job_description: str) -> list[types.PromptMessage]:
    """Analyze a job description and draft a professional outreach email."""
    return [
        types.PromptMessage(
            role="user",
            content=types.TextContent(
                type="text",
                text=MAIL_FORMAT_TEMPLATE_PROMPT.format(job_description=job_description)
            )
        )
    ]