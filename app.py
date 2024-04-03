import os
import datetime
from datetime import *
import zipfile
from flask import Flask, request, render_template, send_file, make_response,url_for,redirect,Response

app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False

# 开始
@app.route('/')
def index():
    return '开始'

# 传入参数
@app.route('/1/<info>/')
def index1(info):
    args = info.split('+')
    return 'Hello. {}!'.format(args[0])

# 获取路径的查询参数
@app.route('/2/')
def index2():
    uname = request.args.get('uname')
    return 'Hello. {}!'.format(uname)

# 获取表单中的内容
@app.route('/3/', methods=['POST', 'GET'])
def index3():
    if request.method == 'POST':
        uname = request.form.get('uname')
        age = request.form.get('age')
        return 'Hello. {}!,你{}岁'.format(uname, age)
    return render_template('index.html')

# 设置表头和获取响应头的内容
@app.route('/4/', methods=['POST', 'GET'])
def index4():
    resp = make_response('')
    url = request.url
    method = request.method
    headers = request.headers.get('User-Agent')
    cookie = request.cookies.get('uuid')
    return '你访问的网址是{}!{}请求\n请求头为{},uuid为{}'.format(url, method, headers, cookie), 200, resp.set_cookie('username', 'jone', max_age=3600)

# url_for找路由
@app.route('/5/', methods=['POST', 'GET'])
def index5():
    url = url_for('index1',info=128746,address = 'beijinglu')
    return 'url地址为{}'.format(url)

# 重定向
@app.route('/6/')
def index6():
    return redirect(url_for('index7'))

@app.route('/7/')
def index7():
    return f'这是登陆页面'


# return返回的值
@app.route('/8/', methods=['POST', 'GET'])
def index8():
    return {'key':'python语言'}

@app.route('/9/', methods=['POST', 'GET'])
def index9():
    resp = make_response('not found')
    resp.status = 404
    resp.headers['Content-Type'] = 'tsnisaa'
    return resp


# 过滤器的使用
@app.route('/10/', methods=['POST', 'GET'])
def index10():
    data={
        'pasow':10.5,
        'nickname':'john',
    }
    return render_template('index4.html',**data,nicksname=[])

# jinja2模板转义字符过滤器
@app.route('/11/', methods=['POST', 'GET'])
def index11():
    info = '<script>alert("hello")</script>'
    return render_template('index5.html',info=info)

# 自定义内容过滤器
@app.template_filter('cut')
def cutter(value):
    value = value.replace('我是九，你是三，除了你，还是你','你不用好，我喜欢就好')
    return value
@app.route('/12/', methods=['POST', 'GET'])
def index12():
    info = '我是九，你是三，除了你，还是你'
    return render_template('index6.html',info=info)


# 自定义时间过滤器
@app.template_filter('handler_time')
def handler_time(time):
    now = datetime.now()
    temp_stamp = (now-time).total_seconds()
    if temp_stamp < 60:
        return '{:.0f}秒前'.format(temp_stamp)
    elif temp_stamp >= 60 and temp_stamp < 3600:
        return '{:.0f}分钟前'.format(temp_stamp//60)
    elif temp_stamp >= 3600 and temp_stamp < 86400:
        return '{:.0f}小时前'.format(temp_stamp//3600)
    elif temp_stamp >=86400 and temp_stamp < 2592000:
        return '{:.0f}天前'.format(temp_stamp//86400)
    elif temp_stamp >=2592000 and temp_stamp < 31536000:
        return '{:.0f}个月前'.format(temp_stamp//2592000)
    elif temp_stamp >=31536000:
        return '{:.0f}年前'.format(temp_stamp//31536000)
@app.route('/13/', methods=['POST', 'GET'])
def index13():
    tmp_stamp = datetime(1971,1,28,18,18,10)
    return render_template('index7.html',tmp_time=tmp_stamp)

@app.route('/14/',methods=['POST', 'GET'])
def index14():
    user = request.args.get('username')
    return render_template('index8.html',username=user)


@app.route('/15/',methods=['POST', 'GET'])
def index15():
    return render_template('index9.html')





# 上传文件
@app.route('/upload/', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        fname = f.filename
        if not os.path.exists('upload'):
            os.makedirs('upload')
        f.save(os.path.join('upload', fname))
        fnma = os.listdir(os.path.join('upload'))
        return render_template('index1.html', fnma=fnma)
    return render_template('index1.html')

# 下载文件
@app.route('/download/', methods=['POST', 'GET'])
def download():
    if request.method == 'POST':
        fname = request.form.getlist('download')
        if len(fname) == 1:
            filpaths = os.path.join('upload', fname[0])
            if request.form.get('openjpg'):
                return send_file(filpaths, as_attachment=False)
            else:
                return send_file(filpaths, as_attachment=True)
        elif len(fname) == 0:
            return '未勾选文件'
        else:
            zip_filename = '下载.zip'
            with zipfile.ZipFile(zip_filename, 'w') as zipf:
                for file in fname:
                    filpath = os.path.join('upload', file)
                    zipf.write(filpath, arcname=file)
            return send_file(zip_filename, as_attachment=True)

    fnma = os.listdir(os.path.join('upload'))
    return render_template('index2.html', fnma=fnma)

if __name__ == '__main__':
    app.run()
