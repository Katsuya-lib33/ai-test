import os

from flask import Flask, jsonify, request

from youtube_script_agent import ScriptRequest, YouTubeScriptAgent

app = Flask(__name__)


def _build_request(payload: dict) -> ScriptRequest:
    return ScriptRequest(
        topic=payload.get("topic", ""),
        audience=payload.get("audience", ""),
        duration_minutes=int(payload.get("duration_minutes", 8)),
        tone=payload.get("tone", "わかりやすく親しみやすい"),
    )


@app.get("/")
def healthcheck():
    return jsonify(
        {
            "name": "youtube-script-agent",
            "status": "ok",
            "model_default": os.environ.get("OPENAI_MODEL", "gpt-4.1"),
        }
    )


@app.post("/generate")
def generate():
    payload = request.get_json(silent=True) or {}

    if not payload.get("topic") or not payload.get("audience"):
        return (
            jsonify({"error": "'topic' と 'audience' は必須です"}),
            400,
        )

    model = payload.get("model") or os.environ.get("OPENAI_MODEL", "gpt-4.1")
    agent = YouTubeScriptAgent(model=model)
    result = agent.generate(_build_request(payload))
    return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8000")))
