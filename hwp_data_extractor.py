import olefile
import os
import re
from flask import Flask, request
from werkzeug.utils import secure_filename

UPLOAD_PATH = './files/'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_PATH


def remove_first_line(string):
    return remove_line(string, 0, 1)


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
        self.txt: list = remove_line(txt, 0, 6).split('\n')

    def get_count_of_people(self, i):
        txt = remove_all_blank(self.txt[i])
        count = 0
        nums = get_array_between_chars(txt, '(', ')')
        for number in nums:
            num = get_char_between_chars(number, '(', ')')
            count += int(num) if num else 0
        return count

    def get_company_name(self, i):
        txt = remove_all_blank(self.txt[i])
        txt = get_array_between_chars(txt, '<', '>')
        name = get_char_between_chars(txt[2], '<', '>')
        name = name[:name.find('(')]
        return name

    def get_company_number(self, i):
        txt = remove_all_blank(self.txt[i])
        txt = get_array_between_chars(txt, '<', '>')
        txt = get_char_between_chars(txt[4], '<', '>')
        number = txt[txt.find(':')+1:txt.find('팩')]
        return number

    def get_company_company_setup_date(self, i):
        txt = remove_all_blank(self.txt[i])
        txt = get_array_between_chars(txt, '<', '>')
        date = get_char_between_chars(txt[2], '<', '>')

        return date

    def get_company_annual_sales(self, i):
        txt = remove_all_blank(self.txt[i])
        txt = get_array_between_chars(txt, '<', '>')
        sales = get_char_between_chars(txt[4], '<', '>')
        return sales[:-1]

    def get_company_count_of_workers(self, i):
        txt = remove_all_blank(self.txt[i])
        txt = get_array_between_chars(txt, '<', '>')
        sales = get_char_between_chars(txt[6], '<', '>')
        return sales[:-1]

    def get_company_description(self, i):
        txt = get_array_between_chars(self.txt[i], '<', '>')
        description = get_char_between_chars(txt[2], '<', '>')
        return description

    def get_business_information(self, i):
        txt = get_array_between_chars(self.txt[i], '<', '>')
        information = get_char_between_chars(txt[2], '<', '>')
        return information

    def get_business_type(self, i):
        txt = get_array_between_chars(self.txt[i], '<', '>')
        type = get_char_between_chars(txt[4], '<', '>')
        return type

    def get_main_product(self, i):
        txt = get_array_between_chars(self.txt[i], '<', '>')
        type = get_char_between_chars(txt[6], '<', '>')
        return type

    def get_address(self, i):
        txt = get_array_between_chars(self.txt[i], '<', '>')
        address = get_char_between_chars(txt[2], '<', '>')
        address = ' '.join(address.split())
        return address

    def get_certificate(self, i):
        txt = get_array_between_chars(self.txt[i], '<', '>')
        certificate = get_char_between_chars(txt[3], '<', '>')
        return certificate

    def get_grade(self, i):
        txt = get_array_between_chars(self.txt[i], '<', '>')
        grade = get_char_between_chars(txt[5], '<', '>')
        return remove_all_blank(grade)

    def get_stack(self, i):
        txt = get_array_between_chars(self.txt[i], '<', '>')
        stack = get_char_between_chars(txt[7], '<', '>')
        return stack

    def get_working_time(self, i):
        txt = get_array_between_chars(self.txt[i], '<', '>')
        start, end = divide_string(remove_all_blank(txt[3]), '~')
        start = get_char_between_chars(start, '<', '시')
        end = get_char_between_chars(end, '', '시')
        return start, end

    def get_working_date(self, i):
        txt = get_array_between_chars(self.txt[i], '<', '>')
        money = get_char_between_chars(txt[7], '(실습기간)', '(정식)')
        return remove_all_blank(money)[:-1]


def init(file_path):

    f = olefile.OleFileIO(file_path)  # HWP file 열기

    en_text = f.openstream('PrvText').read()  # text 꺼내기 (유니코드 상태임)
    de_text = en_text.decode('UTF-16')  # 유니코드를 UTF-16으로 디코딩한다. (utf-8 은 불가능)

    f.close()

    ext = Extractor(de_text)

    count_of_people = ext.get_count_of_people(0)  # 모집인원
    company_name = ext.get_company_name(1)  # 업체명
    company_number = ext.get_company_number(1)
    company_setup_date = ext.get_company_company_setup_date(2)  # 설립일자
    company_annual_sales = ext.get_company_annual_sales(2)  # 연매출액
    company_count_of_workers = ext.get_company_count_of_workers(2)  # 근로자수
    company_description = ext.get_company_description(3)  # 회사소개
    business_information = ext.get_business_information(4)  # 업무내용
    business_type = ext.get_business_type(4)  # 업종형태
    main_product = ext.get_main_product(4)  # 주력상품
    address = ext.get_address(5)
    certificate = ext.get_certificate(6)
    grade = ext.get_grade(7)
    stack = ext.get_stack(7)
    start_time, end_time = ext.get_working_time(8)
    money = ext.get_working_date(8)

    print(count_of_people)  # 모집인원
    print(company_name)  # 업체명
    print(company_number)  # 연락처
    print(company_setup_date)  # 설립일자
    print(company_annual_sales)  # 연매출액
    print(company_count_of_workers)  # 근로자수
    print(company_description)  # 회사소개
    print(business_information + ' / ' + business_type + ' / ' + main_product)  # 업무내용, 업종형태, 주력상품
    print(address)  # 주소
    print(certificate + ' / ' + grade + ' / ' + stack)  # 자격증, 성적, 특기사항
    print(start_time + ' / ' + end_time + ' / ', money)  # 근무시간, 실습기간 중 급여
    # print()  # 구비서류, 면접희망, 근무희망
    # print()  # 접수일자, 마감일자
    # print(de_text)
    return {

    }


@app.route('/extractor', methods=['POST'])
def extractor():
    file = request.files['file']
    filename = secure_filename(file.filename)
    _ = file.save(UPLOAD_PATH + filename)
    file_path = f'{UPLOAD_PATH}{filename}'

    json_data = init(file_path)
    os.remove(file_path)
    return json_data


if __name__ == '__main__':
    app.run()
    # 0. 모집인원
    # 1. 업체명, 연락처
    # 2. 설립일자, 연매출액, 근로자수
    # 3. 회사소개
    # 4. 업무내용, 업종형태, 주력상품
    # 5. 주소
    # 6. 기업위치
    # 7. 자격요건 (자격증, 성적, 특기사항)

    # 8. 근무조건
    # 9. 구비서류, 면접희망, 근무희망
    # 10. 실습 ???
