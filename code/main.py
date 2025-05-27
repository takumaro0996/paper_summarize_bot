import os
import numpy as np
import base64
import httpx
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import arxiv
import google.generativeai as genai
import random
import datetime
import requests
import functions_framework

from const import MODEL_NAME, SEARCH_SIZE, RESPITE_SIZE, GENERATION_CONFIG, THEME_QUERYS, PROMPT

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))


def get_citation_count(arxiv_id):
    url = f"https://api.semanticscholar.org/graph/v1/paper/arXiv:{arxiv_id}?fields=citationCount"
    resp = requests.get(url)
    if resp.status_code == 200:
        data = resp.json()
        return data.get('citationCount', 0)
    else:
        return 0

def get_altmetric_score(arxiv_id):
    url = f"https://api.altmetric.com/v1/arxiv/{arxiv_id}"
    resp = requests.get(url)
    if resp.status_code == 200:
        data = resp.json()
        return data.get('score', 0), data.get('cited_by_posts_count', 0)
    else:
        return 0, 0

@functions_framework.cloud_event
def main(cloud_event):
    current_day = datetime.datetime.today().strftime('%A')
    query, theme = THEME_QUERYS.get(current_day, ['Gemini', "Gemini"])
    print(f"[DEBUG] Current day: {current_day}, Query: {query}, Theme: {theme}")

    # CS分野に絞って検索する場合は以下のように指定する
    cs_query = f"cat:cs.* AND ({query})"

    search = arxiv.Search(
        query=cs_query,
        max_results=SEARCH_SIZE,
        sort_by=arxiv.SortCriterion.SubmittedDate,
        sort_order=arxiv.SortOrder.Descending
    )
    one_month_ago = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=RESPITE_SIZE)
    print(f"[DEBUG] Searching arXiv with query: {cs_query}")
    print(f"[DEBUG] One month ago date: {one_month_ago}")
    result_list = []
    for result in search.results():
        if result.published <= one_month_ago:
            result_list.append(result)

    print(f"[DEBUG] Retrieved {len(result_list)} papers published within the last month.")

    scored_results = []
    for result in result_list:
        arxiv_id_with_version = result.entry_id.split('/')[-1]
        arxiv_id = arxiv_id_with_version.split('v')[0]

        citation_count = get_citation_count(arxiv_id)
        altmetric_score, cited_by_posts_count = get_altmetric_score(arxiv_id)
        days_since_published = (datetime.datetime.now(datetime.timezone.utc) - result.published).days

        if altmetric_score > 5 or cited_by_posts_count > 12:
            score = {
                "citation_count": citation_count,
                "altmetric_score": altmetric_score,
                "cited_by_posts_count": cited_by_posts_count,
                "days_since_published": days_since_published,
                "weighted_score":  altmetric_score / np.log(days_since_published)
            }

            print(f"[DEBUG] Processing arxiv_id: {arxiv_id}, Title: {result.title}")
            print(f"[DEBUG] Citation count: {citation_count}")
            print(f"[DEBUG] Altmetric score: {altmetric_score}, SNS cited count: {cited_by_posts_count}")
            print(f"[DEBUG] Days since published: {days_since_published}")
            print(f"[DEBUG] Weighted score: {score['weighted_score']}")

            scored_results.append((score, result))


    scored_results.sort(
        key=lambda x: (
            x[0]["weighted_score"],
            x[0]["cited_by_posts_count"],
            x[0]["citation_count"]
        ),
        reverse=True
    )
    print(f"[DEBUG] Total papers processed: {len(scored_results)}")

    # # 重み付き確率に基づいて3件の論文を選択
    # if len(scored_results) >= 3:
    #     # 各論文のweighted_scoreを取り出す
    #     weights = np.array([score["weighted_score"] for score, _ in scored_results])
    #     # 重みを確率に変換（合計が1になるように正規化）
    #     probabilities = weights / np.sum(weights)
    #     # 確率に基づいてインデックスを抽出（重複なく3件選択）
    #     selected_indices = np.random.choice(len(scored_results), size=3, replace=False, p=probabilities)
    #     selected_results = [scored_results[i] for i in selected_indices]
    # else:
    #     selected_results = scored_results

    for i, (score, result) in enumerate(scored_results[0:3]):
        print(f"[DEBUG] Rank {i+1}: {result.title}")
        print(f"[DEBUG] Citation count: {score['citation_count']}")
        print(f"[DEBUG] Altmetric score: {score['altmetric_score']}, SNS cited count: {score['cited_by_posts_count']}")
        try:
            pdf_url = result.pdf_url
            model = genai.GenerativeModel(
                model_name=MODEL_NAME,
                generation_config=GENERATION_CONFIG,
            )

            print(f"[DEBUG] Fetching PDF content from: {pdf_url}")
            pdf_response = httpx.get(pdf_url)
            print(f"[DEBUG] PDF fetch status: {pdf_response.status_code}")

            doc_data = base64.standard_b64encode(pdf_response.content).decode("utf-8")
            print("[DEBUG] PDF successfully encoded to base64.")

            response = model.generate_content([{'mime_type':'application/pdf', 'data': doc_data}, PROMPT])
            print("[DEBUG] Summary generated from Gemini API.")

            summary = response.text
            title_en = result.title
            title, *body = summary.split('\n')
            body = '\n'.join(body)
            date_str = result.published.strftime("%Y-%m-%d")
            if i == 0:
                message = f"本日のテーマ「{theme}」\n"
            else:
                message = ""
            message += (
                f"タイトル: {title_en} ({date_str})\n"
                f"Altmetric Score: {round(score['altmetric_score'],1)}, "
                f"SNSポスト数: {score['cited_by_posts_count']}, "
                f"論文引用数: {score['citation_count']}\n"
                f"URL: {result.entry_id}\n"
                f"```{title}\n{body}```"
            )
            print(f"[DEBUG] Sending Slack message:\n{message}")

            client.chat_postMessage(
                channel=os.getenv("SLACK_CHANNEL"),
                text=message
            )

            print("[DEBUG] Message successfully sent to Slack.")

        except SlackApiError as e:
            print(f"[ERROR] Error posting message to Slack: {e}")
