import argparse
import openai
import os
import sys
import io
import json
import time
from datetime import datetime
from dotenv import load_dotenv

def log_transaction(model, input_len, output_len, duration, status="success", error=None):
    """Appends a JSON record to data/flight_recorder.jsonl"""
    try:
        # Determine project root (one level up from this script)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(script_dir)
        data_dir = os.path.join(project_root, "data")
        log_file = os.path.join(data_dir, "flight_recorder.jsonl")

        # Ensure directory exists
        os.makedirs(data_dir, exist_ok=True)

        # Construct record
        record = {
            "timestamp": datetime.now().isoformat(),
            "script": "call_advanced_model.py",
            "model": model,
            "tokens_in_chars": input_len,
            "tokens_out_chars": output_len,
            "duration_sec": round(duration, 2),
            "status": status,
            "error": str(error) if error else None
        }

        # Append to file
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
            
    except Exception as e:
        # Never fail the main mission just because logging failed
        sys.stderr.write(f"[WARNING] Logging failed: {e}\n")

def main():
    # Record start time for duration metrics
    start_time = time.time()

    # Force stdout to use UTF-8
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    
    load_dotenv() 
    parser = argparse.ArgumentParser(description="Call an advanced language model via OpenRouter/Gemini API.")
    parser.add_argument("--prompt", type=str, help="Short query for the model.")
    parser.add_argument("--prompt-file", type=str, help="Path to a file containing a long prompt.")
    parser.add_argument("--model", type=str, default="gemini-2.5-pro",
                        help="Model to use (defaults to 'gemini-2.5-pro').")

    args = parser.parse_args()

    # --- 1. LOAD CONTENT ---
    prompt_content = ""
    if args.prompt:
        prompt_content = args.prompt
    elif args.prompt_file:
        try:
            sys.stderr.write(f"[DEBUG] Reading prompt file: {args.prompt_file}\n")
            with open(args.prompt_file, 'r', encoding='utf-8') as f:
                prompt_content = f.read()
        except Exception as e:
            sys.stderr.write(f"[ERROR] Could not read prompt file: {e}\n")
            sys.exit(1)

    if not prompt_content.strip():
        sys.stderr.write("[ERROR] Prompt content is empty.\n")
        sys.exit(1)

    # --- 2. INSTRUMENTATION (INPUT) ---
    char_count = len(prompt_content)
    word_count = len(prompt_content.split())
    
    sys.stderr.write(f"\n{'='*20} INPUT DIAGNOSTICS {'='*20}\n")
    sys.stderr.write(f"Model: {args.model}\n")
    sys.stderr.write(f"Size:  {char_count:,} chars | ~{word_count:,} words\n")
    sys.stderr.write(f"--- HEAD (First 500 chars) ---\n")
    sys.stderr.write(prompt_content[:500] + "\n")
    sys.stderr.write(f"\n--- TAIL (Last 500 chars) ---\n")
    sys.stderr.write(prompt_content[-500:] + "\n")
    sys.stderr.write(f"{'='*58}\n\n")

    # --- 3. CALL API ---
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        error_msg = "GOOGLE_API_KEY not found in .env"
        sys.stderr.write(f"[ERROR] {error_msg}\n")
        log_transaction(args.model, char_count, 0, time.time() - start_time, "error", error_msg)
        sys.exit(1)

    client = openai.OpenAI(
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        api_key=api_key,
    )

    try:
        sys.stderr.write(f"[DEBUG] Sending request to Gemini... (Please wait)\n")
        response = client.chat.completions.create(
            model=args.model,
            messages=[{"role": "user", "content": prompt_content}],
        )
        
        response_content = response.choices[0].message.content
        duration = time.time() - start_time
        
        if response_content:
            # --- 4. INSTRUMENTATION (OUTPUT) ---
            out_char_count = len(response_content)
            
            # Log to Flight Recorder
            log_transaction(args.model, char_count, out_char_count, duration, "success")

            sys.stderr.write(f"\n{'='*20} OUTPUT DIAGNOSTICS {'='*20}\n")
            sys.stderr.write(f"Status: Success\n")
            sys.stderr.write(f"Time:   {round(duration, 2)}s\n")
            sys.stderr.write(f"Size:   {out_char_count:,} chars\n")
            sys.stderr.write(f"--- PREVIEW (First 500 chars) ---\n")
            sys.stderr.write(response_content[:500] + "\n")
            sys.stderr.write(f"{'='*59}\n")
            
            # THE PAYLOAD (Standard Output)
            sys.stdout.write(response_content)
        else:
            error_msg = "Received empty response from model"
            log_transaction(args.model, char_count, 0, duration, "error", error_msg)
            sys.stderr.write(f"[ERROR] {error_msg}.\n")
            sys.exit(1)
            
    except Exception as e:
        duration = time.time() - start_time
        log_transaction(args.model, char_count, 0, duration, "error", str(e))
        sys.stderr.write(f"[ERROR] API Call Failed: {e}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()