# utils.py
import os
from openai import OpenAI
import configparser
import plantuml

# Check if a given path exists.
def path_exists(path):

    if not os.path.exists(path):
        raise FileNotFoundError(f"The specified path does not exist: {path}")
    
def load_api_key():
    config = configparser.ConfigParser()
    config.read('config/testvalidator.config')
    return config['DEFAULT']['api_key']

def load_model():
    config = configparser.ConfigParser()
    config.read('config/testvalidator.config')
    return config['DEFAULT']['model']
    
# Gen AI prompt inference
def generate_text(prompt):

    try:

        client = OpenAI(
            api_key=load_api_key()
        )

        chat_completion = client.chat.completions.create(

            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that provides information.",
                },
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=load_model(),
        )

        return chat_completion.choices[0].message.content
    except Exception as e:
        return str(e)
    
def analyze_files(root_dir='./', excluded_dirs=['.*', '.git', '.vscode','.venv','Views','Scripts','Rotativa','ReportsContainer','Content','Common','2013.2.611','ASPNetSpellInclude','2011.3.1115','htmls','Properties','packages','bin','obj', 'node_modules', 'target']
                  , excluded_files=['package-lock.json', '*.png', '*.ico','*.config','*.csproj','*.vspscc','*.resx','*.browser','*.cshtml','*.html','*.txt','*.asax','*.sitemap','*.xsd','*.user','*.xml']):
    """
    Analyze files in the specified directory and its subdirectories, excluding certain directories and file patterns.

    Args:
        root_dir (str): The root directory to start the search from.
        excluded_dirs (list): List of excluded directory patterns.
        excluded_files (list): List of excluded file patterns.

    Returns:
        str: Concatenated content of eligible files with filenames and paths.
    """
    concatenated_content = ""

    # Function to check if a file should be included
    def should_include(file_path):
        if any(excluded_dir in file_path for excluded_dir in excluded_dirs):
            return False
        if any(file_path.endswith(excluded_file) for excluded_file in excluded_files):
            return False
        return True

    # Function to process and concatenate the content of a file
    def process_file(file_path):
        nonlocal concatenated_content
        concatenated_content += f"File: {file_path}\n"
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            content = file.read()
            concatenated_content += content + "\n\n"

    # Traverse the directory and process eligible files
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            file_path = os.path.join(root, file)
            if should_include(file_path):
                process_file(file_path)

    return concatenated_content

# Example usage:
# concatenated_content = analyze_files(root_dir='./my_directory', excluded_dirs=['node_modules'], excluded_files=['package-lock.json'])
# print(concatenated_content)

def write_text_to_file(text, file_path):

    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, 'w',encoding='utf-8') as file:
            file.write(text)
        
    except Exception as e:
        print(f"Error writing text to {file_path}: {e}")

def replace_tokens_in_file_text(template_file_path, token_replacements):
    """
    Reads a template file, replaces multiple tokens with their corresponding replacement values, and returns the updated text.

    :param template_file_path: Path to the template file.
    :param token_replacements: Dictionary of tokens and their replacements.
                               Example: {"{{username}}": "JohnDoe", "{{date}}": "2024-01-30"}
    :return: The text of the file with tokens replaced.
    """
    try:
        # Read the content of the template file
        with open(template_file_path, 'r') as file:
            content = file.read()

        # Replace each token with its replacement
        for token, replacement in token_replacements.items():
            content = content.replace(token, replacement)

        return content

    except Exception as e:
        return f"An error occurred: {e}"

# Example usage
# updated_text = replace_tokens_in_file_text("path/to/template.txt", 
#                                            {"{{username}}": "JohnDoe", "{{date}}": "2024-01-30"})
# print(updated_text)

def change_file_extension(filename, new_extension):
    """
    Change the extension of a given filename to a new extension.

    Parameters:
    filename (str): The original filename.
    new_extension (str): The new extension to be applied.

    Returns:
    str: Filename with the new extension.
    """
    if not new_extension.startswith('.'):
        new_extension = '.' + new_extension

    # Split the filename into name and extension
    main_part, _ = filename.rsplit('.', 1) if '.' in filename else (filename, '')

    # Return the filename with the new extension
    return main_part + new_extension

def replace_extension(file_path, new_extension):
    # Split the original path into the root part and the extension
    root, _ = os.path.splitext(file_path)
    
    # Append the new extension to the root
    new_file_path = root + new_extension
    
    return new_file_path

def convert_wsd_to_png(wsd_file_path, output_png_path):
   
    if not os.path.exists(wsd_file_path):
        print(f"Input file does not exist: {wsd_file_path}")
        return
    
    plantumlContent=extract_plantuml_content(wsd_file_path)
    save_extracted_content(wsd_file_path,plantumlContent)
    
    server = plantuml.PlantUML(url='http://www.plantuml.com/plantuml/img/',
                          basic_auth={},
                          form_auth={}, http_opts={}, request_opts={})


    result = server.processes_file(wsd_file_path, output_png_path)
    if result:
        print(f"PNG image successfully created at {output_png_path}")
    else:
        print("Failed to create PNG image.")

def extract_plantuml_content(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    # Find the start and end of the desired content
    start_index = content.find('@startuml')
    end_index = content.find('@enduml')

    if start_index == -1 or end_index == -1:
        print("The specified tags were not found in the file.")
        return

    # Adjust indices to exclude '@startuml' and '@enduml' from the extracted content
    # Add length of '@startuml' and a newline to start_index
    # and just find '@enduml' without adding its length to end_index
    start_index += len('@startuml') + 1
    end_index = content.find('@enduml', start_index)

    # Extract the content between '@startuml' and '@enduml' (excluding the tags)
    plantuml_content = content[start_index:end_index].strip()

    # Output or save the extracted content
    return plantuml_content

def save_extracted_content(output_path, content):
    with open(output_path, 'w') as file:
        file.write(content)