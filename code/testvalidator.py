import argparse
import sys
from utils import analyze_files, generate_text, path_exists, write_text_to_file, change_file_extension, replace_tokens_in_file_text, replace_extension, convert_wsd_to_png  # Import the functions
import os

def analyze(source_path, output, show_results):

    # Check if the source path exists
    path_exists(source_path)

    print(f"Analyzing project: "  + str(source_path))
    print(f"Output destination: " + str(output))
    print(f"Show results: " + str(show_results))

    print("""
Progress:
    """)

    # Get listing of source

    print("(1/3) Getting source code...")    

    contentSource = process_file("content/context.txt")

    if not contentSource:
        resultSource = analyze_files(root_dir=source_path)
    else:
        resultSource = contentSource
  

    # Ask for analysis

    print("(2/3) Analyzing source code...")

    prompt = replace_tokens_in_file_text("./templates/analyze.templ", {"@@INPUT1@@": resultSource})

    # write the final prompt into content/source.txt file for review
    try:
        with open("content/source.txt", 'w', encoding='utf-8') as file:
            file.write(prompt)
    except Exception as e:
        print(f"Error writing text to {e}")

    result = generate_text(prompt)

    # Send results to output

    print("(3/3) Writing output...")

    write_text_to_file(result, output)

    # Optionally show results on screen

    if show_results:
        print(result)

    print(f"""
Success: Analysis complete!
Output file created at: """ + str(output) + """
--------------------------------------------------------------------------------
    """)

# Function to process and concatenate the content of a file
def process_file(file_path):
    con_content = ""    
    if os.path.exists(file_path):    
        con_content += f"File: {file_path}\n"
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            content = file.read()
            con_content += content + "\n\n"
    else:
        con_context = ""
    return con_content

def main():

    print("""
        #####
        #   #
        #   #
        #####
Cadinal Senior software engineer test analsis
Version 1.0.0

--------------------------------------------------------------------------------
Initializing... Please wait...
    """)

    parser = argparse.ArgumentParser(description="Cardinal Test Analysis Tool")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subparser for 'analyze' command
    parser_analyze = subparsers.add_parser('analyze', help='Analyze java source code')
    parser_analyze.add_argument('source_path', help='Path to the java source code')
    parser_analyze.add_argument('-o', '--output', help='Path to save the analysis report', default='out/analysis_report/analysis_report.md')
    parser_analyze.add_argument('--show-results', help='Display analysis results on the screen', action='store_true')
    parser_analyze.set_defaults(func=analyze)

    try:

        # Parse the arguments
        args = parser.parse_args()

        # Retrieve the function to call
        func = args.func

        # Create a new dictionary that contains only the arguments for the function
        # This excludes 'command' and 'func'
        args_for_func = {k: v for k, v in vars(args).items() if k not in ['command', 'func']}

        # Call the function with the arguments
        func(**args_for_func)

    except FileNotFoundError as e:
        print(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
