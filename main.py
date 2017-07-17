from flask import Flask, request, redirect, render_template, session, flash
from models import User, Blog
from app import db,app

@app.route("/", methods=["POST", "GET"])
def index():
    users = User.query.filter_by().all()
    return render_template("index.html", users = users)
    #return render_template("blog.html", title="Build-a-Blog!", blogs = getblogs())

@app.route("/blog", methods = ["GET"])
def blog():
    #show blogs for a specific user chosen in the index
    users = User.query.filter_by().all()
    owner_id = request.args.get("user_id")
    if owner_id:
        blogs = Blog.query.filter_by(owner_id = owner_id).all()
        return render_template("blog.html", title = "Blogz", blogs = blogs, users = users)
    allblogs = Blog.query.filter_by().all()
    return render_template("blog.html", title="Blogz", blogs = allblogs, users = users)

@app.route("/newpost", methods=["POST", "GET"])
def blogpost():
    title_error = ""
    blog_error = ""
    user = User.query.filter_by(username = session["user"]).first()
    if request.method == "POST":
        blog_title = request.form["blog_title"]
        blog_body = request.form["blog_body"]

        if not blog_title:
            title_error = "Please enter a title!"
        if not blog_body:
            blog_error = "Who the hell writes a blank blog post?"
        if title_error or blog_error:
            return render_template("newpost.html", blog_title = blog_title, blog_body = blog_body, title_error = title_error, blog_error = blog_error)
        new_blog = Blog(blog_title, blog_body, user.user_id)
        db.session.add(new_blog)
        db.session.commit()

        #return render_template("blog.html", title="Build-a-Blog!", blogs = getblogs())
        
        return redirect("/display?blog.blog_id=" + str(new_blog.blog_id))
    return render_template("newpost.html", title="Build-a-Blog!")

@app.route("/display", methods=["GET"])
def displayblog():
    blog_id = request.args.get("blog.blog_id")
    blog = Blog.query.filter_by(blog_id = blog_id).first()
    return render_template("display.html", title="Build-a-Blog!", blog = blog )

def getblogs():
    owner = User.query.filter_by(username = session["user"]).first()
    return Blog.query.filter_by(owner = owner).all()
    #return Blog.query.filter_by().all
    

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username = username).first()
        if user and user.password == password:
            session["user"] = user.username
            flash("Welcome, " + user.username)
            return redirect("/")
        else:
            flash("Bad username or password")
            return redirect("/login")

    return render_template("login.html")

@app.route("/logout", methods=["POST", "GET"])
def logout():
    username = session["user"]
    del session["user"]
    flash("Logged out " + username)
    return redirect("/")

@app.route("/register", methods=["POST","GET"])
def register():
    error = False
    username_error = ''
    password_error = ''
    validate_error = ''

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        password2 = request.form["verify"]
        if validate(username) != username: #fails general validation
            username_error = validate(username)
            error = True
        if validate(password) != password: #fails general validation
            password_error = validate(password)
            error = True
        if password_match(password, password2) != True:
            validate_error = "Passwords do not match"
            error = True
        duplicate_user = User.query.filter_by(username = username).count()
        if duplicate_user > 0:
            username_error = "This username already exists!"
            error = True

        if error:
            return render_template("register.html", title = "User Signup",
                            username = username,
                            invalid_username = username_error, 
                            invalid_password = password_error, 
                            verify_error = validate_error
                            )
        else:
            user = User(username = username, password = password)
            db.session.add(user)
            db.session.commit()
            session['user'] = user.username
            flash("Welcome, " + user.username + "!")
            return redirect("/")
    else:
        return render_template("register.html", title = "User Signup")

def validate(text):

    if not text: #user submits a blank field
        error = "This section cannot be left blank."
        return error
    if contains_spaces(text):
        error = "Username cannot contain spaces."
        return error
    if len(text) <= 3:
        error = "Please enter a value greater than 3 characters."
        return error
    if len(text) > 20:
        error = "Please enter a value less than 20 characters."
        return error
    
    return text

def password_match(password, verify):
    if password != verify:
        return False
    else:
        return True

def contains_spaces(text):
    
    for character in text:
        if character == " ":
            return True
    
    return False

endpoints_without_login = ["login", "register", "blog", "index", "displayblog"]

@app.before_request
def require_login():
    if not ('user' in session or request.endpoint in endpoints_without_login):
        return redirect("/login")

app.secret_key = "TheGoatSingsAtMidnight"
if __name__ == '__main__':
    app.run()