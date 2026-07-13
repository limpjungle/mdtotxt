import os
import re
import tempfile
import markdown
from bs4 import BeautifulSoup
from flask import Flask, request, render_template_string, send_file, jsonify
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

HTML_FORM = """
<!doctype html>
<title>MD to TXT Converter</title>
<h1>Загрузите Markdown-файл</h1>
<form method=post enctype=multipart/form-data action=/convert>
  <input type=file name=file accept=".md,.markdown">
  <input type=submit value="Конвертировать">
</form>
"""


def md_to_plain_text(md_content: str) -> str:
    html = markdown.markdown(md_content)
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text()
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


@app.route("/")
def index():
    return render_template_string(HTML_FORM)


@app.route("/convert", methods=["POST"])
def convert():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    filename = file.filename

    if not filename:
        return jsonify({"error": "Empty filename"}), 400

    suffix = os.path.splitext(filename)[1] if "." in filename else ".md"

    with tempfile.NamedTemporaryFile(
        mode="w+", suffix=suffix, delete=False, encoding="utf-8"
    ) as tmp:
        file.save(tmp.name)
        tmp_path = tmp.name

    out_tmp_path = None  # <-- инициализация перед try
    try:
        with open(tmp_path, "r", encoding="utf-8") as f:
            md_content = f.read()
        plain_text = md_to_plain_text(md_content)

        with tempfile.NamedTemporaryFile(
            mode="w+", suffix=".txt", delete=False, encoding="utf-8"
        ) as out_tmp:
            out_tmp.write(plain_text)
            out_tmp_path = out_tmp.name

        download_name = os.path.splitext(filename)[0] + ".txt"
        return send_file(
            out_tmp_path,
            as_attachment=True,
            download_name=download_name,
            mimetype="text/plain",
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        # удаляем временные файлы
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
        if out_tmp_path and os.path.exists(out_tmp_path):
            os.unlink(out_tmp_path)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
