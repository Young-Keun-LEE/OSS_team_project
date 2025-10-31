import scrapy
import re


class MjuNoticeSpider(scrapy.Spider):
    name = "mju_notice"
    start_urls = [
        "https://www.mju.ac.kr/mjukr/255/subview.do"
    ]

    def parse(self, response):
        # 제목 셀 안의 <a> 요소들을 선택합니다.
        notice_links = response.css("td._artclTdTitle a")

        date_regex = re.compile(r"(\d{4}[-./]\d{1,2}[-./]\d{1,2})|\d{4}\s*년\s*\d{1,2}\s*월\s*\d{1,2}\s*일")

        for notice in notice_links:
            # 제목 안전 추출
            title = notice.css("strong::text").get()
            if title:
                title = title.strip()
            else:
                title = notice.xpath("normalize-space(string(.))").get() or ""

            # 링크 추출
            link = notice.attrib.get('href') or notice.css('::attr(href)').get()
            absolute_link = response.urljoin(link) if link else ""

            # 날짜 추출: 여러 후보 텍스트에서 날짜 패턴을 찾음
            tr = notice.xpath("ancestor::tr[1]")
            candidates = []

            # 1) 바로 옆 td들 (다음 td, 다음다음 td, 마지막 td)
            for idx in (1, 2):
                texts = notice.xpath(f"ancestor::td[1]/following-sibling::td[{idx}]//text()").getall()
                candidates.extend([t.strip() for t in texts if t and t.strip()])
            last_texts = notice.xpath("ancestor::td[1]/parent::tr/td[last()]//text()").getall()
            candidates.extend([t.strip() for t in last_texts if t and t.strip()])

            # 2) fallback: tr 내부 모든 텍스트
            if not candidates:
                candidates = [t.strip() for t in tr.xpath('.//td//text()').getall() if t and t.strip()]

            found_date = ""
            for t in candidates:
                m = date_regex.search(t)
                if m:
                    found_date = m.group(0)
                    break

            yield {
                'title': title,
                'link': absolute_link,
                'date': found_date,
            }