import argparse
import json
import os
from dataclasses import dataclass

from openai import OpenAI

from prompts import (
    OUTLINE_PROMPT,
    QA_PROMPT,
    RESEARCH_PROMPT,
    SCRIPT_PROMPT,
    SYSTEM_PROMPT,
)


@dataclass
class ScriptRequest:
    topic: str
    audience: str
    duration_minutes: int
    tone: str


class YouTubeScriptAgent:
    def __init__(self, model: str = "gpt-4.1") -> None:
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.model = model

    def _run(self, user_prompt: str) -> str:
        response = self.client.responses.create(
            model=self.model,
            input=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.7,
        )
        return response.output_text.strip()

    def generate(self, req: ScriptRequest) -> dict:
        research = self._run(
            RESEARCH_PROMPT.format(
                topic=req.topic,
                audience=req.audience,
                duration_minutes=req.duration_minutes,
                tone=req.tone,
            )
        )

        outline = self._run(
            OUTLINE_PROMPT.format(duration_minutes=req.duration_minutes)
            + "\n\n準備メモ:\n"
            + research
        )

        script = self._run(SCRIPT_PROMPT + "\n\n構成案:\n" + outline)
        review = self._run(QA_PROMPT + "\n\n台本:\n" + script)

        return {
            "input": req.__dict__,
            "research": research,
            "outline": outline,
            "script": script,
            "review": review,
        }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="YouTube台本生成AIエージェント")
    parser.add_argument("--topic", required=True, help="動画テーマ")
    parser.add_argument("--audience", required=True, help="ターゲット視聴者")
    parser.add_argument("--duration-minutes", type=int, default=8, help="想定尺(分)")
    parser.add_argument("--tone", default="わかりやすく親しみやすい", help="トーン")
    parser.add_argument(
        "--format",
        choices=["json", "markdown"],
        default="markdown",
        help="出力形式",
    )
    parser.add_argument("--model", default="gpt-4.1", help="使用モデル")
    return parser.parse_args()


def to_markdown(result: dict) -> str:
    return (
        f"# YouTube台本生成結果\n\n"
        f"## 入力\n"
        f"- テーマ: {result['input']['topic']}\n"
        f"- ターゲット: {result['input']['audience']}\n"
        f"- 想定尺: {result['input']['duration_minutes']} 分\n"
        f"- トーン: {result['input']['tone']}\n\n"
        f"## 1. 準備メモ\n{result['research']}\n\n"
        f"## 2. 構成案\n{result['outline']}\n\n"
        f"## 3. 台本\n{result['script']}\n\n"
        f"## 4. レビュー\n{result['review']}\n"
    )


def main() -> None:
    args = parse_args()
    request = ScriptRequest(
        topic=args.topic,
        audience=args.audience,
        duration_minutes=args.duration_minutes,
        tone=args.tone,
    )
    agent = YouTubeScriptAgent(model=args.model)
    result = agent.generate(request)

    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(to_markdown(result))


if __name__ == "__main__":
    main()
