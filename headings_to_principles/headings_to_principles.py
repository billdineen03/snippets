import csv, os, sys
from ast import literal_eval
import pandas as pd

read_file = pd.read_excel(sys.argv[1])
read_file.to_csv('working_file.csv', index = None, header = True)
number = sys.argv[1].replace('.xlsx', '')
sheet_name = f'Extract supporting details {number}'
md_name = f'Principles and snippets #{number}'

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

      
with open(f'{sheet_name}.csv', 'w', newline='') as csvfile:
    fieldnames = ['book_title', 'heading', 'principle', 'snippets']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(output)

with open(f'{md_name}.md', 'w') as markdown_file:
    with open(f'{sheet_name}.csv') as new_sheet:
        new_reader = csv.reader(new_sheet)
        for i, row in enumerate(new_reader):
            if i == 0:
                continue
            markdown_file.write('# principle: ' + row[2] + '\n\n')
            snippets = row[3].split('",')
            for i, snippet in enumerate(snippets):
                markdown_file.write(f'## snippet {i+1}:\n\n' + snippet.strip(']').replace('\\n', '\n') + '\n\n')

with open(f'{sheet_name}.csv') as f:
    df = pd.read_csv(f)
    df['What_info'] = ''
    df['Why_info'] = ''
    df['How_info'] = ''
    df['optional_comments'] = ''
    df['valid?'] = ''
    df['review_comments'] = ''
    df['suggested_alt_What'] = ''
    df['suggested_alt_Why'] = ''
    df['suggested_alt_How'] = ''
    df.to_csv(f'{sheet_name}.csv', index=False)
            

os.remove('working_file.csv')