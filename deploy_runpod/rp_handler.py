import runpod
import time
import logging
from huggingface_hub import InferenceClient, InferenceTimeoutError

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def handler(event):
    logging.info("Handler function started.")
    
    # Extract input
    input = event.get('input', {})
    prompt = input.get('prompt')
    seconds = input.get('seconds', 0)
    
    if not prompt:
        logging.error("No prompt provided in the input.")
        return {"error": "Prompt is required"}

    logging.info(f"Received prompt: {prompt}")
    logging.info(f"Sleep duration: {seconds} seconds")

    # Initialize inference client
    logging.info("Initializing InferenceClient...")
    client = InferenceClient(
        provider="hf-inference",
        api_key="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",
        timeout=120,
    )
    logging.info("InferenceClient initialized successfully.")

    # Prepare messages
    messages = [
        {
            "role": "user",
            "content": str(prompt)
        }
    ]
    logging.info("Messages prepared for inference.")

    # Call Hugging Face model
    try:
        logging.info("Sending request to Hugging Face API...")
        completion = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B",
            messages=messages,
            max_tokens=500,
            temperature=0.1,
        )
        logging.info("Response received from Hugging Face API.")
    except InferenceTimeoutError:
        print("Inference timed out after 120s.")
    except Exception as e:
        logging.error(f"Error during inference: {e}")
        return {"error": str(e)}

    # Extract the answer
    answer = completion.choices[0].message.content
    logging.info(f"Generated response: {answer}")

    print("==================================")
    print("Answer:", answer)
    print("==================================")

    # Sleep if necessary
    if seconds > 0:
        logging.info(f"Sleeping for {seconds} seconds...")
        time.sleep(seconds)
        logging.info("Sleep completed.")

    logging.info("Handler function completed.")
    return answer

if __name__ == '__main__':
    logging.info("Starting serverless function...")
    runpod.serverless.start({'handler': handler})
    logging.info("Serverless function started.")
