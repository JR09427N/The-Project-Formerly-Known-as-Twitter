from flask import Flask, redirect, request, render_template, session, make_response
from flask_session import Session

import example

app = Flask(__name__)
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# =======================
# OLD ROUTES (Commented Out)
# =======================
"""
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/final/signup")

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/example/login")
def example_login():
    return login()

@app.route("/example/signup")
def example_signup():
    return signup()

@app.route("/example/final_listfeedposts")
def example_feed():
    return final_listfeedposts()

@app.route("/example/final_getposts")
def example_getposts():
    return final_getposts()

@app.route("/example/final_uploadpost", methods=["POST"])
def example_uploadpost():
    return final_uploadpost()

@app.route("/example/final_deletepost", methods=["POST"])
def example_deletepost():
    return final_deletepost()

@app.route("/example/final_getpfp")
def example_getpfp():
    return final_getpfp()

@app.route("/example/final_getemail")
def example_getemail():
    return final_getemail()

@app.route("/example/final_uploadpfp", methods=["POST"])
def example_uploadpfp():
    return final_uploadpfp()

@app.route('/posts')
def example_posts():
    username = session['username']
    return redirect(f"/feed/{username}")

@app.route('/feed/<username>')
def example_feed(username):
    return render_template('final_feed.html', username=username)

"""

# =======================
# FINAL PROJECT ROUTES
# =======================

@app.route('/account')
def example_account():
    username = session['username']
    return redirect(f"/profile/{username}")

@app.route('/profile/<username>')
def profile_page(username):
    if username == session['username']:
        return render_template('final_profile_self.html', username=username)
    else:
        return render_template('final_profile_other.html', username=username)

@app.route("/example/login")
def final_login_route():
    return example.login()

@app.route("/example/signup")
def final_signup_route():
    return example.signup()

@app.route("/example/final_getposts")
def example_final_getposts():
    return example.final_getposts()

@app.route("/example/final_uploadpost", methods=["POST"])
def final_upload_post_route():
    return example.final_uploadpost()

@app.route("/example/final_getpfp")
def final_getpfp_route():
    return example.final_getpfp()

@app.route("/example/final_getemail")
def final_getemail_route():
    return example.final_getemail()

@app.route("/example/final_uploadpfp", methods=["POST"])
def final_uploadpfp_route():
    return example.final_uploadpfp()

@app.route("/example/final_listfeedposts")
def final_list_feed_route():
    return example.final_listfeedposts()

@app.route("/example/final_listonepost")
def final_list_one_post_route():
    return example.final_listonepost()

@app.route("/example/final_uploadcomm", methods=["POST"])
def final_upload_comm_route():
    return example.final_uploadcomm()

@app.route('/post_view/<postId>')
def final_post_view(postId):
    return render_template('final_postview.html', postId=postId)

@app.route('/feed')
def final_feed():
    return render_template('final_feed.html')




