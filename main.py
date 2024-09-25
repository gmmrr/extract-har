import json
import os
import base64

def extract_files_from_har(har_file_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    with open(har_file_path, 'r', encoding='utf-8') as file:
        har_data = json.load(file)

    entries = har_data['log']['entries']

    for entry in entries:
        request_url = entry['request']['url']
        response_content = entry['response']['content']

        filename = request_url.split('/')[-1]
        if not filename:
            filename = 'unknown_file'

        if len(filename) > 255:
            print(f"Filename too long: {filename}. Skipping...")
            continue

        if response_content.get('encoding') == 'base64':
            content = base64.b64decode(response_content['text'])
        else:
            content = response_content.get('text', '').encode('utf-8')

        file_path = os.path.join(output_dir, filename)
        with open(file_path, 'wb') as file:
            file.write(content)

        print(f"Saved {filename} to {file_path}")

if __name__ == "__main__":
    har_file_path = 'temp3.har'
    output_dir = './result3'

    extract_files_from_har(har_file_path, output_dir)
