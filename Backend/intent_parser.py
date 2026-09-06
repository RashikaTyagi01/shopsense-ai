from dotenv import load_dotenv
from groq import Groq
import json

load_dotenv()

client = Groq()

def parse_intent(user_message: str):
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": """
        You are an intent extraction system for a shopping assistant.

        Do not recommend products.
        Do not answer the user's shopping request.

        Only extract the user's intent and return JSON with these fields:
        request_type
        search_query
        reorder_product
        max_price
        max_delivery_days
        exclude

        request_type must be one of:
        discovery, reorder, mixed

        For mixed requests, apply max_price, max_delivery_days, and exclude to the discovery/search part unless the user clearly attaches a constraint to the reorder item.

        Return only valid JSON.
        Do not use markdown code blocks or explanations.

        If a field is not present in the user's request,return null for that field.
        Never return an empty string.
        """
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
    )
    content=response.choices[0].message.content
    intent=json.loads(content)
    return intent

