#处理与博客相关的路由和视图
import datetime
import os

from . import main
from flask import render_template, session, request, redirect
from ..models import *
from .. import db

@main.route('/')
def main_index():
  categories = Category.query.all()
  topics = Topic.query.limit(10).all()
  #判断session中是否有id和loginname的之
  if "id" in session and "loginname" in session:
    #已经登录过从数据库中获取登录信息
    id = session["id"]
    user = User.query.filter_by(ID=id).first()

  return render_template('index.html',params=locals())

@main.route("/release",methods=["GET","POST"])
def release_views():
  if request.method == "GET":
    #权限验证
    if "id" in session and "loginname" in session:
      user = User.query.filter_by(ID=session["id"]).first()
      if user.is_author:
        categories = Category.query.all()
        return render_template("release.html",params=locals())
    url=request.headers.get("Referer","/")
    return redirect(url)
  else:
    #post请求处理发表博客的相关操作
    topic = Topic()
    topic.title=request.form["author"]
    topic.blogtype_id=request.form["list"]
    topic.category_id = request.form["category"]
    topic.user_id = session["id"]
    topic.content = request.form["content"]
    topic.pub_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if request.files:
      f = request.files["image"]
      ftime = datetime.datetime.now().strftime("%Y%m%d%H%M%S:%f")
      ext = f.filename.split(".")[-1]
      filename = ftime+"."+ext
      topic.images = "upload/"+filename
      basedir = os.path.dirname(os.path.dirname(__file__))
      upload_path=os.path.join(basedir,"static/upload",filename)
      f.save(upload_path)
    db.session.add(topic)
    return redirect("/")


@main.route("/list")
def list_views():
  # 判断session中是否有id和loginname的之
  if "id" in session and "loginname" in session:
    id = request.args["id"]
    categories = Category.query.all()
    topics = Topic.query.filter_by(category_id=id,user_id=session["id"]).limit(10).all()
    # 已经登录过从数据库中获取登录信息
    id = session["id"]
    user = User.query.filter_by(ID=id).first()
    return render_template("list.html", params=locals())
  else:
    return redirect("/login")


@main.route("/info",methods=["GET","POST"])
def info_views():
  if request.method == "GET":
    if "id" in session and "loginname" in session:
      id  = request.args["id"]
      topic = Topic.query.filter_by(id = id).first()
      id = session["id"]
      user = User.query.filter_by(ID=id).first()
      reply = Reply.query.filter_by(topic_id=topic.id).all()
      return render_template("info.html",params = locals())
    else:
      return redirect("/login")
  else:
    # id = db.Column(db.Integer, primary_key=True)
    # content = db.Column(db.Text, nullable=False)
    # reply_time = db.Column(db.DateTime)
    # # 一(User)对多(Reply)
    # user_id = db.Column(db.Integer, db.ForeignKey('user.ID'))
    # # 一(Topic)对多(Reply)
    # topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'))
    reply = Reply()
    reply.content = request.form["content"]
    reply.reply_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    reply.user_id = session["id"]
    reply.topic_id = request.form["article"]
    db.session.add(reply)
    return redirect("/")





@main.route("/time")
def time_views():
  if "id" in session and "loginname" in session:
    categories = Category.query.all()
    topics = Topic.query.all()
      # 已经登录过从数据库中获取登录信息

    id = session["id"]
    user = User.query.filter_by(ID=id).first()
    return render_template("time.html",params = locals())
  else:
    return redirect("/login")

@main.route("/photo")
def photo_views():
  if "id" in session and "loginname" in session:
    categories = Category.query.all()
    topics = Topic.query.all()
    # 已经登录过从数据库中获取登录信息
    id = session["id"]
    user = User.query.filter_by(ID=id).first()
    return render_template("photo.html", params=locals())
  else:
    return redirect("/login")

@main.route("/about")
def about_views():
  if "id" in session and "loginname" in session:
    categories = Category.query.all()
    topics = Topic.query.all()
    # 已经登录过从数据库中获取登录信息
    id = session["id"]
    user = User.query.filter_by(ID=id).first()
    return render_template("about.html", params=locals())
  else:
    return redirect("/login")

@main.route("/gbook")
def gbook_views():
  if "id" in session and "loginname" in session:
    categories = Category.query.all()
    topics = Topic.query.all()
    # 已经登录过从数据库中获取登录信息
    id = session["id"]
    user = User.query.filter_by(ID=id).first()
    return render_template("gbook.html", params=locals())
  else:
    return redirect("/login")