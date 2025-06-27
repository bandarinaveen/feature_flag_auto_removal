import os
import re
import openai
from pathlib import Path
from typing import List, Dict

# Configure your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = "gpt-4"  # or "gpt-3.5-turbo"


# ========== HELPERS ==========
def get_file_content(file_path: str) -> str:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return ""

def remove_flag_declarations(content: str, flag_name: str, file_path: str) -> Dict:
    content = get_file_content(file_path)
    if not content:
        return {"file": file_path, "changes": [], "error": "Could not read file"}
    system_prompt = (
        "You are an AI assistant that helps remove feature flags from code. "
        "Your task is to analyze the code and return the full, updated file content with the feature flag removed. "
        "Focus on keeping the 'true' branch of any if conditions and removing the flag checks entirely. "
        "Return ONLY the updated file content as a single code block."
    )
    user_prompt = (
        f"Remove all usages of the feature flag '{flag_name}' (show_feature?('{flag_name}')) from the following file. "
        f"Return ONLY the full, updated file content, and nothing else.\n"
        f"File: {file_path}\n"
        "```\n"
        f"{content}\n"
        "```"
    )
    try:
        response = openai.ChatCompletion.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2,
            max_tokens=3000
        )
        analysis = response.choices[0].message.content
        new_content = extract_new_file_content(analysis)
        return {
            "file": file_path,
            "new_content": new_content,
            "analysis": analysis
        }
    except Exception as e:
        return {"file": file_path, "error": f"API Error: {str(e)}"}


def extract_new_file_content(analysis: str) -> str:
    """Extract only the code inside the first code block, ignoring explanations and markdown."""
    # Try to extract from ```ruby ... ``` or generic triple-backtick blocks
    match = re.search(r'```(?:rb)?\s*\n(.*?)\n```', analysis, re.DOTALL)
    if match:
        return match.group(1).strip()
    # fallback: if no code block, return the whole response (not recommended)
    return analysis.strip()


def process_ruby_file(file_path, flag_name):
    flag_path = f'show_feature?("{flag_name}")'

    with open(file_path, "r", encoding="utf-8") as f:
        original = f.read()

    if flag_name not in original:
        return  # Skip

    print(f"\n flag found in this file===> {flag_path} ===== \n")
    print(f"🔧 Processing: {file_path}")

    try:
        result = remove_flag_declarations(original, flag_name, file_path)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(result["new_content"])

        print(f"✅ Updated: {file_path}")

    except Exception as e:
        print(f"❌ Failed to update {file_path}: {e}")

def scan_codebase(code_path, flag_name):
    for root, _, files in os.walk(code_path):
        for file in files:
            if file.endswith(".rb"):
                full_path = os.path.join(root, file)
                process_ruby_file(full_path, flag_name)


# ========== ENTRY POINT ==========

if __name__ == "__main__":
    flag_key = input("🔍 Enter the feature flag name to remove (e.g., pw_enable_user_login_validation): ").strip()
    codebase_path = input("📁 Enter the root path to your Ruby codebase: ").strip()
    
    if flag_key != None:
        print(f"\n🚀 Starting cleanup for flag `{flag_key}` in `{codebase_path}` \n")
        scan_codebase(codebase_path, flag_key)
        print("\n🏁 Completed.\n")
    else:
        print(f"\n🚀 Given flag Doesn't present in the code -- `{flag_key}` \n")
