def clean_sort_rules(filepath: str, output_filepath: str):
    lines = []
    with open(filepath) as f:
        for line in f:
            lines.append(line)
    lines = sorted(lines, key=lambda x: float(x.split()[-1]), reverse=True)

    with open(output_filepath, "w") as text_file:
        for line in lines:
            text_file.write(line)
    print('done!')

for type in ['all', 'serious', 'fatal']:
    clean_sort_rules(f'../result/rules/{type}_accident_rules.txt', f'../result/rules/{type}_accident_rules_sorted.txt')
