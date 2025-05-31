import sys
import io
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def run_pandas_code(code: str,file_name: str) -> str:
    """
    Executes the given Python code with pandas, numpy and matplotlib support.
    """
    # Redirect stdout to capture print statements
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    try:
        df = pd.read_csv(file_name)

        # Include all required packages in local_vars
        local_vars = {
            "df": df,
            "pd": pd,
            "np": np, 
            "plt": plt,
            "__builtins__": __builtins__
        }
        # Pass local_vars as both globals and locals
        exec(code, local_vars, local_vars)
        output = sys.stdout.getvalue()
        return output if output else "Code executed successfully but produced no output"
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        sys.stdout = old_stdout

code="""

def calculate_max_sale():
    if df['sales'].empty:
        raise ValueError("Sale column is empty")

    max_sale = df['sales'].dropna().max()

    analysis_period = "Analysis period: No date filters applied"

    result = {
        'data': max_sale,
        'analysis_period': analysis_period
    }

    return result

# Execute the function
result = calculate_max_sale()
print(result)
"""

if __name__ == "__main__":
    # Example code to execute
    result = run_pandas_code(code,"dummy_sales_data.csv")
    print(result)