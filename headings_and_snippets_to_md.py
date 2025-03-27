#input = csv with headings: 
    # book_title	
    # heading	
    # snippets	
    # main_idea	
    # definitions	
    # explanations	
    # actionables	
    # optional_comments	
    # valid_main_idea?	
    # valid_definitions?	
    # valid_explanations?	
    # valid_actionables?	
    # review_comments	
    # alt_main_idea	alt_definitions	
    # alt_explanations	
    # alt_actionables

# I want the file_name.csv as file_name.md
# then for each row after the first:
# row[1] is the heading
# row[2] is the snippets

#def export_md(csv_file):

import sys, csv
with open(sys.argv[1]) as csv_file:
    file_name = sys.argv[1][0:-4]
    reader = csv.reader(csv_file)
    with open(f'{file_name}.md', 'w') as markdown_file:
        for i, row in enumerate(reader):
            if i == 0:
                continue
            markdown_file.write('# heading: ' + row[1] + '\n\n')
            snippets = row[2].split('",')
            for i, snippet in enumerate(snippets):
                markdown_file.write(f'## snippet {i+1}:\n\n' + snippet.replace('\\n', '\n') + '\n\n')