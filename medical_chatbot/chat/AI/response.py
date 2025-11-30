from openai import AzureOpenAI
from dotenv import load_dotenv
import os
from .input_filter import *
import logging

#load environmental variables.
load_dotenv()

# Ensure required environment variables are set
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")
OPENAI_DEPLOYMENT_NAME = os.getenv("OPENAI_DEPLOYMENT_NAME")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_VERSION = os.getenv("OPENAI_API_VERSION")


# Ensure all variables are strings (not None)
if not all(isinstance(var, str) for var in [OPENAI_API_BASE, OPENAI_DEPLOYMENT_NAME, OPENAI_API_KEY, OPENAI_API_VERSION]):
    logging.error("One or more required OpenAI environment variables are not of type str.")
    raise TypeError("One or more required OpenAI environment variables are not of type str.")

logging.info("Environment variables loaded successfully.")

# Initialize Azure OpenAI client
client = AzureOpenAI(
    azure_endpoint=OPENAI_API_BASE,
    azure_deployment=OPENAI_DEPLOYMENT_NAME,
    api_key=OPENAI_API_KEY,
    api_version=OPENAI_API_VERSION
)

conversation_history = []

conversation_history = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

def Ask_AI(prompt: str, conversation_history: list) -> str:
    try:
        logging.info("Preparing to call Azure OpenAI API.")
        #Append user input to converstion history.
        conversation_history.append({"role": "user", "content": prompt})
        
        # Use a chat model (e.g., gpt-35-turbo or gpt-4). Adjust based on your deployment.
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Replace with your actual chat model deployment name
            messages=conversation_history,
            temperature=0.2,
            top_p=0.8,
            max_tokens=300  # Optional: Limit response length
        )
        answer = response.choices[0].message.content
        
        # Append AI response to history
        conversation_history.append({"role": "assistant", "content": answer})
        
        # Validate the response
        if answer is None:
            logging.error("API returned no content in response.")
            raise RuntimeError("API returned no content in response.")
        if not validate_response(answer):
            logging.warning("AI response failed validation; using fallback.")
            return "I'm sorry, but I can only provide information on medical topics. Please rephrase your query or consult a professional."
        
        logging.info(f"AI response generated successfully: length {len(answer)}")
        return answer
    except Exception as e:
        logging.error(f"API call failed: {str(e)}")
        raise RuntimeError(f"API call failed: {str(e)}")


#Creating set of valid words for user input break condition.
check_words = {"exit", "quit", "close", "stop", "bye"}


def main():
    logging.info("Chatbot application started.")

    print("""Welcome! Type 'exit', 'quit', 'close', 'stop', 'bye' to quit.
                 Inputs are filtered for safety.
          """)
    while True:
        user_question = input("Enter your question: ").strip()
        if user_question.lower() in check_words:
            logging.info("User initiated exit.")
            print("Thanks for Reaching out to the HelpAI. Goodbye! Have A Nice Day!")
            break
        if not filter_input(user_question):
            continue  # Skip to next iteration if input is invalid
        try:
            answer = Ask_AI(user_question, conversation_history)
            print("AI Response:", answer)
        except Exception as e:
            logging.error(f"Error in main loop: {str(e)}")
            print(f"Error: {e}. Please try again.")
if __name__ == "__main__":
    main()