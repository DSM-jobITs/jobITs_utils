import re


def divide_string(string, char):
    idx = string.find(char)
    return string[:idx], string[idx+1:]


def remove_all_blank(string):
    return string.replace(' ', '')


def remove_line(string, start_index, cnt):
    sliced_list = string.split('\n')
    removed_list = sliced_list[:start_index] + sliced_list[start_index + cnt:]
    return "\n".join(removed_list)


def get_char_between_chars(string, front_char, behind_char):
    regex = re.compile('{}(.*){}'.format(re.escape(front_char), re.escape(behind_char)))
    return "".join(regex.findall(string))


def get_array_between_chars(string, front_char, behind_char):
    arr = []
    while string:
        f_idx = string.find(front_char)
        b_idx = string.find(behind_char)
        if f_idx == -1 or b_idx == -1:
            arr.append(string)
            break
        arr.append(string[f_idx:b_idx+1])
        string = string[b_idx+1:]
    return arr


class Extractor:

    def __init__(self, txt):
        self.txt: list = remove_line(txt, 0, 4).split('\n')

    def get_text(self):
        return self.txt

    def get_count_of_people(self, i):
        txt = remove_all_blank(self.txt[i])
        count = 0
        nums = get_array_between_chars(txt, '(', ')')
        for number in nums:
            num = get_char_between_chars(number, '(', ')')
            count += int(num) if num else 0
        return count

    def get_company_name(self, i):
        return remove_all_blank(self.txt[i])

    def get_business_number(self, i):
        return get_char_between_chars(self.txt[i], '(', ')')

    def get_company_phone(self, i):
        txt = remove_all_blank(self.txt[i])
        front_phone = get_char_between_chars(txt, '(', ')')
        middle_phone = get_char_between_chars(txt, ')', '-')
        back_phone = get_char_between_chars(txt, '-', '')
        return f'{front_phone}-{middle_phone}-{back_phone}'

    def get_establish_date(self, i):
        txt = remove_all_blank(self.txt[i])
        year = get_char_between_chars(txt, '', '년')
        month = get_char_between_chars(txt, '년', '월')
        day = get_char_between_chars(txt, '월', '일')

        return f'{year}-{month}-{day}'

    def get_sales(self, i):
        return self.txt[i]

    def get_count_of_workers(self, i):
        txt = self.txt[i]
        return txt[:txt.find('명')]

    def get_company_description(self, i):
        txt = self.txt[i]
        txt_list = txt.split('\n')

        arr = map(lambda line: " ".join(line.split()), txt_list)

        return "\n".join(arr)

    def get_work_detail(self, i):
        txt = self.txt[i]
        txt_list = txt.split('\n')

        arr = map(lambda line: " ".join(line.split()), txt_list)

        return "\n".join(arr)

    def get_industry_type(self, i):
        return remove_all_blank(self.txt[i])

    def get_main_product(self, i):
        return remove_all_blank(self.txt[i])

    def get_address(self, i):
        txt = self.txt[i]
        return " ".join(txt[txt.find('소')+1:].split())

    def get_manager_phone(self, i):
        txt = self.txt[i]
        txt = remove_all_blank(txt.replace('-', ''))
        return txt[txt.find(':')+1:]

    def get_certificate(self, i):
        return remove_all_blank(self.txt[i])

    def get_grade(self, i):
        txt = self.txt[i]
        return txt[:txt.find('%')]

    def get_stack(self, i):
        return " ".join(self.txt[i].split())

    def get_working_time(self, i):
        txt = remove_all_blank(self.txt[i])
        start = txt[:txt.find('~')]
        end = txt[txt.find('~')+1:txt.find('까지')]
        return start, end

    def get_money(self, i):
        txt = remove_all_blank(self.txt[i])
        return txt[txt.find('(실습기간)')+6:-1]

    def get_training_period(self, i):
        return self.txt[i][:-2]

    def get_document(self, i):
        return " ".join(self.txt[i].split())
