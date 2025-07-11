import json, csv, sys, os, datetime
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

def export_to_csv(dicts: list, book_title):
    with open(f"{book_title}.csv", 'w', newline = '', errors='ignore') as csvfile:
        fieldnames = ['book_title', 'heading', 'snippets']
        writer = csv.DictWriter(csvfile, fieldnames = fieldnames, restval=book_title)
        writer.writeheader()
        writer.writerows(dicts)
        
def remove_punctuation(word):
    def is_alphanumsp(c): return c.isalnum() or c == ' '
    filtered = [c for c in word if is_alphanumsp(c)]
    return ''.join(filtered)

output = flatten_data(data)

for id, guide in enumerate(output):
    book_title = remove_punctuation(book_titles[id])
    file_name = f"{book_title}.csv"
    export_to_csv(guide, book_title)
    with open(file_name) as f:
        df = pd.read_csv(f)
        df['main_idea'] = ''
        df['definitions'] = ''
        df['explanations'] = ''
        df['actionables'] = ''
        df['optional_comments'] = ''
        df['valid_main_idea?'] = ''
        df['valid_definitions?'] = ''
        df['valid_explanations?'] = ''
        df['valid_actionables?'] = ''
        df['review_comments'] = ''
        df['alt_main_idea'] = ''    
        df['alt_definitions'] = ''
        df['alt_explanations'] = ''
        df['alt_actionables'] = ''
        row_count = df.shape[0] - 1
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
    if row_count >= 20:
        breakpoint = round(row_count / 2)
        df[:breakpoint].to_csv(f"{book_title}_a {timestamp}.csv", index=False)
        df[breakpoint:].to_csv(f"{book_title}_b {timestamp}.csv", index=False)
    else:
        df.to_csv(f"{file_name} {timestamp}.csv", index=False)
    os.remove(file_name)
