testvalidator Tool Documentation
===========================

Compile Code:
-------------
To compile the testvalidator program, use the following command in your terminal:

    ./venv/bin/pyinstaller testvalidator.spec

Make sure you have activated the virtual environment where PyInstaller is installed.

If you experience errors due to missing python dependencies, run the following command in your terminal:

    pip install -r requirements.txt

Configure  Tool:
----------------
Ensure the config/testvalidator.config file exists and contains a valid API key for OpenAI in the following form, as well as a model that your OpenAI subscription is able to use (note that a free account might not be able to access the default model specified):

[DEFAULT]
api_key = api_key_value_goes_here
model = gpt-4-0125-preview

Usage Examples:
---------------
Below are examples of how to use the testvalidator tool from the command line. Ensure that you navigate to the `dist` directory where the executable is located before running these commands.

Note:
All commands should be run from the directory containing the executable.
Add .exe to the commands below when compiling and running on windows.

Place your Java code into testcode folder or any folder but provide that path as argument as below.
in the example below, Java code is placed into .\testcode\src folder.

Analyze Java code:
.\dist\testvalidator analyze .\testcode\src

Known Issues:
-------------

* This tool has only been tested against a small sample code base and will need further work to handle larger sets of input files.
* At the moment the tool produces .md markup files as output. To turn the .md file into a PDF you will need another tool - I use this VSCode plugin: https://marketplace.visualstudio.com/items?itemName=yzane.markdown-pdf