from threading import Thread

from flask import current_app, render_template
from flask_mail import Mail, Message

def thread_task(app,mail,msg):
    with app.app_context():
        try:
            result = mail.send(msg)
        except Exception as e:
            print(str(e))
            return False
        else:
            print(result)
            return True

def send_mail(to,subject,filename,**kwargs):
    """

    :param to: 收件人
    :param subject: 邮件主题
    :param filename: 邮件正文对应的html名称
    :param kwargs: 关键字参数，模板中需要的变量名
    :return:
    """
    # 初始化mail对象,一定要先配置邮件信息
    app = current_app._get_current_object()
    # 初始化mail对象,一定要先配置邮件信息
    mail = Mail(app)
    msg = Message(subject=subject,
                  sender='wangtuo1115@163.com',
                  recipients=to)
    # 邮件正文内容为后者,也就是html的内容
    # msg.body = info
    msg.html = render_template(filename + '.html',**kwargs)

    # 启动多线程执行邮件发送的任务
    thread = Thread(target=thread_task, args=(app,mail,msg))
    thread.start()

    return  thread