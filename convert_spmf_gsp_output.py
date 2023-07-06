from types import NoneType


def mapping_of(v):
    if v == 'user_login':
        return 'a'
    if v == 'view_lecture':
        return 'b'
    if v == 'watch_video_lecture':
        return 'c'
    if v == 'download_handout':
        return 'd'
    if v == 'attemp_quiz':
        return 'e'
    if v == 'view_Quiz_List':
        return 'f'
    if v == 'view_progress':
        return 'g'
    if v == 'view_assignment':
        return 'h'
    if v == 'view_announcements':
        return 'i'
    if v == 'user_logout':
        return 'j'


def main():
    file_output_spmfgsp = open("output_spmfgsp.txt", "r")
    lines = file_output_spmfgsp.readlines()
    count = 0
    outputs = ""
    add_support_value = True
    add_line_number = False
    for line in lines:
        count += 1
        line_values = line.split('|')
        output = ""
        for line_value in line_values:
            if line_value.strip().startswith("#SUP:"):
                support_line = line_value.strip()
                # print('Support and SIDs: ', support_line)
                support = support_line.split(":")[1].strip().split(' ')[0].strip()
                # print(support)
            else:
                line_value = line_value.strip()
                line_value_items = line_value.split(' ')
                if len(output) > 0:
                    output = output + ", "
                output = output + "<("
                if len(line_value_items) == 1:
                    v = mapping_of(line_value_items[0])
                    # print(v, ',', line_value_items)
                    output = output + v
                    output = output + ")>"
                else:
                    for line_value_item in line_value_items:
                        # print(line_value_item)
                        v = mapping_of(line_value_item)
                        output = output + v + ", "
                    output = output.rstrip(' ').rstrip(',')
                    output = output + ")>"
        if add_line_number:
            outputs = outputs + str(count) + ": " + output + '\n'
        else:
            if add_support_value:
                s = round(float(support) / float(456.0), 2)
                outputs = outputs + str(s) + ":\t" + output + '\n'
            else:
                outputs = outputs + output + '\n'
    file_output_spmfgsp.close()
    print(outputs)


if __name__ == "__main__":
    main()
