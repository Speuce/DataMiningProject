def clean_sort_itemsets(filepath: str, output_filepath: str):
    rules = 0
    duplicates = 0
    lines = []
    with open(filepath) as f:
        for line in f:
            if line in lines:
                duplicates += 1
            else:
                lines.append(line)
                rules += 1
    print(f'Found {rules} frequent itemsets with {duplicates} duplicates')
    lines.sort()
    lines = sorted(lines, key=lambda x: int(x.split('|')[1]))
    with open(output_filepath, "w") as text_file:
        for line in lines:
            text_file.write(line)
    print('done!')


clean_sort_itemsets('output.txt', 'sorted_by_count.txt')
