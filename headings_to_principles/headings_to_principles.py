import csv
import pandas as pd

with open('test_sheet.csv') as f:
    output = []
    reader = csv.reader(f)
    for i, row in enumerate(reader):
        if i == 0:
            continue
        try:
            row[5] == 'y' or row[5] == 'n' or row[5] == 'x'
        except:
            print(f"Invalid validity status in row {i+1}")
        else:
            if row[5] == 'x':
                continue
            book_title = row[0]
            heading = row[1]
            snippets = row[2]
            if row[5] == 'y':
                correct = row[3]
            elif row[5] == 'n':
                correct = row[7]
            principles = correct.split('- ')
            for principle in principles:
                if principle and principle != "None":
                    output.append({'book_title': book_title, 'heading': heading, 'principle': principle.strip(), 'snippets': snippets})

      
with open('test_output.csv', 'w', newline='') as csvfile:
    fieldnames = ['book_title', 'heading', 'principle', 'snippets']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(output)