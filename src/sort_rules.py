minconf = 0.5

def clean_sort_rules(filepath: str, output_filepath: str):
    lines = []
    with open(filepath) as f:
        for line in f:
            conf = float(line.split()[-1])
            if conf < minconf:
                continue
            part1 = line.split('->')[0]
            part2 = line.split('->')[1]
            ignore = False
            if 'vehicle_type:Car' in part1:
                if 'casualty_type:Car' in part2:
                    continue
            if 'vehicle_type:Motorcycle' in part1:
                if 'casualty_type:Motorcycle' in part2:
                    continue
            if 'casualty_class:Pedestrian' in part1:
                if 'casualty_type:Sidewalk User' in part2 or 'casualty_type:Pedestrian' in part2:
                    continue
            if 'sex_of_driver:Male' in part1:
                if 'sex_of_casualty:Male' in part2:
                    continue
            if 'age_band_of_driver:Youth' in part1:
                if 'age_band_of_casualty:Youth' in part2:
                    continue
            if 'age_band_of_driver:Adult' in part1:
                if 'age_band_of_casualty:Adult' in part2:
                    continue
            if 'accident_severity:Slight' in part1:
                if 'casualty_severity:Slight' in part2:
                    continue
            if not ignore:
                lines.append(line)
    lines = sorted(lines, key=lambda x: float(x.split()[-1]), reverse=True)

    with open(output_filepath, "w") as text_file:
        for line in lines:
            text_file.write(line)
    print('done!')

for type in ['all', 'serious', 'fatal']:
    clean_sort_rules(f'../result/rules/{type}_accident_rules.txt', f'../result/rules/{type}_accident_rules_sorted_reduced.txt')