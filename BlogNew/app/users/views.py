#处理与用户业务逻辑相关的视图和路由
from . import users
from .. import db
from ..models import *
from flask import render_template,request,session,redirect

@users.route("/login",methods=["GET","POST"])
def login_views():
    if request.method == "GET":
        return render_template("login.html")
    else:
        #接受前端传递过来的用户名和密码
        loginname = request.form["username"]
        upwd = request.form["password"]
        #查询数据库，验证用户名和密码
        user=User.query.filter_by(loginname=loginname,upwd=upwd).first()
        #根据结果保存进ｓｅｓｓｉｏｎ
        if user:
            session["id"] = user.ID
            session["loginname"] = loginname
            return redirect("/")
        else:
            return redirect("/login")

@users.route("/register",methods=["GET","POST"])
def register_views():
    if request.method == "GET":
        return render_template("register.html")
    else:
        #接受前端传递过来的用户名和密码
        username = request.form["username"]
        user = User.query.filter_by(loginname=username).first()

        email = request.form["email"]
        password = request.form["password"]
        upassword = request.form["upassword"]
        #查询数据库,是否已有该用户
        user=User.query.filter_by(loginname=username).first()
        print(user)
        if user:
            return render_template("register.html",MSG1="用户名已存在")
        if password != upassword:
            return render_template("register.html", MSG2="两次密码输入不相同")
        else:
            u = User()
            u.loginname = username
            u.uname = username
            u.email = email
            u.upwd = upassword
            db.session.add(u)
            return redirect("/login")

@users.route("/logout", methods=["GET", "POST"])
def logout_views():
    session.clear()
    return redirect("/login")


        # if username and password and cpassword:
    #   olduser = UserInfo.objects.filter(username=username)
    #   if olduser:
    #     return render(request, 'register.html', {'msg':"该用户已经存在"})
    #   if password != cpassword:
    #     return render(request, 'register.html', {"msg":"两次密码不一致"})
    #   newpassword = make_password(password, None, 'pbkdf2_sha1')
    #   # 参1:加密的密码, 参2:任意的字符串 参3:加密方式
    #   # 得到的是一串随机的字符串,并且每次生成都不一样
    #   try:
    #     UserInfo.objects.create(username=username, password=newpassword)
    #   except DatabaseError as e:
    #     logging.warning(e)
    #   return render(request, 'register.html', {'msg':"注册成功"})
    # else:
    #   return render(request, 'register.html', {'msg':"输入项不能为空"})

