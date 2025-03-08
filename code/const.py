GENERATION_CONFIG = {
    'temperature': 0.0,
    'top_p': 0,
    'top_k': 1,
    'candidate_count': 1,
    "response_mime_type": "text/plain",
}

THEME_QUERYS = {
    "Monday": ['Gemini', "Gemini"],
    "Tuesday": ['GPT', "GPT"],
    "Wednesday": ['transcribe LLM', "transcribe"],
    "Thursday": ['Prompt Engineering', "Prompt Engineering"],
    "Friday": ['Multimodal ', "Multimodal "],
    "Saturday": ['Gemini', "Gemini"],
    "Sunday": ['GPT', "GPT"]
}

PROMPT = """# 命令
あなたは論文要約のエキスパートです。この論文の内容を、専門知識のない理解できるように日本語で要約してください。
専門用語は可能な限り平易な言葉に置き換え、研究の目的、先行研究との比較、使用された方法論、主要な結果、応用可能性, 今後の展望や課題、キーワードについて説明してください。
出力形式に従って、冒頭に余計な文章を入れないようにしてください。

# 出力形式
- **タイトルの日本語訳**

- **研究の目的**（300文字程度）

- **先行研究との比較**（150文字程度）

- **使用された方法論**（300文字程度）

- **主要な結果**（300文字程度）

- **応用可能性**（150文字程度）

- **今後の展望や課題**（100文字程度）

- **キーワード**（3~5つ程度）
"""

PROMPTS = ["""与えられた論文を以下のフォーマットに従って、「日本語訳をしたタイトル」、「要点（3つ以内）」、「キーワード（5つまで）」を抽出してください。
- タイトル:[タイトルの日本語訳]
- 要点
    - [要点1]
    - [要点2]
    - [要点3]
- キーワード: [キーワード1], [キーワード2], ...
""",
"わかりました。フォーマットに準じた形式でまとめます",
# sample1
"""
title: Reproducible data science over data lakes: replayable data pipelines with Bauplan and Nessie
body: As the Lakehouse architecture becomes more widespread, ensuring the reproducibility of data workloads over data lakes emerges as a crucial concern for data engineers. However, achieving reproducibility remains challenging. The size of data pipelines contributes to slow testing and iterations, while the intertwining of business logic and data management complicates debugging and increases error susceptibility. In this paper, we highlight recent advancements made at Bauplan in addressing this challenge. We introduce a system designed to decouple compute from data management, by leveraging a cloud runtime alongside Nessie, an open-source catalog with Git semantics. Demonstrating the system's capabilities, we showcase its ability to offer time-travel and branching semantics on top of object storage, and offer full pipeline reproducibility with a few CLI commands.
""",
"""
- タイトル:データレイク上の再現可能なデータサイエンス: BauplanとNessieを用いた再実行可能なデータパイプライン
- 要点
    - Lakehouseアーキテクチャの普及に伴い、データレイクにおけるデータワークロードの再現性が重要になっている。
    - BauplanとNessieを用いて、計算処理をデータ管理から切り離し、オブジェクトストレージ上でタイムトラベルやブランチングのセマンティクスを提供するシステムを紹介。
    - 数回のCLIコマンドで、データパイプラインの完全な再現性を実現できることを実証。
- キーワード: Lakehouse, データレイク, 再現性, データパイプライン, Nessie
""",
# sample2
"""
title: Personhood credentials: Artificial intelligence and the value of privacy-preserving tools to distinguish who is real online
body: Anonymity is an important principle online. However, malicious actors have long used misleading identities to conduct fraud, spread disinformation, and carry out other deceptive schemes. With the advent of increasingly capable AI, bad actors can amplify the potential scale and effectiveness of their operations, intensifying the challenge of balancing anonymity and trustworthiness online. In this paper, we analyze the value of a new tool to address this challenge: "personhood credentials" (PHCs), digital credentials that empower users to demonstrate that they are real people -- not AIs -- to online services, without disclosing any personal information. Such credentials can be issued by a range of trusted institutions -- governments or otherwise. A PHC system, according to our definition, could be local or global, and does not need to be biometrics-based. Two trends in AI contribute to the urgency of the challenge: AI's increasing indistinguishability from people online (i.e., lifelike content and avatars, agentic activity), and AI's increasing scalability (i.e., cost-effectiveness, accessibility). Drawing on a long history of research into anonymous credentials and "proof-of-personhood" systems, personhood credentials give people a way to signal their trustworthiness on online platforms, and offer service providers new tools for reducing misuse by bad actors. In contrast, existing countermeasures to automated deception -- such as CAPTCHAs -- are inadequate against sophisticated AI, while stringent identity verification solutions are insufficiently private for many use-cases. After surveying the benefits of personhood credentials, we also examine deployment risks and design challenges. We conclude with actionable next steps for policymakers, technologists, and standards bodies to consider in consultation with the public.
""",
"""
- タイトル: 人間性クレデンシャル: 人工知能とオンラインで誰が本物かを区別するプライバシー保護ツールの価値
- 要点
    - 人間性クレデンシャル（PHCs）は、ユーザーが個人情報を開示せずに本物の人間であることを示すためのデジタル証明書である。
    - AIの発展により、悪意のある行為が増加し、その影響を抑えるための信頼性と匿名性のバランスが求められている。
    - CAPTCHAsなどの既存の対策が不十分な中で、PHCsは悪意ある行為の防止に新たな手段を提供する。
- キーワード: 人間性クレデンシャル, プライバシー保護, 信頼性, 人工知能, オンライン詐欺防止
"""
]