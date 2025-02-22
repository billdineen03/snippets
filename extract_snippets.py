import json, csv, sys
import pandas as pd
with open(sys.argv[1]) as file:
    data = json.load(file)['assignments']

book_titles = [guide['source'] for guide in data]

def flatten_dict(dict: dict):
    output = [{'heading': dict['heading'], 'snippets': dict['snippets']}]
    if dict['children']:
        children = []
        for child in dict['children']:
            children.extend(flatten_dict(child))
        output.extend(children)
    return output
    
def flatten_headings(headings: list):
    output = []
    for heading in headings:
        output.extend(flatten_dict(heading))
    return output

def flatten_data(data: list):
    output = []
    for guide in data:
        output.append(flatten_headings(guide['headings']))
    return output

def export_to_csv(dicts: list, id, book_title):
    with open(f"{book_title}.csv", 'w', newline = '', errors='ignore') as csvfile:
        fieldnames = ['book_title', 'heading', 'snippets']
        writer = csv.DictWriter(csvfile, fieldnames = fieldnames, restval=book_title)
        writer.writeheader()
        writer.writerows(dicts)
        
def remove_punctuation(word):
    def is_alphanumsp(c): return c.isalnum() or c == ' '
    filtered = [c for c in word if is_alphanumsp(c)]
    return ''.join(filtered)

for id, guide in enumerate(output):
    book_title = remove_punctuation(book_titles[id])
    export_to_csv(guide, id, book_title)
    with open(f"{book_title}.csv") as f:
        df = pd.read_csv(f)
        df['principles'] = ''
        df['optional_comments'] = ''
        df['valid?'] = ''
        df['review_comments'] = ''
        df['suggested_alternative'] = ''
        df.to_csv(f"{book_title}.csv", index=False)