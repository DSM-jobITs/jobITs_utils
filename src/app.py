from pdfminer.high_level import extract_text

from src.functions import Extractor

CHECKBOX = '□'
PATH = './../files/update.pdf'
text = extract_text(PATH)

text = "\n".join(text.split('\n')[::2])

if __name__ == '__main__':
    ext = Extractor(text)

    personnel = ext.get_count_of_people(0)
    company_name = ext.get_company_name(4)
    business_number = ext.get_business_number(5)
    company_phone = ext.get_company_phone(7)
    establish_date = ext.get_establish_date(10)
    sales = ext.get_sales(11)
    workers = ext.get_count_of_workers(13)
    company_description = ext.get_company_description(15)
    work_detail = ext.get_work_detail(17)
    industry_type = ext.get_industry_type(20)
    main_product = ext.get_main_product(21)
    address = ext.get_address(22)
    manager_phone = ext.get_manager_phone(31)
    certificate = ext.get_certificate(33)
    grade = ext.get_grade(34)
    stack = ext.get_stack(35)
    start_time, end_time = ext.get_working_time(42)
    money = ext.get_money(45)
    training_period = ext.get_training_period(51)
    document = ext.get_document(55)

    for line in ext.get_text():
        print(line)

    print('\n###########################################################\n')

    print("모집인원 :", personnel)
    print("업체명 :", company_name)
    print("사업자번호 :", business_number)
    print("전화번호 :", company_phone)
    print("설립일자 :", establish_date)
    print("매출액 :", sales)
    print("근로자수 :", workers)
    print("회사소개 :", company_description)
    print("업무내용 :", work_detail)
    print("업종형태 :", industry_type)
    print("주력상품 :", main_product)
    print("주소 :", address)
    print("담당자 연락처 :", manager_phone)
    print("자격증 :", certificate)
    print("성적 :", grade)
    print("특기사항 :", stack)
    print(f"근무시간 : {start_time} ~ {end_time}", )
    print("실습기간 급여 :", money)
    print("실습기간 :", training_period)
    print("구비서류 :", document)
