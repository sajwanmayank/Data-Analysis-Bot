import os
from typing import Optional, Dict, Any
from dotenv import load_dotenv
from groq import Groq

class GroqLLMClient:
    """A client class for interacting with Groq LLM API"""
    
    def __init__(self, default_model: str = "deepseek-r1-distill-llama-70b"):
        load_dotenv()
        self.api_key = self._get_api_key()
        self.client = Groq(api_key=self.api_key)
        self.default_model = default_model

    @staticmethod
    def _get_api_key() -> str:
        """Retrieve API key from environment variables"""
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        return api_key

    def get_response(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.7,
    ) -> Dict[str, Any]:
        """
        Get response from Groq LLM
        Args:
            prompt: Input prompt
            system_prompt: System prompt to set context
            model: Model to use (defaults to self.default_model)
            temperature: Temperature for response generation
        Returns:
            Dict containing response content and metadata
        """
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        try:
            chat_completion = self.client.chat.completions.create(
                messages=messages,
                model=model or self.default_model,
                temperature=temperature
            )
            
            # Extract usage data directly from the attributes
            usage_data = None
            if hasattr(chat_completion, 'usage'):
                usage_data = {
                    'prompt_tokens': chat_completion.usage.prompt_tokens,
                    'completion_tokens': chat_completion.usage.completion_tokens,
                    'total_tokens': chat_completion.usage.total_tokens
                }
            
            return {
                "content": chat_completion.choices[0].message.content,
                "model": chat_completion.model,
                "usage": usage_data
            }
            
        except Exception as e:
            raise RuntimeError(f"API Error: {str(e)}")
