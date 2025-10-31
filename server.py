import os
import sys
import json
from fastmcp import FastMCP
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

mcp = FastMCP("mju_notice_crawler")

# --- 이 부분은 Scrapy를 파이썬 스크립트에서 반복 실행할 때 필요합니다 ---
if 'twisted.internet.reactor' in sys.modules:
    del sys.modules['twisted.internet.reactor']
os.environ['TWISTED_REACTOR'] = 'asyncio'
# ---

@mcp.tool
def main():
    """
    Scrapy 크롤러를 파이썬 내부에서 직접 실행하고,
    그 결과를 읽어 터미널에 출력합니다.
    """
    output_file = 'notice.json'

    print("📢 명지대학교 공지사항 크롤링을 시작합니다... (출력: notice.json)")

    # 이전에 생성된 결과 파일이 있다면 삭제
    if os.path.exists(output_file):
        os.remove(output_file)

    # Scrapy 프로젝트의 설정을 불러옵니다. (mju_crawler/settings.py)
    settings = get_project_settings()
    
    # 결과 파일을 저장하기 위한 설정을 코드에서 직접 추가합니다.
    # 한글 깨짐 방지 옵션을 모두 포함합니다.
    settings.set('FEEDS', {
        output_file: {
            'format': 'json',
            'encoding': 'utf8',
            'store_empty': False,
            'fields': None,
            'indent': 4,
            'ensure_ascii': False,
        }
    })
    # 불필요한 로그를 줄여 결과만 깔끔하게 보이도록 설정
    settings.set('LOG_LEVEL', 'ERROR')

    # 크롤러 실행을 위한 프로세스를 설정합니다.
    process = CrawlerProcess(settings)
    
    # 실행할 스파이더의 이름을 지정합니다. (mju_spider.py의 name)
    process.crawl('mju_notice')
    
    # 크롤링이 끝날 때까지 스크립트 실행을 여기서 멈추고 기다립니다.
    process.start()
    
    # --- 크롤링 완료 ---
    if not os.path.exists(output_file):
        print("❌ 크롤링은 완료되었으나 결과 파일을 찾을 수 없습니다.")
        return

    print(f"✅ 크롤링 완료! 결과가 '{output_file}'에 저장되었습니다.")
    print("각 항목은 'title', 'link', 'date' 필드를 포함합니다.")

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0",port=8000)