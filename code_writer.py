from brain import GroqLLMClient 
from prompt_library import system_prompt_for_code_writer
import re

def clean_code_response(response: str ) -> str:
    """
    Cleans the code response from the code_writer function.
    Removes any leading/trailing whitespace, code block markers, any content before and including </think> tags,
    and ensures the code is ready for execution.
    """
    # Remove code block markers
    code = re.sub(r"^```(?:python)?\s*|\s*```$", "", response.strip(), flags=re.MULTILINE)
    # Remove everything up to and including the first </think> tag (if present)
    code = re.sub(r"[\s\S]*?</think>\s*", "", code, count=1, flags=re.IGNORECASE)
    return code.strip()

def code_writer(user_prompt: str,column_names: str, temperature: float = 0.5):
    client = GroqLLMClient()
    formatted_system_prompt = system_prompt_for_code_writer.format(
        column_names=column_names,
    )
    response = client.get_response(
        prompt=user_prompt,
        system_prompt=formatted_system_prompt,
        temperature=temperature,
        model="gemma2-9b-it"
    )
    cleaned_code = clean_code_response(response["content"])
    return cleaned_code

if __name__ == "__main__":
    user_prompt = "calculate maximum for column 'sales'."
    print(code_writer(user_prompt,['sale', 'date', 'product']))
