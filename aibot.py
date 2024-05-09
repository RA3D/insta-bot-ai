import openai

from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY


def instagram_comment_from_script(script):
    # Truncate the script to 1000 characters
    truncated_script = script[:1000]

    # Define the style of the comment needed for Instagram
    prompt = f"Based on this video script, generate a short, engaging Instagram comment:\n\n{truncated_script}"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=40,
            temperature=0.7,
        )
        comment = response['choices'][0]['message']['content']
        return comment.strip()
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""
