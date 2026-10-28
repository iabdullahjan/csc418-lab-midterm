# Assignment Submission Portal with Automated Testing

CSC418 DevOps Lab Midterm
Mian Abdullah Jan (FA23-BSE-019)

A simple web portal where students enter their name, registration number, assignment title and submission URL. Valid submissions are saved in `submissions.json` and shown in a table. Every push to GitHub runs the automated tests, and the test report is sent automatically to a receiver on the local PC, which saves it as `test-report.json`.

## Project structure

```
app.py                     Flask app (form, validation, saving, list)
templates/index.html       Page for the app
tests/test_portal.py       Automated tests (pytest)
ci/make_report.py          Turns the pytest results into the JSON report
receiver/receiver.py       Local HTTP receiver that saves test-report.json
docs/index.html            Static demo for GitHub Pages (bonus)
.github/workflows/ci.yml   CI pipeline (GitHub Actions)
start-receiver.bat         Double-click to start the receiver
start-runner.bat           Double-click to start the self-hosted runner
```

## Requirements

- Python 3.10 or newer
- Git

Install the packages:

```
python -m pip install -r requirements.txt
```

## Run the application

```
python app.py
```

Then open http://127.0.0.1:5000 in a browser.

## Run the tests

```
python -m pytest -v
```

The three test cases are:

| Test | Expected result |
|---|---|
| test_valid_submission_is_saved_and_listed | Complete details and a valid URL are saved and appear in the list |
| test_missing_registration_number_is_rejected | Rejected with the message "Registration number is required" |
| test_invalid_url_is_rejected_and_not_saved | Rejected with "Submission URL is not valid" and nothing is saved |

## Start the report receiver

```
python receiver/receiver.py
```

(or double-click `start-receiver.bat`)

It listens on http://localhost:5050/report. When the pipeline sends a report, it saves it as `test-report.json` in the folder it was started from, and also keeps a copy of every run in `reports/report-<run id>.json`.

## How the CI pipeline works

The workflow `.github/workflows/ci.yml` runs on every push.

1. The `test` job runs on a self-hosted runner installed on this PC (`C:\actions-runner`). A GitHub-hosted runner's localhost is the runner itself, so running the runner locally lets it reach the receiver on `localhost:5050`.
2. It installs the packages and runs `pytest --junitxml=results.xml`. If any test fails, pytest exits with an error and the step and the run fail.
3. `ci/make_report.py` reads `results.xml` and writes `test-report.json` with the repository, branch, commit SHA, run ID, timestamp, each test's result and failure message, the counts and the overall status.
4. The report is sent to the local receiver with an HTTP POST. These steps use `if: always()`, so the report is delivered for both passing and failing runs.
5. The report is also uploaded as a run artifact.

### Setting up the self-hosted runner

1. In the repository go to Settings > Actions > Runners > New self-hosted runner, choose Windows x64.
2. Download and extract the runner into `C:\actions-runner` and run `config.cmd` with the URL and token GitHub shows. Answer N to "run as service".
3. Start it with `C:\actions-runner\run.cmd` (or `start-runner.bat`). It must show "Listening for Jobs".

### Demo order

1. Start the receiver (`start-receiver.bat`).
2. Start the runner (`start-runner.bat`).
3. Push a commit and watch the Actions tab. `test-report.json` updates on its own.

## Bonus: GitHub Pages deployment

The `deploy` job runs only on pushes to `main` and has `needs: test`, so it only runs when all tests passed. When a test fails, the deploy job is skipped and the old site stays live. It publishes the static demo in `docs/`.

Pages source must be set to "GitHub Actions" in Settings > Pages.

Live demo: https://iabdullahjan.github.io/csc418-lab-midterm/

## Bonus: Email report

The last step of the `test` job emails the report (subject has the result and commit SHA, body is the JSON report, and the file is attached) after both passing and failing runs. Credentials are kept in GitHub secrets, not in the code.

Set these in Settings > Secrets and variables > Actions:

- Secret `MAIL_USERNAME`: the Gmail address that sends the mail
- Secret `MAIL_PASSWORD`: a Gmail App Password for that account
- Variable `REPORT_EMAIL`: the address that receives the report

The email step is skipped while `REPORT_EMAIL` is not set.
