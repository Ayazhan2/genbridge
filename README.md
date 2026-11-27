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
- **Google Analytics 4 + Matomo** – page views + custom events (`career_check`, `mentor_signup`, `session_request`, `social_click`, `share`)
- **Share my result** – copy a link to a Career Check result or use the phone's share menu

## Technologies
| Part | Technology |
|------|------------|
| Front-end | HTML5, Jinja2 templates, CSS3, JavaScript (fetch API) |
| Back-end | Python 3, Flask 3.1 |
| Database | SQLite |
| Hosting | PythonAnywhere |
| Analytics | Google Analytics 4, Matomo Cloud, Zoho Social |
| IDE | PyCharm 2025.2 |

## Project structure
```
app.py          – back-end: pages, API, form validation
db_setup.py     – creates the database and adds the jobs
templates/      – HTML pages (base.html is the common layout)
static/         – style.css, trends.js and og-image.png
```

## Social media
📸 **Instagram:** [@genbridge_sma](https://www.instagram.com/genbridge_sma/)

Posts are scheduled and measured in **Zoho Social**. The Instagram account is connected to Zoho Social directly with Instagram login, no Facebook Page needed.

How a visit from social media is tracked:

```
Zoho Social post (link with UTM tags)
   │
   ▼
website visit       GA4 + Matomo read utm_source / utm_medium / utm_campaign
   │
   ▼
actions on site     career_check, share, social_click, mentor_signup, session_request
```

- **Follow us** in the footer – `social_click` event with `network`
- **Share my result** on the Career Check page – `share` event with `network`; the shared link has `utm_source=<network>&utm_medium=social&utm_campaign=share_result`
- **Open Graph / Twitter card** tags + `static/og-image.png` – link previews on social networks and messengers

Social links are set in one place in `app.py` (`INSTAGRAM_URL`, `FACEBOOK_URL`). An empty value hides the link.

The Instagram bio links to the short address `/ig`. It redirects to the home page with `utm_source=instagram&utm_medium=social&utm_campaign=genbridge_launch`.

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

## Team #1
- Ayazhan Mussabayeva (202609069)
- Miras Zadabek
- Majd Benomar
