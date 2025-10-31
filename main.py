import subprocess
import json
import os

def main():
    """
    이 스크립트의 메인 함수입니다.
    Scrapy crawl 명령어를 실행하고, 그 결과를 읽어 터미널에 출력합니다.
    """
    output_file = 'notices.json'
    spider_name = 'mju_notice' # mju_spider.py에 정의된 name

    print("📢 명지대학교 공지사항 크롤링을 시작합니다...")

    # 이전에 생성된 결과 파일이 있다면 삭제
    if os.path.exists(output_file):
        os.remove(output_file)

    # Scrapy crawl 명령어를 터미널에서 실행하는 것과 동일한 효과
    # 한글 깨짐 방지 옵션을 여기에 모두 포함
    command = [
        "scrapy", "crawl", spider_name,
        "-o", output_file,
        "-s", "FEED_EXPORT_ENCODING=utf-8",
        "-s", "FEED_EXPORT_OPTIONS={'ensure_ascii': False}"
    ]
    
    # subprocess를 사용해 명령어를 실행하고, 완료될 때까지 기다립니다.
    # capture_output=True는 실행 결과를 변수로 받기 위함입니다.
    result = subprocess.run(command, capture_output=True, text=True)

    # 명령어 실행 중 에러가 발생했는지 확인
    if result.returncode != 0:
        print("❌ 크롤링 중 에러가 발생했습니다.")
        print("에러 내용:")
        print(result.stderr) # 에러 내용을 터미널에 출력
        return

    # 결과 파일이 생성되었는지 확인
    if not os.path.exists(output_file):
        print("❌ 크롤링은 성공했으나 결과 파일이 생성되지 않았습니다.")
        return
        
    # 결과 파일을 읽어서 notices 변수에 저장
    with open(output_file, 'r', encoding='utf-8') as f:
        notices = json.load(f)
    
    # 사용이 끝난 임시 파일 삭제
    os.remove(output_file)

    if not notices:
        print("❌ 새로운 공지사항을 가져오지 못했습니다.")
        return

    print("✅ 크롤링 완료! 최신 공지사항 10개는 다음과 같습니다.")
    print("-" * 50)
    
    for i, notice in enumerate(notices[:10]):
        print(f"[{i+1:02d}] {notice.get('title', '제목 없음')}")
        
    print("-" * 50)

if __name__ == "__main__":
    main()