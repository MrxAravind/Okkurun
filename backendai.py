import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential


GitHub = os.getenv('Token') 


# List of available models
MODELS = [
    "Meta-Llama-3-8B-Instruct",
    "Cohere-command-r-plus-08-2024",
    "Ministral-3B",
    "AI21-Jamba-1.5-Large",
    "Phi-3.5-MoE-instruct",
    "gpt-4o-mini",
    "gpt-4o"
]

def run_inference(model,query):
    """Run inference on selected model"""
    client = ChatCompletionsClient(
        endpoint="https://models.inference.ai.azure.com",
        credential=AzureKeyCredential(GitHub),
    )

    try:
        response = client.complete(
            messages=[
                SystemMessage(content="You are a helpful AI assistant."),
                UserMessage(content=query),
            ],
            model=model,
            temperature=1,
            max_tokens=2048,
            top_p=0.1
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"
    
