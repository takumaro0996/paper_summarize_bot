MODEL_NAME = "gemini-2.5-pro-preview-03-25"

SEARCH_SIZE = 150

RESPITE_SIZE = 1

GENERATION_CONFIG = {
    'temperature': 0.0,
    'top_p': 0,
    'top_k': 1,
    'candidate_count': 1,
    "response_mime_type": "text/plain",
}

THEME_QUERYS = {
    "Monday": ['multimodal image video speech', "マルチモーダル"],
    "Tuesday": ['retrieval rag search', "RAG"],
    "Wednesday": ['reasoning capabilities evaluation', "推論精度の向上"],
    "Thursday": ['agents alignment feedback', "AIエージェント"],
    "Friday": ['Gemini LLM', "Gemini"],
    "Saturday": ['safety bias attacks evaluation', "セキリュティ"],
    "Sunday": ['training learning efficient tuning instruction', "学習・訓練方法"]
}

PROMPT = """## 命令
あなたは論文要約のエキスパートです。この論文の内容を、専門知識のない高校生でも理解できるように**日本語**で要約してください。
専門用語は可能な限り平易な言葉に置き換え、出力形式に従って、冒頭に余計な文章を入れないようにしてください。

## 出力形式
- タイトルの日本語訳 (自然な日本語で)
- 研究の目的や概要など (300字程度)
- 研究や実験の方法と結果 (300字程度)
- キーワード (英語で出力してくだしさい)

## 出力例（http://arxiv.org/abs/2502.03544v2を使用する）
- タイトルの日本語訳
  AlphaGeometry2によるオリンピック幾何学問題解決における金メダリストレベルの性能の実現
- 研究の目的や概要など
  研究は、AIによる数学的推論能力の向上を目指し、先行研究であるAlphaGeometry (AG1) を大幅に改良したAlphaGeometry2 (AG2) を開発しました。AG2は、国際数学オリンピック (IMO) レベルのより複雑な幾何学問題（物体の移動、角度・比率・距離の線形方程式、非構成的な問題など）を解くことを目的としています。
- 研究や実験の方法と結果
  AG2は、数理論理学と計算機科学の分野での最新の研究成果を取り入れ、特に「証明の構成」と「証明の最適化」に焦点を当てています。これにより、AG2はIMOレベルの幾何学問題を解くための新しいアプローチを提供します。実験結果として、AG2はIMO 2023年大会で金メダリストと同等のパフォーマンスを示しました。
- キーワード
  AI, AlphaGeometry language, Gemini
"""
