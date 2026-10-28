import json
import os
from urllib.parse import urlparse
from flask import Flask, render_template, request

app = Flask(__name__)
app.config["DATA_FILE"] = "submissions.json"

FIELDS = [("name", "Name"), ("reg_no", "Registration number"),
          ("title", "Assignment title"), ("url", "Submission URL")]


def load_submissions():
    path = app.config["DATA_FILE"]
    if not os.path.exists(path):
        return []
    with open(path) as f:
        return json.load(f)


def save_submission(sub):
    subs = load_submissions()
    subs.append(sub)
    with open(app.config["DATA_FILE"], "w") as f:
        json.dump(subs, f, indent=2)


def is_valid_url(url):
    p = urlparse(url)
    return p.scheme in ("http", "https") and "." in p.netloc


def validate(form):
    errors = []
    for key, label in FIELDS:
        if not form[key]:
            errors.append(f"{label} is required")
    if form["url"] and not is_valid_url(form["url"]):
        errors.append("Submission URL is not valid")
    return errors


@app.route("/", methods=["GET", "POST"])
def index():
    errors, message = [], ""
    if request.method == "POST":
        form = {key: request.form.get(key, "").strip() for key, _ in FIELDS}
        errors = validate(form)
        if not errors:
            save_submission(form)
            message = "Submission saved"
    html = render_template("index.html", errors=errors, message=message,
                           submissions=load_submissions())
    return html, (400 if errors else 200)


if __name__ == "__main__":
    app.run(debug=True)
