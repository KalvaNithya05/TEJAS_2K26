import os
from dotenv import load_dotenv

backend_env = os.path.join('backend', '.env')
print(f"Checking {backend_env}")

if os.path.exists(backend_env):
    print("File exists.")
    with open(backend_env, 'r') as f:
        content = f.read()
        print(f"File size: {len(content)}")
        if 'your_supabase' in content:
            print("WARNING: File content contains 'your_supabase' placeholder string.")
        else:
            print("File content does NOT contain 'your_supabase'.")
else:
    print("File does NOT exist.")

print("-" * 20)
print("Loading dotenv...")
load_dotenv(backend_env)
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

print(f"URL: {url}")
if key:
    print(f"KEY: {key[:5]}...{key[-5:] if len(key)>5 else ''}")
else:
    print("KEY: None")
