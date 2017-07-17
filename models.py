from app import db, app

class User(db.Model):

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    blog = db.relationship("Blog", backref="owner")

    def __init__(self,username,password):
        self.username = username
        self.password = password

class Blog(db.Model):
    blog_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    body = db.Column(db.Text)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
        
    def __init__(self,title,body,owner_id):
        self.title = title
        self.body = body
        self.owner_id = owner_id