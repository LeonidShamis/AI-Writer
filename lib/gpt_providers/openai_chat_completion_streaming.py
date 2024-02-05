import sys
import logging
import openai

# Configure standard logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def openai_chatgpt_streaming_text(user_prompt):
    """
    Uses streaming functionality to get real-time output from OpenAI's GPT model.

    Args:
        user_prompt (str): The prompt to send to the model.

    Returns:
        str: The complete text generated by the model in response to the prompt.

    Raises:
        SystemExit: If an error occurs in connecting to the OpenAI API or during streaming.
    """
    try:
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-16k",
            messages=[{"role": "user", "content": user_prompt}],
            max_tokens=8192,
            temperature=0.9,
            n=1,
            stream=True
        )

        collected_events = []
        completion_text = ''

        logger.info("Starting to receive streaming responses...")
        for chunk in response:
            collected_events.append(chunk)  # Save the event response
            event_text = chunk.choices[0].delta.content  # Extract the text
            completion_text += event_text  # Append the text
            sys.stdout.write(event_text)
            sys.stdout.flush()

        logger.info("Completed receiving streaming responses.")
        return completion_text

    except openai.OpenAIError as e:
        logger.error(f"OpenAI API Error: {e}")
        sys.exit("Exiting due to OpenAI API error.")

    except Exception as e:
        logger.error(f"Unexpected error during streaming: {e}")
        sys.exit("Exiting due to an unexpected error.")