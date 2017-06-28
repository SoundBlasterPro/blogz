from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:fred123@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = "TheGoatSingsAtMidnight"

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    body = db.Column(db.Text)
        
    def __init__(self,title,body):
        self.title = title
        self.body = body

@app.route("/", methods=["POST", "GET"])
def index():

    return render_template("blog.html", title="Build-a-Blog!", blogs = getblogs())

@app.route("/newpost", methods=["POST", "GET"])
def blogpost():
    title_error = ""
    blog_error = ""
    if request.method == "POST":
        blog_title = request.form["blog_title"]
        blog_body = request.form["blog_body"]

        if not blog_title:
            title_error = "Please enter a title!"
        if not blog_body:
            blog_error = "Did you forget to write your blog?"
        if title_error or blog_error:
            return render_template("newpost.html", blog_title = blog_title, blog_body = blog_body, title_error = title_error, blog_error = blog_error)
        new_blog = Blog(blog_title, blog_body)
        db.session.add(new_blog)
        db.session.commit()

        #return render_template("blog.html", title="Build-a-Blog!", blogs = getblogs())
        
        return redirect("/display?blog.id=" + str(new_blog.id))
    return render_template("newpost.html", title="Build-a-Blog!")

@app.route("/display", methods=["GET"])
def displayblog():
    blog_id = request.args.get("blog.id")
    blog = Blog.query.filter_by(id = blog_id).first()
    return render_template("display.html", title="Build-a-Blog!", blog = blog )

def getblogs():
    return Blog.query.filter_by().all()

if __name__ == '__main__':
    app.run()