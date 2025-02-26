import csv, os
import pandas as pd

read_file = pd.read_excel('test_sheet.xlsx')
read_file.to_csv('working_file.csv', index = None, header = True)

with open('working_file.csv') as f:
    output = []
    reader = csv.reader(f)
    for i, row in enumerate(reader):
        if i == 0:
            continue
        if row[5] == 'x':
                continue
        elif row[5] == 'y':
            correct = row[3]
        elif row[5] == 'n':
            correct = row[7]
        else:
            raise Exception(f"Invalid validity status in row {i+1}")
        book_title = row[0]
        heading = row[1]
        snippets = row[2]
        
        principles = correct.split('- ')
        for principle in principles:
            if principle and principle != "None":
                output.append({'book_title': book_title, 'heading': heading, 'principle': principle.strip(), 'snippets': snippets})

      
with open('test_output.csv', 'w', newline='') as csvfile:
    fieldnames = ['book_title', 'heading', 'principle', 'snippets']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(output)

with open('test_output.md', 'w') as markdown_file:
    with open('test_output.csv') as new_sheet:
        new_reader = csv.reader(new_sheet)
        for i, row in enumerate(new_reader):
            if i == 0:
                continue
            markdown_file.write('# principle: ' + row[2] + '\n\n')
            snippets = row[3].split('[')
            for i, snippet in enumerate(snippets):
                if i == 0:
                    continue
                markdown_file.write(f'## snippet {i}:\n\n' + snippet.strip(']').replace('\\n', '\n') + '\n\n')
           
os.remove('working_file.csv')