import requests
import re

def get_key_from_js():
    base_url = "https://www.blackbox.ai"
    response = requests.get(base_url)

    if response.status_code != 200:
        print("Failed to load the page.")
        return None

    # Get the HTML of the page
    js_files = re.findall(r'static/chunks/\d{4}-[a-fA-F0-9]+\.js', response.text)
    
    # Pattern to match UUID format in JavaScript files
    key_pattern = re.compile(r'w="([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})"')

    for js_file in js_files:
        js_url = f"{base_url}/_next/{js_file}"
        js_response = requests.get(js_url)

        if js_response.status_code == 200:
            # Find all JavaScript file links
            match = key_pattern.search(js_response.text)
            if match:
                return {"key": match.group(1), "source": js_url}

    print("Key not found")
    return None

result = get_key_from_js()
if result:
    print("Validated Key:", result["key"])
    print("Source file:", result["source"])
else:
    print("Key not found")