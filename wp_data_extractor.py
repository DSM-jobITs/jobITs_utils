import olefile
import re

FILE_PATH = './files/2020.hwp'

###############################
# Text 에서 필요한 내용을 추출하기 위한 문자열을 자르고 나누고 값을 얻기 위한 깔끔한 코드를 완성해야 한다.
# 확장성은 떨어질 수 밖에 없기에 정확성과 코드의 깔끔함을 최우선으로 생각해야 한다.
###############################


def remove_first_line(string):
    return remove_line(string, 0, 1)


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

    def get_count_of_people(self, txt):
        txt = remove_all_blank(txt)
        count = 0
        nums = get_array_between_chars(txt, '(', ')')
        for number in nums:
            num = get_char_between_chars(number, '(', ')')
            count += int(num) if num else 0
        return count

    def get_company_name(self, txt):
        txt = remove_all_blank(txt)
        txt = get_array_between_chars(txt, '<', '>')
        name = get_char_between_chars(txt[2], '<', '>')
        name = name[:name.find('(')]
        return name

    def get_company_number(self, txt):
        txt = remove_all_blank(txt)
        txt = get_array_between_chars(txt, '<', '>')
        txt = get_char_between_chars(txt[4], '<', '>')
        number = txt[txt.find(':')+1:txt.find('팩')]
        return number

    def get_company_company_setup_date(self, txt):
        txt = remove_all_blank(txt)
        txt = get_array_between_chars(txt, '<', '>')
        date = get_char_between_chars(txt[2], '<', '>')

        return date

    def get_company_annual_sales(self, txt):
        txt = remove_all_blank(txt)
        txt = get_array_between_chars(txt, '<', '>')
        sales = get_char_between_chars(txt[4], '<', '>')
        return sales

    def get_company_count_of_workers(self, txt):
        txt = remove_all_blank(txt)
        txt = get_array_between_chars(txt, '<', '>')
        sales = get_char_between_chars(txt[6], '<', '>')
        return sales

if __name__ == '__main__':

    f = olefile.OleFileIO(FILE_PATH)  # HWP file 열기

    en_text = f.openstream('PrvText').read()  # text 꺼내기 (유니코드 상태임)
    de_text = en_text.decode('UTF-16')  # 유니코드를 UTF-16으로 디코딩한다. (utf-8 은 불가하다)

    text = remove_line(de_text, 0, 6)
    text = text.split('\n')

    ext = Extractor()

    count_of_people = ext.get_count_of_people(text[0])  # 모집인원
    company_name = ext.get_company_name(text[1])  # 업체명
    company_number = ext.get_company_number(text[1])  # 연락처
    company_setup_date = ext.get_company_company_setup_date(text[2])  # 설립일자
    company_annual_sales = ext.get_company_annual_sales(text[2])  # 연매출액
    company_count_of_workers = ext.get_company_count_of_workers(text[2])  # 근로자수

    print(count_of_people)  # 모집인원
    print(company_name)  # 업체명
    print(company_number)  # 연락처
    print(company_setup_date)  # 설립일자
    print(company_annual_sales)  # 연매출액
    print(company_count_of_workers)  # 근로자수

    # 0. 모집인원
    # 1. 업체명, 연락처
    # 2. 설립일자, 연매출액, 근로자수

    # 3. 회사소개
    # 4. 업무내용, 업종형태, 주력상품
    # 5. 주소
    # 6. 기업위치, 담당자 성명, 핸드폰, 버스노선, E-mail
    # 7. 자격요건 (자격증, 성적, 특기사항)
    # 8. 근무조건
    # 9. 구비서류, 면접희망, 근무희망
    # 10. 실습 ???
