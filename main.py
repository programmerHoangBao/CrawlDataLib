from service.RequestWebsite import CrawlData
import service.JsonService as JsonService
import service.MongodbService as MongodbService

def main():
    url = "https://dichvucong.gov.vn/p/home/dvc-cau-hoi-pho-bien.html"
    next_click_xpath = "/html/body/div[5]/div/div/div[5]/div[2]/ul/li[8]/a"
    selector_div_link_question = "#tatCa > div:nth-child(1)"
    selector_question = "h1.main-title-sub"
    selector_answer = ".article > p:nth-child(3)"
    base_url = "https://dichvucong.gov.vn"
    uri = "mongodb+srv://bao:123@cluster0.vkixc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    database_name = "DichVuCong"
    collection_name = "Question"
    file_path = "./Big_Data/Crawl_Data/Data/DichVuCong.json"
    total_page = 2
    current_page = 1
    page_source = None
    link_questions = []
    list_question = []

    for page in range(1, total_page+1):
        if current_page != 1:
            page_source = CrawlData.simulate_click_XPATH(URL=url, XPATH=next_click_xpath)
        else:
            page_source = CrawlData.get_page_source_selenium(url)

        if page_source is not None:
            list_selector_a = CrawlData.get_child_selectors(page_source, selector_div_link_question)
            for selector_a in list_selector_a:
                set_href = CrawlData.get_attribute_value(page_source, selector_a, attribute="href", base_url=base_url)
                for link in set_href:
                    link_questions.append(link)
            
            for link_question in link_questions:
                question = CrawlData.get_attribute_value_with_selenium(url=link_question, selector=selector_question)
                answer = CrawlData.get_attribute_value_with_selenium(url=link_question, selector=selector_answer)
                list_question.append({"question": question.pop(), "answer": answer.pop()})

    if len(list_question) != 0:
        JsonService.overwrite_data_to_json(data=list_question, dir_path="./Big_Data/Crawl_Data/Data", file_name="DichVuCong.json")
    else:
        print("No data!")
    if (JsonService.json_file_exists(file_path)):
        MongodbService.upload_json_to_mongodb(uri=uri, database_name=database_name, collection_name=collection_name, file_path=file_path)

if __name__ == "__main__":
    main()


                
        
