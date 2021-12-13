def clean_sort_itemsets(filepath: str, output_filepath: str, bycount: bool = False):
    rules = 0
    duplicates = 0
    prefixes = []
    lines = []
    counts = []
    with open(filepath) as f:
        for line in f:
            prefix = line.split('|')[0]
            count = int(line.split('|')[1])
            index = -1
            try:
                index = prefixes.index(prefix)
            except ValueError:
                pass
            if index != -1:
                if count < counts[index]:
                    lines[index] = line
                    counts[index] = count
                duplicates += 1
            else:
                lines.append(line)
                prefixes.append(prefix)
                counts.append(count)
                rules += 1
    print(f'Found {rules} frequent itemsets with {duplicates} duplicates')
    lines.sort()

    if bycount:
        lines = sorted(lines, key=lambda x: int(x.split('|')[1]))

    with open(output_filepath, "w") as text_file:
        for line in lines:
            text_file.write(line)
    print('done!')

clean_sort_itemsets(f'../result/log/log_all_accidents.log', f'../result/all_accidents.txt')
clean_sort_itemsets(f'../result/log/log_all_accidents.log', f'../result/all_accidents_bycount.txt', True)
