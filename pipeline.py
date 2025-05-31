from code_writer import code_writer
from code_exicution import run_pandas_code
from error_handling import run_code_with_rewrite_on_error
from Final_response import final_response
from format_query import format_query
import pandas as pd
def run_analysis_pipeline(user_query: str,file_name: str, max_attempts: int = 3) -> str:
    """
    Executes the complete analysis pipeline:
    1. Format the query --> (user_prompt,column_dict)
    2. Generate code --> (response of format query , column list)
    3. Execute code with error handling --> (formatted_query,filename,list of column, max_attempts)
    4. Generate final response -->(code_result,user_query)
    """
    df=pd.read_csv(file_name)
    column_dict = df.dtypes.to_dict()

    columns_list = df.columns.tolist()

    try:
        # Step 1: Format the query
        formatted_query = format_query(user_query,column_dict)
        print(f"Formatted Query: {formatted_query}")
        if "greet" in formatted_query.lower():
            return final_response(
                "greet",
                None
            )
        elif "This type of Content is not supported." in formatted_query:
            return final_response(
                "his type of Content is not supported.",
                None
            )
        else:
            # Step 2 & 3: Generate and execute code with error handling
            code_output, success = run_code_with_rewrite_on_error(formatted_query,columns_list,file_name, max_attempts)
            
            if not success:
                return f"Code execution failed after {max_attempts} attempts.\nDetails: {code_output}"
            #return final_response(
             #   code_output,
             #   query
            #)
            
            # Step 4: Generate final response with results
            final_result = final_response(
                code_output,
                user_query
            )
            
            return final_result
        
    except Exception as e:
        return f"Pipeline error: {str(e)}"

if __name__ == "__main__":
    # Example usage
    user_query = "which product has higest revenue give product name and revenue"
    file_name = "dummy_sales_data.csv"  # Example filename
    result = run_analysis_pipeline(user_query, file_name,3)
    print(result)