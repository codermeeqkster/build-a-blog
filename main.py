from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import jinja2


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:build-a-blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'f8wv3w2f>v9j4sEuhcNYydAGMzzZJgkGgyHE9gUqaJcCk^f*^o7fQyBT%XtTvcYM'


class Entry(db.Model):
    '''
    Stores blog entries
    '''
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(180))
    body = db.Column(db.String(1000))

    def __init__(self, title, body ):
        self.title = title
        self.body = body
        #self.created = datetime.utcnow()
  

#
@app.route("/")
def index():
    
    return redirect("/blog")
#
@app.route("/blog")
def display_blog_entries():
    
    entry_id = request.args.get('id')
    if (entry_id):
        entry = Entry.query.get(entry_id)
        return render_template('ind_entry.html', title="Blog Entry", entry=entry)

    blog_list = Entry.query.all()   
    return render_template('blog_list.html', title="Blog List", blog_list=blog_list)

def is_valid(x):
        if x:
            return True
        else:
            return False

#
@app.route('/newpost', methods=['GET', 'POST'])
def new_entry():
    if request.method == 'POST':
        
        title_error = ""
        body_error = ""
        new_entry_title = request.form['title']
        new_entry_body = request.form['body']
        new_entry = Entry(new_entry_title, new_entry_body)

        if is_valid(new_entry_title) and is_valid(new_entry_body):
            db.session.add(new_entry)
            db.session.commit()

            url = "/blog?id=" + str(new_entry.id)
            return redirect(url)
        else:
            if not is_valid(new_entry_title) and not is_valid(new_entry_body):
                title_error = "Please enter text for blog title"
                body_error = "Please enter text for blog entry"
                return render_template('new_entry.html', body_error=body_error, title_error=title_error)
            elif not is_valid(new_entry_title):
                title_error = "Please enter text for blog title"
                return render_template('new_entry.html', title_error=title_error, new_entry_body=new_entry_body)
            elif not is_valid(new_entry_body):
                body_error = "Please enter text for blog entry"
                return render_template('new_entry.html', body_error=body_error, new_entry_title=new_entry_title)

    else: # GET
        return render_template('new_entry.html', title="New blog entry")
        
if __name__ == '__main__':
    app.run()