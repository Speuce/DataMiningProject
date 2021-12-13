minconf = 0.5


def clean_sort_rules(filepath: str, output_filepath: str, type: str):
    lines = []
    allitems = set()
    with open(filepath) as f:
        for line in f.readlines():
            # conf = float(line.split()[-1])
            # if conf < minconf:
            #     continue
            part1 = line.split('|')[0]
            items = set([st.split(':')[0] for st in part1.strip(',').split(',')])
            allitems = allitems.union(items)
            # ignore = False
            # oneRuleRight = len(part2.split(",")) == 2
            # if type == 'serious':
            #     if 'casualty_severity:Serious' in part2 and oneRuleRight:
            #         continue
            # if type == 'Fatal':
            #     if oneRuleRight and 'casualty_severity:Fatal' in part2:
            #         continue
            # if oneRuleRight and 'driver_home_area_type:Urban area' in part2:
            #     continue
            # if oneRuleRight and 'casualty_type:Car' in part2:
            #     continue
            # if oneRuleRight and ('sex_of_casualty:Male' in part2 or 'sex_of_driver:Male' in part2):
            #     continue
            # if 'vehicle_type:Car' in part1:
            #     if 'casualty_type:Car' in part2:
            #         continue
            # if 'vehicle_type:Motorcycle' in part1:
            #     if 'casualty_type:Motorcycle' in part2:
            #         continue
            # if 'casualty_class:Pedestrian' in part1:
            #     if 'casualty_type:Sidewalk User' in part2 or 'casualty_type:Pedestrian' in part2:
            #         continue
            # if 'sex_of_driver:Male' in part1:
            #     if 'sex_of_casualty:Male' in part2:
            #         continue
            # if 'age_band_of_driver:Youth' in part1:
            #     if 'age_band_of_casualty:Youth' in part2:
            #         continue
            # if 'age_band_of_driver:Adult' in part1:
            #     if 'age_band_of_casualty:Adult' in part2:
            #         continue
            # if 'accident_severity:Slight' in part1:
            #     if 'casualty_severity:Slight' in part2:
            #         continue
            # if not ignore:
            # lines.append(line)
    # lines = sorted(lines, key=lambda x: float(x.split()[-1]), reverse=True)
    allitems = sorted(list(allitems))
    with open(output_filepath, "w") as text_file:
        for line in allitems:
            text_file.write(f'{line}\n')
    print('done!')

clean_sort_rules(f'../result/all_accidents.txt', f'../keys.txt', "no")
