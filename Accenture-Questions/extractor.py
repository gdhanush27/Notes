import os

# Specify the directory to scan and the output file
directory = 'Accenture-Previous-Year-Coding-Questions-\Accenture Previous Year Coding Questions'
output_file = 'Questions.md'

# List of file extensions to include
file_extensions = ['.c', '.cpp', '.java', '.py']

# Open the output file in write mode
with open(output_file, 'w') as outfile:
    # Walk through the directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Check if the file has one of the specified extensions
            if any(file.endswith(ext) for ext in file_extensions):
                file_path = os.path.join(root, file)
                file_extension = os.path.splitext(file)[1][1:]
                # Write file name and content to the output file
                outfile.write(f'# {file} \n ```{file_extension} \n')
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as infile:
                    outfile.write(infile.read())
                outfile.write(f'\n ``` \n\n')

print(f'All specified files have been written to {output_file}')
