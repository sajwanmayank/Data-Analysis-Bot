from brain import GroqLLMClient 
from prompt_library import system_prompt_for_final_response

def final_response(code_result: str,query: str, temperature: float = 0.5):
    client = GroqLLMClient()
    formatted_system_prompt = system_prompt_for_final_response.format(
        query=query,
    )
    response = client.get_response(
        prompt=code_result,
        system_prompt=formatted_system_prompt,
        temperature=temperature,
        model="llama-3.1-8b-instant"
    )
    #print("Model used:", response["model"])
    return response["content"]
    #if response.get("usage"):
     #   print("\nToken usage:", response["usage"])

if __name__ == "__main__":
    user_prompt = "{'data': np.float64(974.54), 'analysis_period': 'Analysis period: No date filters applied'}"
    print(final_response("this type of content not supported","who is mayank"))