from docx import Document

# Specify the .docx file and the output text file
docx_file = 'E:\GIT\Accenture-Questions\Quantitative Aptitude.docx'
output_file = 'Question2.txt'

# Read the .docx file
doc = Document(docx_file)

# Open the output text file in write mode
with open(output_file, 'w') as txt_file:
    # Loop through each paragraph in the .docx file
    for paragraph in doc.paragraphs:
        # Write the paragraph text to the .txt file
        txt_file.write(paragraph.text + '\n')

print(f'Docx file content has been written to {output_file}')
