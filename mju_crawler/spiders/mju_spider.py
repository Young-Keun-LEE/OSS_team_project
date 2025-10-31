import scrapy

class MjuNoticeSpider(scrapy.Spider):
    name = "mju_notice"
    start_urls = [
        "https://www.mju.ac.kr/mjukr/255/subview.do"
    ]

    def parse(self, response):
        # 1. response.css()를 사용하여 페이지의 HTML에서 원하는 부분을 선택합니다.
        #    '_artclTdTitle' 클래스를 가진 <td> 요소 안의 <a> 태그를 모두 선택합니다.
        notice_links = response.css("td._artclTdTitle a")

        # 2. 선택된 모든 <a> 태그에 대해 반복문을 실행합니다.
        for notice in notice_links:
            # 3. 각 <a> 태그(notice) 안에서 추가로 CSS 선택자를 사용하여 데이터를 추출합니다.
            
            # 제목(title) 추출: <a> 태그 안의 <strong> 태그에 있는 텍스트를 가져옵니다.
            # ::text는 태그 내부의 텍스트 노드를 의미합니다.
            # .get()은 선택된 결과 중 첫 번째 항목을 문자열로 반환합니다.
            # .strip()은 텍스트 양옆의 불필요한 공백을 제거합니다.
            title = notice.css("strong::text").get().strip()
            
            # 링크(link) 추출: <a> 태그의 'href' 속성 값을 가져옵니다.
            # ::attr(href)는 href 속성을 의미합니다.
            link = notice.attrib['href'] # 또는 notice.css('::attr(href)').get()
            
            # 4. 상대 경로를 절대 경로로 변환합니다.
            #    예: '/bbs/.../artclView.do' -> 'https://www.mju.ac.kr/bbs/.../artclView.do'
            absolute_link = response.urljoin(link)

            # 5. 추출된 데이터를 딕셔너리 형태로 `yield` 합니다.
            #    `yield`는 Scrapy 엔진에 "데이터 항목 하나를 찾았다"고 알려주는 역할을 합니다.
            #    Scrapy는 이렇게 yield된 딕셔너리들을 모아서 파일로 저장하거나 다른 처리를 합니다.
            yield {
                'title': title,
                'link': absolute_link,
            }