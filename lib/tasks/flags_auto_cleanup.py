import os
import re
import ollama

# ========== HELPERS ==========

def strip_code_fences_and_comments(text):
    print(f"\n\n\n Output after strip:::::: {text} \n\n\n")
    text = re.sub(r"^```(?:ruby)?\s*|```$", "", text.strip(), flags=re.MULTILINE).strip()
    lines = text.splitlines()
    return "\n".join(line for line in lines if not line.strip().startswith("//"))


def remove_flag_declarations(content: str, flag_name: str, model: str) -> str:
    prompt = f"""
You are a Ruby code modifier. Do NOT add any comments and explanations.

The goal is to REMOVE any usage of the feature flag `{flag_name}` from the following code.

🧹 What to do:
- Only delete the line that declares it (e.g. ... = show_feature?(`{flag_name}`)).
- Do not change any other code.
- Do NOT remove unrelated code.
- Do NOT change any indentation and formatting.
- DO NOT add any comments and explanations.
- Do NOT add any extra lines or headers (e.g., "Here is your cleaned code").
- Do not add any explanation and formatting.
- Return the cleaned code only — no Markdown or extra text.

Here is the file:
{content}
"""
    response = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}])
    return strip_code_fences_and_comments(response["message"]["content"])


def process_ruby_file(file_path, flag_name, model):
    # flag_path = f"show_feature?({flag_name})"
    # with open(file_path, "r", encoding="utf-8") as f:
    #     original = f.read()

    # if flag_path not in original and flag_name not in original:
    #     return  # Skip
    flag_path = f"show_feature?({flag_name})"

    with open(file_path, "r", encoding="utf-8") as f:
        original = f.read()

    if flag_name not in original:
        return  # Skip

    print(f"\n========== in process_ruby_file ===flag found in this file=== {flag_path} =====\n")
    print(f"🔧 Processing: {file_path}")

    try:
        cleaned = remove_flag_declarations(original, flag_name, model)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(cleaned)

        print(f"✅ Updated: {file_path}")

    except Exception as e:
        print(f"❌ Failed to update {file_path}: {e}")

def scan_codebase(code_path, flag_name, model):
    for root, _, files in os.walk(code_path):
        for file in files:
            if file.endswith(".rb"):
                full_path = os.path.join(root, file)
                process_ruby_file(full_path, flag_name, model)

def get_variable_name(file_path, key):
    for root, _, files in os.walk(file_path):
        for file in files:
            if file.endswith(".rb"):
                full_path = os.path.join(root, file)
                # with open(full_path, "r") as file:
                with open(full_path, 'r', encoding='utf-8') as file:
                    ruby_code = file.read()

                # Regex pattern to match the Ruby constant definition
                pattern = rf'(\w+)\s*=\s*show_feature\?\("{key}"\)'
                match = re.search(pattern, ruby_code)
                if match:
                    print(f"=========== in get_variable_name match found in this file::::{full_path}\n")
                    return match.group(1)
    return None

# ========== ENTRY POINT ==========

if __name__ == "__main__":
    flag_key = input("🔍 Enter the feature flag name to remove (e.g., pw_enable_user_login_validation): ").strip()
    codebase_path = input("📁 Enter the root path to your Ruby codebase: ").strip()
    model = "mistral"

    flag_name = get_variable_name(codebase_path, flag_key);
    print("\n flagname start ==== \n")
    print(flag_name)
    print("\n flagname end ==== \n")
    if flag_name != None:
        print(f"\n🚀 Starting cleanup for flag `{flag_key}` in `{codebase_path}` using model `{model}`\n")
        scan_codebase(codebase_path, flag_name, model)
        print("\n🏁 Completed.\n")
    else:
        print(f"\n🚀 Given flag Doesn't present in the code -- `{flag_key}` \n")
