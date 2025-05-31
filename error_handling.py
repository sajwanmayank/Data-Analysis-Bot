from code_writer import code_writer 
from code_exicution import run_pandas_code
from typing import Tuple

def run_code_with_rewrite_on_error(user_prompt: str,coulmn_list: list,file_name: str, max_attempts: int = 3) -> Tuple[str, bool]:
    """
    Runs code generated from user_prompt with multiple retry attempts on error.
    
    Args:
        user_prompt (str): The original prompt for code generation
        max_attempts (int): Maximum number of attempts to rewrite and retry code
        
    Returns:
        Tuple[str, bool]: (output/error message, success status)
    """
    attempt = 1
    previous_errors = []
    
    while attempt <= max_attempts:
        if attempt == 1:
            code = code_writer(user_prompt, coulmn_list)
        else:
            # Enhanced prompt with error history
            error_history = "\n".join([f"Attempt {i+1} failed with: {err}" 
                                     for i, err in enumerate(previous_errors)])
            new_prompt = (
                f"{user_prompt}\n\n"
                f"Previous attempts failed with these errors:\n{error_history}\n"
                f"This is attempt {attempt} of {max_attempts}. "
                "Please write the function again avoiding these errors."
            )
            code = code_writer(new_prompt, coulmn_list)
        
        output = run_pandas_code(code, file_name)
        print(code)
        if not output.startswith("Error:"):
            return output, True
        
        previous_errors.append(output)
        attempt += 1
    
    # If we've exhausted all attempts, return the final error
    final_message = (
        f"Failed after {max_attempts} attempts. Last error: {previous_errors[-1]}\n"
        f"Error history:\n{chr(10).join(previous_errors)}"
    )
    return final_message, False

if __name__ == "__main__":
    user_prompt = "write a code for taking out maximum sale from column 'sale' from dataset 'sales.csv' and print the result"
    result, success = run_code_with_rewrite_on_error(user_prompt,['sale'],'sales.csv',max_attempts=3)
    if success:
        print("Success! Output:", result)
    else:
        print("Failed! Details:", result)