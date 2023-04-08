from website import create_app, db
from website.utils import get_trending_title, ai_text
from apscheduler.schedulers.background import BackgroundScheduler
from website.models import Blog

app = create_app()

def auto_blog():
    title = get_trending_title()
    blog_para = ai_text(title)
    if blog_para != '':
        blog_db = Blog(title=title, paragraph=blog_para, catagry='', show_para=False)
        db.session.add(blog_db)
        db.session.commit()

scheduler = BackgroundScheduler()
scheduler.add_job(auto_blog,'interval',minutes=60)
scheduler.start()


if __name__ == "__main__":
    app.run()