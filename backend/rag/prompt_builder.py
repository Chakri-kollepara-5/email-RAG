def build_prompt(user_email: str, retrieved_docs: list[str]):

    context_text = "\n\n".join(retrieved_docs)

    prompt = f"""
You rewrite emails to sound professional, respectful, calm and polite.

RULES:
- Fix grammar and tone
- Keep the SAME meaning
- Keep it short
- No emojis
- No slang
- Do NOT add extra information
- Output ONLY the rewritten email

Here are company-approved rewrite examples and tone guidelines:
{context_text}

Rewrite this email politely:

"{user_email}"
"""

    return prompt.strip()
