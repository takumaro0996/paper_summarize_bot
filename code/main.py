import os
import base64
import httpx
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import arxiv
import google.generativeai as genai
import random
import datetime
import functions_framework
from const import GENERATION_CONFIG, THEME_QUERYS, PROMPT

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))

@functions_framework.cloud_event
def main(cloud_event):

    # 現在の曜日を取得
    current_day = datetime.datetime.today().strftime('%A')
    # 現在の曜日に応じたクエリを選択
    query, theme = THEME_QUERYS.get(current_day, ['Gemini', "Gemini"])

    search = arxiv.Search(
        query=query,  # 検索クエリ
        max_results=30,  # 取得する論文数
        sort_by=arxiv.SortCriterion.SubmittedDate,  # 論文を投稿された日付でソート
        sort_order=arxiv.SortOrder.Descending  # 新しい論文から順に取得
    )

    #searchの結果をリストに格納
    result_list = []
    for result in search.results():
        result_list.append(result)
    #ランダムにnum_papersの数だけ選ぶ
    num_papers = 1
    results = random.sample(result_list, k=num_papers)

    # 論文情報をSlackに投稿する
    for i, result in enumerate(results):
        try:
            pdf_url = result.pdf_url
            print(f"Start Summarize")
            model = genai.GenerativeModel(
                model_name="gemini-2.0-flash",
                generation_config=GENERATION_CONFIG,
            )

            # Retrieve and encode the PDF
            doc_data = base64.standard_b64encode(httpx.get(pdf_url).content).decode("utf-8")
            response = model.generate_content([{'mime_type':'application/pdf', 'data': doc_data}, PROMPT])
            print(response.text)

            summary = response.text
            title_en = result.title
            title, *body = summary.split('\n')
            body = '\n'.join(body)
            date_str = result.published.strftime("%Y-%m-%d %H:%M:%S")
            message = f"本日のテーマは「{theme}」です！\nタイトル: {title_en}\n発行日: {date_str}\nURL: {result.entry_id}\n```{title}\n{body}```"
            print(message)

            # response = client.chat_postMessage(
            #     channel=os.getenv("SLACK_CHANNEL"),
            #     text=message
            # )

        except SlackApiError as e:
            print(f"Error posting message: {e}")