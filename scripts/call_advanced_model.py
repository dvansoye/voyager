import argparse
import openai
import os
import sys
import io
from dotenv import load_dotenv

def main():
    # Force stdout to use UTF-8
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    load_dotenv() # Load environment variables from .env file
    parser = argparse.ArgumentParser(description="Call an advanced language model via OpenRouter API.")
    parser.add_argument("--prompt", type=str, help="Short query for the model.")
    parser.add_argument("--prompt-file", type=str, help="Path to a file containing a long prompt.")
    parser.add_argument("--model", type=str, default="gemini-2.5-pro",
                        help="Model to use (defaults to 'gemini-2.5-pro').")

    args = parser.parse_args()

    if not args.prompt and not args.prompt_file:
        sys.stderr.write("Error: Either --prompt or --prompt-file must be provided.\n")
        sys.exit(1)

    prompt_content = ""
    if args.prompt:
        prompt_content = args.prompt
    elif args.prompt_file:
        try:
            with open(args.prompt_file, 'r', encoding='utf-8') as f:
                prompt_content = f.read()
        except FileNotFoundError:
            sys.stderr.write(f"Error: File not found at {args.prompt_file}\n")
            sys.exit(1)
        except Exception as e:
            sys.stderr.write(f"Error reading prompt file: {e}\n")
            sys.exit(1)

    if not prompt_content.strip():
        sys.stderr.write("Error: Prompt content is empty after reading from argument or file.\n")
        sys.exit(1)

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        sys.stderr.write("Error: GOOGLE_API_KEY environment variable not set.\n")
        sys.exit(1)

    client = openai.OpenAI(
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        api_key=api_key,
    )

    try:
        response = client.chat.completions.create(
            model=args.model,
            messages=[{"role": "user", "content": prompt_content}],
        )
        response_content = response.choices[0].message.content
        if response_content:
            sys.stdout.write(response_content)
        else:
            sys.stderr.write("Error: Received empty response content from the model.\n")
            sys.exit(1)
    except openai.APIError as e:
        sys.stderr.write(f"OpenRouter API Error: {e}\n")
        sys.exit(1)
    except Exception as e:
        sys.stderr.write(f"An unexpected error occurred: {e}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()