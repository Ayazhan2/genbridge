# GenBridge – Experience meets the future of work

GenBridge is a student project for the **Social Media Analytics** course at Woosong University (Fall 2026).

The website shows which jobs are growing or declining (based on the World Economic Forum *Future of Jobs Report 2025*) and connects young people with mentors aged 50+ who want to share their experience and earn from it.

🌍 **Live website:** https://genbridgekr.pythonanywhere.com

## Features
- **Job Trends** – top 10 fastest-growing and fastest-declining jobs
- **Career Check** – type your job and see if it is growing or declining, plus related jobs
- **Mentors** – list of mentors from the database
- **Become a Mentor** – sign-up form with server-side validation
- **Request a Session** – send a request to a mentor
- **Google Analytics 4** – page views + custom events (`career_check`, `mentor_signup`, `session_request`)

## Technologies
| Part | Technology |
|------|------------|
| Front-end | HTML5, Jinja2 templates, CSS3, JavaScript (fetch API) |
| Back-end | Python 3, Flask 3.1 |
| Database | SQLite |
| Hosting | PythonAnywhere |
| Analytics | Google Analytics 4 |
| IDE | PyCharm 2025.2 |

## Project structure
```
app.py          – back-end: pages, API, form validation
db_setup.py     – creates the database and adds the jobs
templates/      – HTML pages (base.html is the common layout)
static/         – style.css and trends.js
```

## How to run locally
```bash
pip install flask
python db_setup.py
python app.py
```
Then open http://127.0.0.1:5000

## API
| Address | Returns |
|---------|---------|
| `/api/jobs` | all jobs in JSON |
| `/api/check?job=bank` | Career Check result in JSON |
| `/api/stats` | number of jobs, mentors and requests |

## Author
Ayazhan Mussabayeva (202609069)
