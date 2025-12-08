from dotenv import load_dotenv
import os
from typing import List, Dict, Optional
from openai import OpenAI
from openai._exceptions import (
    AuthenticationError,
    APIError,
    APIConnectionError,
    RateLimitError,
)

load_dotenv()
ENV_KEYS = {
    "API_KEY": "DEEPSEEK_APP_KEY",
    "BASE_URL": "DEEPSEEK_BASE_URL",
    "MODEL": "DEEPSEEK_MODEL",
}

DEFAULT_MAX_HISTORY = 20
DEFAULT_TIMEOUT = 60

class ChatWithHistoryLLM:
    def __init__(self, max_history: int = DEFAULT_MAX_HISTORY, timeout: int = DEFAULT_TIMEOUT):
        self._validate_and_load_config()
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
            timeout=timeout
        )
        self.max_history = max_history
        self.history: List[Dict[str, str]] = []

    def _validate_and_load_config(self):
        self.api_key = self._get_env(ENV_KEYS["API_KEY"], required=True)
        self.base_url = self._get_env(ENV_KEYS["BASE_URL"], required=True)
        self.model = self._get_env(ENV_KEYS["MODEL"], required=True)

    def _get_env(self, key: str, required: bool = False) -> Optional[str]:
        value = os.getenv(key)
        if required and value is None:
            raise ValueError(f"Environment variable {key} is required but not set.")
        return value

    def _truncate_history(self) -> None:
        if len(self.history) > self.max_history:
            # remove oldest messages
            self.history = self.history[-self.max_history:]

    def chat(self, user_input) -> str:
        # Append user input to history
        user_input_stripped = user_input.strip()
        if not user_input_stripped:
            raise ValueError("User input cannot be empty.")
        self.history.append({"role": "user", "content": user_input_stripped})

        try:
            self._truncate_history()
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=self.history,
                temperature=0.7,
            )
            response = completion.choices[0].message.content
            self.history.append({"role": "assistant", "content": response})
            return response
        except AuthenticationError as auth_err:
            return f"Authentication Error: {str(auth_err)}"
        except APIConnectionError as conn_err:
            return f"API Connection Error: {str(conn_err)}"
        except RateLimitError as rate_err:
            return f"Rate Limit Error: {str(rate_err)}"
        except APIError as api_err:
            return f"API Error: {str(api_err)}"
        except Exception as e:
            return f"An unexpected error occurred: {str(e)}"
    
    def clear_history(self) -> None:
        self.history = []
    
if __name__ == "__main__":
    try:
        chat_llm = ChatWithHistoryLLM()
        while True:
            try:
                user_input = input("User: ")
            except KeyboardInterrupt:
                print("\nExiting chat.")
                break

            if user_input.lower() in ["exit", "quit"]:
                break

            if user_input.lower() == "clear":
                chat_llm.clear_history()
                print("Chat history cleared.")
                continue

            response = chat_llm.chat(user_input)
            print(f"Assistant: {response}")
    except ValueError as ve:
        print(f"Input Error: {str(ve)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")