from brain import GroqLLMClient 
from prompt_library import system_prompt_for_format_query

def format_query(user_prompt: str, column_dtype_dict: dict,temperature: float = 0.5):
    client = GroqLLMClient()
    
    # Format the system prompt with the provided parameters
    formatted_system_prompt = system_prompt_for_format_query.format(
        column_dtype_dict=column_dtype_dict,
    )
    
    response = client.get_response(
        prompt=user_prompt,
        system_prompt=formatted_system_prompt,
        temperature=temperature,
        model="deepseek-r1-distill-llama-70b"
    )
    return response["content"]