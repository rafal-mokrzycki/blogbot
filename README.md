Blogbot is a web app connected do GCP that enables collecting headlines or articles from web and post summaries on linkedin.

It consists of several modules:
A. Collector that collects articles (1) or (2) headlines using API and saves them in Google Storage
B. Transformer that transforms the files into longer blog posts (3) using transformer python module
C. Distributor thet schedules posting on LinkedIn using API

User has to choose:
a. a platform where to gather information
b. whether to get headlines or whole articles
c. how long blog posts should be
d. whether they contain photos or not
e. where to post the blog posts (LinkedIn, other)
f. how often to gather the info (once a day, once every 6 hrs.)
g. how often to post and how many posts should appear


To run:
```bash
uvicorn app.main:app
```

To run with changes update:
```bash
uvicorn app.main:app --reload
```
