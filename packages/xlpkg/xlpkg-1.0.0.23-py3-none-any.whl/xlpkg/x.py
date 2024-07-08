import re,os,sys,time,json,string,logging,pymysql,webbrowser, random, inspect, urllib3, binascii, hashlib, datetime,glob
import pandas as pd
from dbutils.pooled_db import PooledDB
from operator import itemgetter
from collections import OrderedDict
from pathlib import Path

from PyQt6.QtWidgets import *
#from selenium import webdriver
from collections.abc import Iterable,Iterator,ItemsView
from sshtunnel import SSHTunnelForwarder

#import request

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler as FSEH


#设置窗体居中显示
def f_setcenter(w,h):
    # 获取主屏幕的信息
    from PyQt5.QtGui import QScreen
    screen = QApplication.primaryScreen()

    # 获取屏幕的分辨率（宽度和高度）
    screen_size = screen.size()

    # 计算窗口的初始位置（屏幕中心）
    width, height = 400, 300
    x = (screen_size.width() - width) // 2
    y = (screen_size.height() - height) // 2

    # 使用self.setGeometry()设置窗口的初始位置和大小
    self.setGeometry(x, y, width, height)
    x=(screen)
    pass

#将多个空格替换成一个空格,删除前导及结尾空格
def f_replace_space(s,type=0):
    match type:
        case 0:
            while '  ' in s:
              s=s.replace('  ',' ').strip()
            return(s)
        case 1:
            return(''.join(s.split()).strip())

        case 2:
            return(re.sub(r'\s+',' ',s).strip())
    pass
# 获取combobox选定项的文本
def f_getcombtext(self, combo):
    text = combo.currentText()
    return (text)


# 为combobox添加项目
def f_add_item(self,cb, items):
    for i in items.values():
        cb.addItem(i)
    pass


#字典键值互换
def f_dictkv(d0,flag=0):
    # d0创建原始字典
    d1={}
    # 字典推导式互换键值
    if flag==0:
        d1 = {v: k for k, v in d0.items()}
    #zip解压
    elif flag==1:
        d1 = dict(zip(d0.values(), d0.keys()))
    #for循环遍历
    elif flag ==2:
        for k, v in d0.items():
            d1[v] = k
    #for循环键不唯一时
    elif flag==3:
        from collections import defaultdict
        d1=defaultdict(list)
        for k,v in d0.items():
            d1[v].append(k)
        pass
    return(d1)


#获取列名
def f_colnames(cur):
    col_names = [i[0] for i in cur.description]
    d = {}
    for i in range(len(col_names)):
        d[str(i)] = col_names[i]
    titles = (d.items())
    return(titles)
    pass
def f_locustrun(webhost='127.0.0.1',webport=8088):
    fpath = os.path.abspath(__file__)
    #os.system(f'locust -f {fpath} --web-host=127.0.0.1')
    cmd=''
    cmd+=f'locust -f {fpath} --web-host={webhost} --web-port={web-port}'
    #os.system(f"locust -f {fpath} --web-host=127.0.0.1 --web-port=8088")
    os.system(cmd)
    pass

#显示字体颜色
def f_c(n=0):
    color='\033['+str(n)+'m'
    return(color)
    pass

#显示字体颜色
def f_color(n=0):
    color='\033['+str(n)+'m'
    return(color)
    pass

#封装f_color
def f_ptitle(n=31,msg=''):
    print(f_color(n), msg, f_color(0))
    pass

#获取指定第3方包可用版本号
def f_getpackversion(packname):
    cmd=r"pip index versions "+packname
    return(os.system(cmd))
    pass

#当前文件名(绝对路径)
def f_curfile():
    return(os.path.abspath(__file__))
    pass

#监控指定目录及子目录下的文件变化情况。
class CFSEH(FSEH):
    def on_any_event(self, event,type=1):
        f=open(r'd:\soft\kafka3.6\logs\watchdir.txt', 'a')
        if type==1:
            f.write('')
            pass
        else:
            #print(str(()),"事件类型:", event.event_type)
            if event.is_directory:
                return None
            elif event.event_type == 'created':
                f.write(str(f_dt()),"事件类型:", event.event_type,"新建: %s" % event.src_path)
                print(str(f_dt()),"事件类型:", event.event_type,"新建: %s" % event.src_path)
            elif event.event_type == 'modified':
                f.write(str(f_dt()),"事件类型:", event.event_type,"新建: %s" % event.src_path)
                print(str(f_dt()),"事件类型:", event.event_type,"修改: %s" % event.src_path)
            elif event.event_type == 'deleted':
                f.write(str(f_dt()),"事件类型:", event.event_type,"新建: %s" % event.src_path)
                print(str(f_dt()),"事件类型:", event.event_type,"删除: %s" % event.src_path)
            elif event.event_type == 'moved':
                f.write(str(f_dt()),"事件类型:", event.event_type,"新建: %s" % event.src_path)
                print(str(f_dt()),"事件类型:", event.event_type,"移动: %s" % event.src_path)
            elif event.event_type == 'renamed':
                f.write(str(f_dt()),"事件类型:", event.event_type,"新建: %s" % event.src_path)
                print(str(f_dt()),"事件类型:", event.event_type,"重命名: %s" % event.src_path,event.dst_path)
        pass
    pass

def f_watchdir(path):
    #path = '/your/folder/path'  # 将路径替换为要监控的文件夹路径
    event_handler = CFSEH()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    pass

# 获取my_function函数的参数信息
def f_getfunparam(fun_name):
    parameters = inspect.signature(fun_name).parameters
    p1=[]
    p2=[]
    p3=[]
    for name, param in parameters.items():
        print("参数名称:", name,"类型注释:", param.annotation,"默认值:", param.default)
        p1.append(name)
        p2.append(param)
        p3.append(param.default)
    return(p1,p2,p3)
    pass

#解析列表转换为json
def f_jsonparse(datas, result='', n=0,p=0):
    for data in re.split('(\{|\[|\]|\}|,)', datas):
        data = re.sub(r'^\s+|\s+$', '', data)	# 为了更大程度地兼容，保证列对齐
        if data == '':
            continue
        elif data == ',':
            result = result + data
            continue
        elif re.match('^\"', data):
            innerList = re.split('(,)', data)
            inner_row = 0
            for data2 in innerList:
                tabs = n * '\t'
                result = result + f'\n{tabs}{data2}'
                inner_row += 1
            continue
        elif re.match('[\{\[]', data):
            result = result + data
            n += 1
            continue
        elif re.match('[\}\]]', data):
            n -= 1
            tabs = n * '\t'
            result = result + f'\n{tabs}{data}'
            continue
        else:
            result = result + f'{data}'
            continue
    if p!=0:
        print(result)
        return(result)
    else:
        return(result)
pass

#对象占用内存大小(字节数)
def f_getmemsize(obj):
    return(sys.getsizeof(obj))
    pass

#格式化显示json数据
def f_json(jsondata,i=4,s=True):
    ret=json.dumps(jsondata,indent=i,sort_keys=s)
    return(ret)
    pass

#MD5
def f_md5(s):
    obj = hashlib.md5(s.encode())
    md5 = obj.hexdigest()
    return(md5.upper())
    pass

def f_success(r,d):
    success=r.json()['success']
    print('success:',success,'elapsed:',str(round(r.elapsed.total_seconds()*1000,2)).zfill(10),d,'\033[0m')
    pass

#时间戳
def f_ts(n=10):
    match n:
        case 10:
            return(str(int(round(time.time()))))
        case 13:
            return(str(int(round(time.time()*1000))))
    pass

#时间戳转日期时间
def f_ts2dt(ts,n=0):
    dt=datetime.datetime.fromtimestamp(ts)
    ret=''
    match n:
        case 0:
            ret=dt.strftime('%Y-%m-%d %H:%M:%S')
        case 1:
            ret = dt.strftime('%Y-%m-%d')
        case 2:
            ret = dt.strftime('%H:%M:%S')
    return(ret)
    pass

#日期时间字符串转日期
def f_str2dt(dt_str,n=0):
    ret=''
    match n:
        case 0:
            frm='%Y-%m-%d %H:%M:%S'
            ret=datetime.strptime(dt_str,fmt)
        case 1:
            frm = '%Y-%m-%d'
            ret = datetime.strptime(dt_str, fmt)
        case 2:
            frm='%H:%M:%S'
            ret = datetime.strptime(dt_str, fmt)
    return(ret)
    pass

#日期时间转时间戳
def f_dt2ts(dt,n=0):
    ts=datetime.datetime.fromtimestmp(ts)
    ret=''
    match n:
        case 0:
            ret=dt.strftie('%Y-%m-%d %H:%M:%S')
        case 1:
            ret = dt.strftie('%Y-%m-%d')
        case 2:
            ret = dt.strftie('%H:%M:%S')
    return(ret)
    pass
#header 签名算法
def f_header_sign(token,d,k):
    x=''
    s=''
    for i,j in d.items():
        x+=(i+'='+j+'&')
    print(x[:-1])
    s+=x
    s += k['cid']
    s += str(k['ts'])
    s += k['cv']
    s += token
    s += k['sk']
    print('string9999:' + s)
    obj = hashlib.md5(s.encode())
    sign = obj.hexdigest()
    return(sign)
    pass

#签名算法
def f_sign(d,k):
    x0 = ''
    x1 = ''
    x2 = ''
    signkey = ''
    for i, j in d.items():
        x0 += (i + '=' + j + '&')
    #print(x0[:-1])
    for i, j in k.items():
        if (i == 'sk'):
            signkey = j
        x1 += j
    x2 = x0[:-1] + x1
    sign=f_md5(x2)
    #print(x1)
    #print(x2)
    #print('signkey:', signkey)
    #print('【签名字符串】',x3)
    return (sign)
    pass

#获取token(仅适用于用户和商家)
def f_gettoken(resp,n=1):
    token=''
    match n:
        case 1|2:
            token=resp.json()['data'].get('token')
        case 3:
            token=resp.json()['appuser'].get('token')
    return(token)
    pass

#获取token(仅适用于骑手)
def f_getdrivertoken(resp):
    token=resp.json()['appuser'].get('token')
    return(token)
    pass

def f_elapsedlogin(resp,n):
    role=''
    token=''
    elapsed = resp.elapsed.total_seconds() * 1000
    # print('token:' + token)
    token=f_gettoken(resp,n)
    match n:
        case 1:
            role='用户'
        case 2:
            role = '商家'
        case 3:
            role = '骑手'
    #print(str(n)+'.'+role+'登录成功! elapsed:', str(round(elapsed, 2)).zfill(10)+' ms','token:',token)
    print(str(n)+'.'+role+'登录成功! elapsed:', str(round(elapsed, 2)).zfill(10)+' ms')
    pass

#获取respsone的请求头
def f_getheader(resp):
    header=resp.headers
    return(header)
    pass

#生成secrety_key
def f_secretykey(n):
    ret=None
    if type(n)==int and int(n)>0:
        ret=(binascii.hexlify(os.urandom(n))).decode()
    else:
        ret='参数必须为整数且大于0!'
    return(ret)
    pass

def f_secretykey1(n):
    ret=None
    if(type(n)==int and int(n)>0):
       ret=hashlib.md5(os.urandom(n)).hexdigest()
    else:
        ret = '参数必须为整数且大于0!'
    return (ret)
    pass
def f_resphead(resp):
    return(resp.request.headers)
    pas
    s

#dict 转json
def f_d2j(d):
    return(json.dumps(d))
    pass

#json转dict
def f_j2d(j):
    return(json.loads(j))
    pass

#接口耗时(毫秒)
def f_toms(elapsed):
    return(elapsed.total_seconds()*1000)
    pass
#获取指定对象的方法
def f_getmethod(obj):
    method=[]
    for i in dir(obj):
        if re.match('^__',i) or (re.match('__$',i)): #排除以__开头和结尾的。
            pass
        else:
            method.append(i)
    return(method)
    pass


def f_exit(self, event):
    r0 = QMessageBox.question(self, "提示", "确定退出?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
    if r0 == QMessageBox.StandardButton.Yes:
        r1 = QMessageBox.question(self, "提示", "再次确定退出?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if r1 == QMessageBox.StandardButton.Yes:
            sys.exit()
        else:
            print('No')
    pass

#按字典键排序
def f_sort_dict_bykey(d):
    return(dict(sorted(d.items(), key=lambda x: x[0])))
    pass

def f_sort_dict_bykey1(d):
    return(dict(sorted(d.items(), key=itemgetter(0))))
    pass

def f_sort_dict_bykey2(d):
    return(dict(OrderedDict(sorted(d.items(), key=lambda x:x[0]))))
    pass

#按字典值排序
def f_sort_dict_byval(d):
    return(dict(sorted(d.items(),key=lambda x:x[1])))
    pass

def f_sort_dict_byval1(d):
    return(dict(sorted(d.items(), key=lambda x:x[1])))
    pass

def f_sort_dict_byval2(d):
    return(dict(OrderedDict(sorted(d.items(), key=lambda x:x[1]))))
    pass

#文件对话框
class Filedialog(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        b_01 = QPushButton("OK", self)

        self.resize(800, 600)
        self.show()
        b_01.clicked.connect(self.f_ok)

    def f_ok(self):
        fname, _ = QFileDialog.getOpenFileName(self, "Open file", '/', "Images(*.jpg *.gif)")
        print(fname)

#关于
def f_msgabout(msg):
    QMessageBox.about('about',msg)
    pass

#错误
def f_msgcritical(msg):
    QMessageBox.critical('Error',msg)
    pass

#警告
def f_msgwarn(msg):
    QMessageBox.warning('Warn',msg)
    pass

#消息
def f_msginfo(msg):
    QMessageBox.information('Info',msg)
    pass

#消息
def f_msgquestion(msg):
    QMessageBox.question('Question',msg)
    pass

#import request
'''
mysql show 命令用法
#1、 显示MySQL上的Binlog文件信息
SHOW BINARY LOGS; 或者 SHOW MASTER LOGS; #
#2、 显示Binlog文件中的event，可以指定具体的Binlog文件，开始的位置，偏移等
SHOW BINLOG EVENTS [IN 'log_name'] [FROM pos] [LIMIT [offset,] row_count]
#3、 显示所有可用的字符集
SHOW CHARACTER SET [LIKE'pattern' |WHERE expr]
#4、 显示所有支持的字符集校验规则
SHOW COLLATION [LIKE'pattern' | WHERE expr]
#5、 显示一个表的字段信息
SHOW [FULL] {COLUMNS | FIELDS} {FROM | IN} tbl_name [{FROM | IN} db_name] [LIKE 'pattern' | WHERE expr]
6、 显示指定库的建库语句
SHOW CREATE {DATABASE | SCHEMA} [IF NOT EXISTS] db_name
#7、 显示指定事件的创建语句
SHOW CREATE EVENT event_name
#8、 显示指定函数的创建语句
SHOW CREATE FUNCTION func_name
#9、 显示指定存储过程的创建语句
SHOW CREATE PROCEDURE proc_name
10、 显示指定表的建表语句
SHOW CREATE TABLE tbl_name
#11、 显示指定触发器的创建语句
SHOW CREATE TRIGGER trigger_name
#12、 显示指定用户的创建语句
SHOW CREATE USER user
#13、 显示指定视图的创建语句
SHOW CREATE VIEW view_name
#14、 显示数据库名称
SHOW {DATABASES | SCHEMAS} [LIKE 'pattern' | WHERE expr]
#15、 显示指定存储引擎运行时的快照信息
SHOW ENGINE engine_name {STATUS | MUTEX}
#16、 显示支持的所有存储引擎
SHOW [STORAGE] ENGINES
#17、 显示错误信息和错误个数，SHOW COUNT(*) ERRORS 等同于 SELECT @@error_count;
SHOW ERRORS [LIMIT [offset,] row_count]， SHOW COUNT(*) ERRORS
#18、 显示事件管理器中的事件
SHOW EVENTS [{FROM | IN} schema_name] [LIKE 'pattern' | WHERE expr]
#19、 显示指定函数的函数代码
SHOW FUNCTION CODE func_name
#20、 显示指定函数的状态信息
SHOW FUNCTION STATUS [LIKE 'pattern' | WHERE expr]
#21、 显示指定用户的授权信息
SHOW GRANTS [FOR user]
#22、 显示表的索引信息
SHOW {INDEX | INDEXES | KEYS} {FROM | IN} tbl_name [{FROM | IN} db_name] [WHERE expr]
#23、 显示主库的Binlog日志信息
SHOW MASTER STATUS
#24、 显示表缓存中打开的非临时表信息
SHOW OPEN TABLES [{FROM | IN} db_name] [LIKE 'pattern' | WHERE expr]
#25、 显示已安装的插件信息
SHOW PLUGINS
#26、 显示支持的所有权限信息
SHOW PRIVILEGES
#27、 显示指定存储过程的代码信息
SHOW PROCEDURE CODE proc_name
#28、 显示指定存储过程的状态信息
SHOW PROCEDURE STATUS [LIKE 'pattern' | WHERE expr]
#29、 显示线程快照信息
SHOW [FULL] PROCESSLIST
#30、 显示当前会话的SQL语句的资源使用情况
SHOW PROFILE [type [, type] ... ] [FOR QUERY n] [LIMIT row_count [OFFSET offset]]
#31、 显示当前会话多个SQL语句的执行耗时
SHOW PROFILES
#32、 显示relay log文件中的event，可以指定具体的relay log文件，开始的位置，偏移等。
 SHOW RELAYLOG EVENTS [IN 'log_name'] [FROM pos] [LIMIT [offset,] row_count] [channel_option]
#33、 显示当前主库上注册的从库信息
SHOW SLAVE HOSTS
#34、 显示从库的复制信息
SHOW SLAVE STATUS [FOR CHANNEL channel]
#35、 显示MySQL的状态变量
SHOW [GLOBAL | SESSION] STATUS [LIKE 'pattern' | WHERE expr]
#36、 显示指定表的状态信息
SHOW TABLE STATUS [{FROM | IN} db_name] [LIKE 'pattern' | WHERE expr]
#37、 显示指定库中的所有表信息
SHOW [FULL] TABLES [{FROM | IN} db_name] [LIKE 'pattern' | WHERE expr]
#38、 显示指定库中的所有触发器信息
kSHOW TRIGGERS [{FROM | IN} db_name] [LIKE 'pattern' | WHERE expr]
#39 显示MySQL所有系统变量信息
SHOW [GLOBAL | SESSION] VARIABLES [LIKE 'pattern' | WHERE expr]
#40 显示警告信息和警告个数， SHOW COUNT(*) WARNINGS 等同于 SELECT @@warning_count;
SHOW WARNINGS [LIMIT [offset,] row_count]， SHOW COUNT(*) WARNINGS
'''
code_ok=200
success_ok=True

#本地数据库
config_local = \
{
    'user': 'root',
    'passwd': '000000',
    'host': '127.0.0.1',
    'port': 3306,
    'db': 'mysqldemo',
    'charset':'utf8',
    'cursorclass': 'cursors.DictCursor',
    'autocommit' : True
}

config_wdms = \
    {
        'user': 'test',
        'passwd': 'test@123',
        'host': '172.18.2.135',
        'port': 3306,
        'db': 'wdms',
        'charset': 'utf8',
        'cursorclass': 'cursors.DictCursor',
        'autocommit': True
    }

config_devops = \
    {
        'user': 'test',
        'passwd': 'test@123456',
        'host': 't3nod1ciqw0bkmo.oceanbase.aliyuncs.com',
        'port': 3306,
        'db': 'runfast_devops',
        'charset': 'utf8',
        'cursorclass': 'cursors.DictCursor',
        'autocommit': True
    }

#字典按键/值升序/降序排序后返回新的字典
#s=false:key正序
#s=True:key反序
def f_dictsort(dict0,k=0,rev=False):
    d=sorted(dict0.items(),key=lambda d:d[k],reverse=rev)
    return(dict(d))
    pass

#列表转元组
def f_list2tuple(lst):
    return(tuple(lst))
    pass

#元组转列表
def f_tuple2list(tup):
    return(list(tup))
    pass

#列表转集合
def f_list2set(lst):
    return(set(lst))
    pass

#元组转集合
def f_tuple2set(tup):
    return(set(tup))
    pass

#集合转列表
def f_set2list(set1):
    return(list(set1))
    pass

#集合转元组
def f_set2tuple(set1):
    return(tuple(set1))
    pass

#字典转列表
def f_dict2list(dict):
    lst=[]
    for k,v in dict.items():
        lst.append((k,v))
    return(lst)
    pass

#字典转元组
def f_dict2tuple(dict):
    lst=[]
    for k,v in dict.items():
        lst.append((k,v))
    return(tuple(lst))
    pass

def f_combadditem(comb,sql,col):
    lst = ['云南', '贵州', '四川', '广西', '湖南', '湖北', '河南', '河北', '广东', '广西', '山东', '山西']
    # for i in lst:
    #     self.cb_id.addItem(i)
    try:
        with f_conn_local() as conn:
            with conn.cursor(cursor=pymysql.cursors.DictCursor) as cur:
                row = cur.execute(sql)
                r = cur.fetchall()
                for i in r:
                    print("J:", i[col])
                    # comb.addItem(str(j["id"]))
                    comb.addItem(str(i[col]))
    except Exception as e:
        print(e)
    pass

def f_jsoncontains(conn):
    try:
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            sql='select id,json_contains(c_json, \'{"name":"xiaolong"}\') x from t_json;'
            row=cur.execute(sql)
            r=cur.fetchall()
            print(r)
    except Exception as e:
        print(e)
    pass

def f_jsonsearch(conn,type='all'):
    try:
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            if type.lower()=='all':
                sql='select id,json_search(c_json,\'all\', \'xiaolong\') x from t_json;'
            elif type.lower()=='one':
                sql='select id,json_search(c_json,\'one\', \'xiaolong\') x from t_json;'

            row=cur.execute(sql)
            r=cur.fetchall()
            print(r)
    except Exception as e:
        print(e)
    pass

def f_jsonpretty(conn):
    try:
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            sql='select id,json_pretty(c_json) from t_json where c_json->"$.name"=\'xiaolong\';'
            row=cur.execute(sql)
            r=cur.fetchall()
            print(r)
    except Exception as e:
        print(e)
    pass

def f_jsondepth(conn):
    try:
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            sql='select id,concat(\'c_json: \',json_depth(c_json)) depth from t_json ;'
            row=cur.execute(sql)
            r=cur.fetchall()
            print(r)
    except Exception as e:
        print(e)
    pass

def f_jsonlength(conn):
    try:
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            sql='select id,concat(\'c_json: \',json_length(c_json)) length from t_json ;'
            row=cur.execute(sql)
            r=cur.fetchall()
            print(r)
    except Exception as e:
        print(e)
    pass

def f_jsonkeys(conn):
    try:
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            sql='select id,concat(\'c_json: \',json_keys(c_json)) `keys` from t_json ;'
            row=cur.execute(sql)
            r=cur.fetchall()
            print(r)
    except Exception as e:
        print(e)
    pass

def f_jsonremove(conn):
    try:
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            sql='select json_remove(c_json, \'$.addr[0].office[0].city\') x from t_json where id = 1';
            row=cur.execute(sql)
            r=cur.fetchall()
            print(r)
    except Exception as e:
        print(e)
    pass

def f_jsonreplace(conn):
    try:
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            sql='select json_replace(c_json, \'$.addr[0].office[0].city\',\'9999\') x from t_json where id = 1';
            row=cur.execute(sql)
            r=cur.fetchall()
            print(r)
    except Exception as e:
        print(e)
    pass

def f_jsonset(conn):
    try:
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            sql='select json_set(c_json, \'$.addr[0].office[0].city[0]\', \'林和街道\') from t_json where id = 1;'
            row=cur.execute(sql)
            r=cur.fetchall()
            print(r)
    except Exception as e:
        print(e)
    pass

def f_jsonextract(conn):
    try:
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            sql='select json_extract(c_json, \'$.addr[0].office[0].city[0]\') `jsonextract` from t_json where id = 1;'
            row=cur.execute(sql)
            r=cur.fetchall()
            print(r)
    except Exception as e:
        print(e)
    pass

def f_jsoninsert(conn):
    try:
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            sql='select json_insert(\'{"street":"林和街道"}\', "$.age", 25, "$.physics", 98) json_insert from t_json where c_json->\'$.name\' = \'xiaolong\';'
            row=cur.execute(sql)
            r=cur.fetchall()
            print(r)
    except Exception as e:
        print(e)
    pass

def f_jsonarray(conn):
    try:
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            sql='select json_array(\'speed\', \'dinneer\', \'art\', 43, date(now()), curtime(), \'quick\', c_json->\'$.name\') x from t_json where c_json->\'$.name\'=\'xiaolong\';'
            row=cur.execute(sql)
            r=cur.fetchall()
            print(r)
    except Exception as e:
        print(e)
    pass

def f_jsonquote(conn):
    sql='''
    select json_quote("[1,2,3,4,5,6]") x ,json_quote('null') x1,json_quote('"null"') x2 ,json_quote("") x3,json_quote('') x4,json_quote(null) x5 from t_json where c_json->'$.name'='xiaolong';
    '''
    print('sql:',sql)
    try:
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            #sql='select json_array(\'speed\', \'dinneer\', \'art\', 43, date(now()), curtime(), \'quick\', c_json->\'$.name\') x from t_json where c_json->\'$.name\'=\'xiaolong\';'
            row=cur.execute(sql)
            r=cur.fetchall()
            print(r)
    except Exception as e:
        print(e)
    pass

def f_jsoncontains_path(conn):
    sql1='''
        select json_contains_path(c_json, 'all', '$.name', '$.addr') x from t_json where c_json->'$.name'='xiaolong';
    '''
    sql2='''
    select json_contains_path(c_json, 'all', '$.name1', '$.addr') x from t_json where c_json->'$.name'='xiaolong';
    '''
    sql3='''
    select json_contains_path(c_json, 'all', '$.name1', '$.addr1') x from t_json where c_json->'$.name'='xiaolong';
    '''
    sql4='''
    select json_contains_path(c_json, 'one', '$.name', '$.addr') x from t_json where c_json->'$.name'='xiaolong';
    '''
    sql5='''
    select json_contains_path(c_json, 'one', '$.name1', '$.addr') x from t_json where c_json->'$.name'='xiaolong';
    '''
    sql6='''
    select json_contains_path(c_json, 'one', '$.name1', '$.addr1') x from t_json where c_json->'$.name'='xiaolong';
    '''
    try:
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            #sql='select json_array(\'speed\', \'dinneer\', \'art\', 43, date(now()), curtime(), \'quick\', c_json->\'$.name\') x from t_json where c_json->\'$.name\'=\'xiaolong\';'
            row=cur.execute(sql1)
            r=cur.fetchall()
            print(r)
            row=cur.execute(sql2)
            r=cur.fetchall()
            print(r)
            row=cur.execute(sql3)
            r=cur.fetchall()
            print(r)
            row=cur.execute(sql4)
            r=cur.fetchall()
            print(r)
            row=cur.execute(sql5)
            r=cur.fetchall()
            print(r)
            row=cur.execute(sql6)
            r=cur.fetchall()
            print(r)
    except Exception as e:
        print(e)
    pass

def f_jsonprint():
    try:
        sql='''
        select json_quote("[1,2,3,4,5,6]") x ,json_quote('null') x1,json_quote('"null"') x2 ,json_quote("") x3,json_quote('') x4,json_quote(null) x5 from t_json where c_json->'$.name'='xiaolong';
        '''
        print('sql:',sql)
    except Exception as e:
        print(e)
    pass

def f_jsonvalid(conn):
    try:
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            sql='select json_valid(c_json->\'$.addr\') , json_valid(\'name\') , json_valid(null)  from t_json where id=1; '
            row=cur.execute(sql)
            r=cur.fetchall()
            print(r)
    except Exception as e:
        print(e)
    pass

def f_getcode():
    return(''.join(random.sample(string.ascii_letters+string.digits+string.punctuation,32)))
    pass

def f_getcode1():
    return(''.join(random.sample(string.ascii_letters+string.digits,32)))
    pass

#切换数据库
def f_switchdb(conn,db):
    try:
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            sql = 'use '+db+';'
            cur.execute(sql)
    except Exception as e:
        print(e)
    pass

#创建科目表
subject= ['chinese', 'math', 'english', 'physics', 'chemistry', 'biology', 'geography', 'politics', 'history', 'sport']

t_subject="""create table t_subject(id int not null auto_increment primary key comment 'id',`name` varchar(20) not null unique comment'学科'); """
t_teacher="""create table t_teacher
(id int not null auto_increment primary key comment 'id',
	`name` varchar(20) not null unique comment '姓名',
	sex int not null default 2 comment'性别',
	subjectid json comment'所教学科'
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
"""

t_student=""" create table t_student
(
	id int not null auto_increment primary key comment 'id',
	student_id varchar(20) comment '学号',
	class varchar(20) not null  comment'年级',
	`name` varchar(20) not null unique comment'姓名',
	sex int comment '性别'
) ENGINE=MyISAM  DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
"""

t_score="""CREATE TABLE `t_score` 
(
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `section` varchar(20) DEFAULT NULL COMMENT '考试阶段',
  `grade` int(11) DEFAULT NULL COMMENT '班级',
  `name` varchar(10) DEFAULT NULL COMMENT '姓名',
  `score` json DEFAULT NULL COMMENT '考试成绩',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
"""

def f_show_01(conn):
    try:
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            sql='show binary logs;' #或者show master logs;
            row=cur.execute(sql)
            res=cur.fetchall()
            for i in res:
                print(i)
    except Exception as e:
        print(e)
    pass

def f_show_02(conn):
    try:
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            sql='show binlog events;' #或者show master logs;
            row=cur.execute(sql)
            res=cur.fetchall()
            for i in res:
                print(i)
    except Exception as e:
        print(e)
    pass

def f_show_03(conn):
    try:
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            sql='show character set;'
            row=cur.execute(sql)
            res=cur.fetchall()
            for i in res:
                print(i)
    except Exception as e:
        print(e)
    pass

def f_show_04(conn):
    try:
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            sql='show collation;'
            row=cur.execute(sql)
            res=cur.fetchall()
            for i in res:
                print(i)
    except Exception as e:
        print(e)
    pass

def f_show_14(conn):
    try:
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            sql='show databases;'
            row=cur.execute(sql)
            res=cur.fetchall()
            for i in res:
                print(i)
    except Exception as e:
        print(e)
    pass

def f_show_16(conn):
    try:
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            sql='show engines;' #同'show storage engines;'
            row=cur.execute(sql)
            res=cur.fetchall()
            for i in res:
                print(i)
    except Exception as e:
        print(e)
    pass

def f_show_1701(conn):
    try:
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            sql='show errors;'
            row=cur.execute(sql)
            res=cur.fetchall()
            for i in res:
                print(i)
    except Exception as e:
        print(e)
    pass

def f_show_1702(conn):
    try:
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            sql='show count(*) errors;'
            row=cur.execute(sql)
            res=cur.fetchall()
            for i in res:
                print(i)
    except Exception as e:
        print(e)
    pass

def f_show_1801(conn):
    try:
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            sql='show events;'
            row=cur.execute(sql)
            res=cur.fetchall()
            for i in res:
                print(i)
    except Exception as e:
        print(e)
    pass

def f_show_20(conn):
    try:
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            sql='show function status;'
            row=cur.execute(sql)
            res=cur.fetchall()
            for i in res:
                print(i)
    except Exception as e:
        print(e)
    pass

def f_show_21(conn):
    try:
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            sql='show grants;'
            row=cur.execute(sql)
            res=cur.fetchall()
            for i in res:
                print(i)
    except Exception as e:
        print(e)
    pass

def f_show_23(conn):
    try:
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            sql='show master status;'
            row=cur.execute(sql)
            res=cur.fetchall()
            for i in res:
                print(i)
    except Exception as e:
        print(e)
    pass

def f_show_2401(conn):
    try:
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            sql='show open tables;'
            row=cur.execute(sql)
            res=cur.fetchall()
            for i in res:
                print(i)
    except Exception as e:
        print(e)
    pass

def f_show_25(conn):
    try:
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            sql='show plugins;'
            row=cur.execute(sql)
            res=cur.fetchall()
            for i in res:
                print(i)
    except Exception as e:
        print(e)
    pass

def f_show_26(conn):
    try:
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            sql='show privileges;'
            row=cur.execute(sql)
            res=cur.fetchall()
            for i in res:
                print(i)
    except Exception as e:
        print(e)
    pass

def f_show_28(conn):
    try:
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            sql='show procedure status;'
            row=cur.execute(sql)
            res=cur.fetchall()
            for i in res:
                print(i)
    except Exception as e:
        print(e)
    pass

def f_show_29(conn):
    try:
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            sql='show full processlist;'
            row=cur.execute(sql)
            res=cur.fetchall()
            for i in res:
                print(i)
    except Exception as e:
        print(e)
    pass

def f_show_30(conn):
    try:
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            sql='show profile;'
            row=cur.execute(sql)
            res=cur.fetchall()
            for i in res:
                print(i)
    except Exception as e:
        print(e)
    pass

def f_show_31(conn):
    try:
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            sql='show profiles;'
            row=cur.execute(sql)
            res=cur.fetchall()
            for i in res:
                print(i)
    except Exception as e:
        print(e)
    pass

def f_show_32(conn):
    try:
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            sql='show relaylog events;'
            row=cur.execute(sql)
            res=cur.fetchall()
            for i in res:
                print(i)
    except Exception as e:
        print(e)
    pass

def f_show_33(conn):
    try:
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            sql='show slave hosts;'
            row=cur.execute(sql)
            res=cur.fetchall()
            for i in res:
                print(i)
    except Exception as e:
        print(e)
    pass

def f_show_34(conn):
    try:
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            sql='show slave status;'
            row=cur.execute(sql)
            res=cur.fetchall()
            for i in res:
                print(i)
    except Exception as e:
        print(e)
    pass

def f_show_3501(conn):
    try:
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            sql='show status;' #同 show session status;
            row=cur.execute(sql)
            res=cur.fetchall()
            for i in res:
                print(i)
    except Exception as e:
        print(e)
    pass

def f_show_3502(conn):
    try:
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            sql='show global status;'
            row=cur.execute(sql)
            res=cur.fetchall()
            for i in res:
                print(i)
    except Exception as e:
        print(e)
    pass

def f_show_3601(conn):
    try:
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            sql='show table status;'
            row=cur.execute(sql)
            res=cur.fetchall()
            for i in res:
                print(i)
    except Exception as e:
        print(e)
    pass

def f_show_3602(conn,db_name):
    try:
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            sql='show table status from '+db_name+';'
            row=cur.execute(sql)
            res=cur.fetchall()
            for i in res:
                print(i)
    except Exception as e:
        print(e)
    pass

def f_show_3701(conn):
    try:
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            sql='show tables ;' #同show full tables;
            row=cur.execute(sql)
            res=cur.fetchall()
            for i in res:
                print(i)
    except Exception as e:
        print(e)
    pass

def f_show_3702(conn,db_name):
    try:
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            sql='show tables from '+db_name+' ;'
            row=cur.execute(sql)
            res=cur.fetchall()
            for i in res:
                print(i)
    except Exception as e:
        print(e)
    pass

def f_show_3801(conn):
    try:
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            sql='show triggers ;'
            row=cur.execute(sql)
            res=cur.fetchall()
            for i in res:
                print(i)
    except Exception as e:
        print(e)
    pass

def f_show_3802(conn,db_name):
    try:
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            sql='show triggers from '+db_name+' ;'
            row=cur.execute(sql)
            res=cur.fetchall()
            for i in res:
                print(i)
    except Exception as e:
        print(e)
    pass

def f_show_3901(conn):
    try:
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            sql='show variables ;' #同show session variables;
            row=cur.execute(sql)
            res=cur.fetchall()
            for i in res:
                print(i)
    except Exception as e:
        print(e)
    pass

def f_show_3902(conn):
    try:
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            sql='show global variables;'
            row=cur.execute(sql)
            res=cur.fetchall()
            for i in res:
                print(i)
    except Exception as e:
        print(e)
    pass

def f_show_4001(conn):
    try:
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            sql='show warnings;'
            row=cur.execute(sql)
            res=cur.fetchall()
            for i in res:
                print(i)
    except Exception as e:
        print(e)
    pass

def f_show_4002(conn):
    try:
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            sql='show count(*) warnings;'
            row=cur.execute(sql)
            res=cur.fetchall()
            for i in res:
                print(i)
    except Exception as e:
        print(e)
    pass

#聚合函数
def f_aggregation(conn,sql):
    try:
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            sql ="""
                select grade, count(*) as count, avg(score->'$.chinese') as avg, max(score->'$.chinese') as max, min( score->'$.chinese') as min, sum(score->'$.chinese') as sum from t_score group by grade;
                """
            row = cur.execute(sql)
            res = cur.fetchall()
            for i in res:
                print(i)
    except Exception as e:
        print(e)
    pass

#删除表
def f_droptab(conn,tab_name):
    try:
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            sql='drop table if exists '+tab_name+';'
            cur.execute(sql)
            print(tab_name, '删除成功！')
    except Exception as e:
        print(e)
    pass

#创建表
def f_createtab(conn,tab_name):
    try:
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            if(tab_name.lower()=='t_subject'):
                cur.execute(t_subject)
            elif(tab_name.lower()=='t_teacher'):
                cur.execute(t_teacher)
            elif(tab_name.lower()=='t_student'):
                cur.execute(t_student)
            elif(tab_name.lower()=='t_score'):
                cur.execute(t_score)
            print(tab_name, '创建成功！')
    except Exception as e:
        print(e)
    pass

#清空表
def f_truncatetab(conn,tab_name):
    try:
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            sql='truncate table '+tab_name+';'
            cur.execute(sql)
            print(tab_name, '清空成功！')
    except Exception as e:
        print(e)
    pass

#添加科目表
def f_addsubject(conn,val=[]):
    if(len(val)==0):
        val=subject
    try:
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            sql='insert into t_subject(`name`) values(%s)'
            cur.executemany(sql,val)
    except Exception as e:
        print(e)
    pass

def f_initsubject(conn,tab_name,val=[]):
    f_createtab(conn,tab_name)
    f_addsubject(conn,val)
    pass

#查询数据库
def f_getdatabase(conn):
    try:
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            sql='show databases;'
            cur.execute(sql)
            res=cur.fetchall()
            for i in res:
                print('\t',end='')
                print(i)
    except Exception as e:
        print(e)
    pass

#显示表
def f_gettable(conn,db=[]):
    try:
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            for i in range(len(db)):
                sql='use '+db[i]+';'
                sql='show tables;'
                row=cur.execute(sql)
                res=cur.fetchall()
                print('\033[32m[' + db[i] + ']\033[0m')
                for i in res:
                    print('\t',end=' ')
                    print(i)
    except Exception as e:
        print(e)
    pass

#根据SQL语句获取列名
def f_getcolbysql(conn,sql,flag=0):
    try:
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            row = cur.execute(sql)
            if(flag==0):
                return([i[0] for i in cur.description])
            else:
               for c in [i[0] for i in cur.description]:
                   print(c,end=' ')
               print('')
    except Exception as e:
        print(e)
    pass

#显示指定表的所有列
def f_getcolumn(conn,tab_name=[]):
    try:
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            for i in range(len(tab_name)):
                sql="show columns from "+tab_name[i]+ ";" #同desc table_name
                #print(sql)
                row=cur.execute(sql)
                res=cur.fetchall()
                print('\033[32m['+tab_name[i]+']\033[0m')
                for i in res:
                    print('\t',end='')
                    print(i)
    except Exception as e:
        print(e)
    pass

# select * from information_schema.tables where table_schema = 'mysqldemo' ;
# select * from information_schema.columns where table_schema = 'mysqldemo' and table_name = 't_score' ;

"""
连接池
使用连接池可以提高频繁操作数据库操作效率。Python提供了多种连接池，如：
1、DBUtils：Python数据库连接池工具集，支持多线程和多进程。
2、SQLAlchemy：Python ORM框架，实现了连接池和对象池等高级特性。
"""
def f_poolconn(host='localhost', port=3306, user='root', password='000000', database='mysqldemo', charset='utf8mb4',mincached=5, maxcached=20):
    pool=PooledDB(pymysql,host=host, port=port, user=user, password=password, database=database, charset=charset, mincached=mincached, maxcached=maxcached)
    conn = pool.connection()
    return(conn)
    pass

#查询数据库版本号
def f_getversion(conn):
    try:
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            sql='select version();'
            cur.execute(sql)
            res=cur.fetchone()
            print(res)
    except Exception as e:
        print(e)
        pass
    
class db:
    def __init__(self,p):
        self.host     = p[0]
        self.port     = p[1]
        self.user     = p[2]
        self.password = p[3]
        self.db_name  = p[4]
        self.charset  = p[5]
        pass

    #连接数据库
    def f_conn(self):
        try:
            conn = pymysql.connect(host=self.host,port=self.port,user=self.user, password=self.password, database=self.database,charset=self.chart)
            return(conn)
        except Exception as e:
            print(e)
        pass

    #操作
    def operate(self,conn,sql):
        #conn = pymysql.connect(host=self.host,port=self.port,user=self.user, password=self.password, database=self.database,charset=self.chart)
        #conn=self.f_conn()
        try:
           with conn.cursor(cursor=pymysql.cursors.DictCursor) as cur:
               cur.execute(sql)
               conn.commit()
        except Exception as e:
            print(e)
            #conn.rollback()
        pass

    #查询
    def f_select(self,conn,sql):
        try:
            with conn.cursor(cursor=pymysql.cursors.DictCursor) as cur:
                cur.execute(sql)
                res=cur.fetchall()
                for i in res:
                    print(i)
        except Exception as e:
            print(e)
        pass

    #插入
    def f_insert(self,conn,sql):
        try:
            with conn.cursor(cursor=pymysql.cursors.DictCursor) as cur:
                ret=cur.execute(sql)
                print(ret)
                conn.commit()
        except Exception as e:
            print(e)
            #conn.rollback()
        pass

    #更新
    def f_update(self,conn,sql):
        try:
            with conn.cursor(cursor=pymysql.cursors.DictCursor) as cur:
                ret=cur.execute(sql)
                print(ret)
                conn.commit()
        except Exception as e:
            print(e)
            #conn.rollback()
        pass

    #删除
    def f_delete(self,conn,sql):
        try:
            with conn.cursor(cursor=pymysql.cursors.DictCursor) as cur:
                ret=cur.execute(sql)
                print(ret)
            conn.commit()
        except Exception as e:
            print(e)
            #conn.rollback()
        pass
    pass

# 调用存储过程
'''
args 参数格式 [[arg1],[arg2],[arg3],[arg4],[arg5],[argn],]
args 可用select命令生成
'''
def f_callproc(conn, proc, args=[]):
    try:
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            for i in range(len(args)):
                ret = cur.callproc(proc,args[i])
                res = cur.fetchall()
                conn.commit()
                for j in res:
                    print(j)
    except Exception as e:
        print(e)
        # conn.rollback()
    pass

def f_getarray(conn,proc,args=[]):
    try:
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            ret1= cur.callproc(proc,args)
            print(ret1)
            # res = cur.fetchall()
            # conn.commit()
            # for j in res:
            #     print(j)
    except Exception as e:
        print(e)
        # conn.rollback()
    pass

#生成两个数组的差集
def f_arraydifference(a1,a2):
    return(set(a1)-set(a2))
    pass

#生成两个数组的交集
def f_arrayintersection(a1,a2):
    return(set(a1)&set(a2))
    pass

#生成两个数组的并集
def f_arrayunion(a1,a2,type=1):
    '''
    type 0 :不去重
    type 1:去重
    '''
    if type==0:#不去重
        return(a1 + a2)
    elif type==1:#去重
        return(list(set(a1+a2)))
    pass

#多个数组的并集
def f_arrayunion1(a):
    n=len(a)
    x=a[0]
    for i in range(1,n):
        #print(a[i])
        x=list(set(x)|set(a[i]))
    return(x)
    pass

#生成json列的查询语句
def f_getjsoncol(tab,col,lst,type=0):
    s=[]
    n=''
    k=len(lst)-1
    #print(k)
    for i,j in zip(lst,range(k+1)):
        #print(j,k)
        if j<k:
            s=col+'->>\'$.'+i+'\''+' '+i+ ','
        else:
            s = col + '->>\'$.' + i + '\'' + ' ' + i
        n+=s
    if type==0:
        return(n)
    elif type==1:
        return('select \n\t'+n+'\nfrom '+tab+';')
    elif type==2:
        return('select \n\t'+n+'\nfrom '+' ;')
    elif type==3:
        return(n+'\nfrom '+tab+' ;')
    pass

#对称表排序
def f_sort(lst):
    return(lst.sort())
    pass

#判断对象是否可迭代
def f_isiterable(obj):
    if(isinstance(obj,Iterable)):
        return(True)
    else:
        return(False)
    pass

#判断对象是否迭代器
def f_isiterator(obj):
    if(isinstance(obj,Iterator)):
        return(True)
    else:
        return(False)
    pass

#用webdriver打开网页
def f_openurl0(url):
    wd=webdriver.Chrome()
    wd.get(url)
    time.sleep(5)
    wd.quit()
    pass

#用webbrowser打开网页
def f_openurl(url,new=0,autoraise=True):
    webbrowser.open(url,new=new,autoraise=autoraise)
    pass

#闰年判断
def f_leap(year):
    if(year%4==0 and year%100!=0) or year%400==0:
        return(True) #是闰年
    else:
        return(False) #不是闰年
    pass

#返回当前日期时间
def f_dt1():
    try:
        dt=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return(dt)
    except Exception as e:
        logging.error(e)
    pass

#创建指定数量n的字典
def f_create_dict(n=random.randint(1,10)):
    s='dict={'
    for i in range(1,n+1):
      x='"k'+str(i)+'":'+'"V'+str(i)+'"'
      s+=x+','
    s+='}'
    return(s)
    pass
	
#所有单词首字母大写
def f_title(s):
    return(s.title())
    pass
#字符串首写字母大写
def f_capitalize(s):
    return(s.capitalize())
    pass

#大小写转换
def f_swapcase(s):
	return(s.swapcase())
	pass


#根据经纬度计算配送距离
def f_dis(geo):
    from geopy.distance import geodesic
    #geo={'userLng':'113.370350', 'userLat': '23.010000','senderLng': '113.370350', 'senderLat': '22.979478'}
    lat1 = float(geo['userLat'])
    lon1 = float(geo['userLng'])
    lat2 = float(geo['senderLat'])
    lon2 = float(geo['senderLng'])
    # 创建位置
    l1 = (lat1, lon1)
    l2 = (lat2, lon2)
    dis=geodesic(l1, l2).kilometers
    return(dis)
    pass
#计算多个经纬度之间的直线距离(M)
def f_distance1(x):
    s=0.0
    l=len(x)-1
    for i in range(l):
        d=(f_distance2(x[i],x[i+1]))
        s+=d
    return(round(float(s),4))
    pass

#计算两个经纬度之间的直线距离(M)
def f_distance2(o,n):
    loc1=(o[0],o[1])
    loc2=(n[0],n[1])
    d = distance.distance(loc1,loc2).m
    return(round(float(d),4))
    pass

#转小写
def f_lower(s):
   return(s.lower())
   pass
   
#转大写
def f_upper(s):
	return(s.upper())
	pass

#计算两个经纬度之间的直线距离(M)
def f_distance4(lat1,lng1,lat2,lng2):
    coord1=(lat1,lng1)
    coord2=(lat2,lng2)
    d=geodesic(coord1,coord2).m
    return(round(float(d),4))
    pass

#执行系统命令
def f_cmd(cmd):
	os.system(cmd)
	pass

#清除屏幕
def f_cls():
    os.system('cls')
    pass

#是否目录
def f_isdir(fname):
    ret=os.path.isdir(fname)
    if ret:
        return(True)
    else:
        return(False)
    pass

#是否文件
def f_isfile(fname):
    ret=os.path.isfile(fname)
    if ret:
        return(True)
    else:
        return(False)
    pass

#获取当前工作目录
def f_getcwd():
    return(os.getcwd())
    pass

#执行操作系统命令
def f_cmd(cmd):
    os.system(cmd)
    pass

#返回时间戳
def f_ticks():
    return(time.time())
    pass

#返回日期时间
def f_dt(type=0):
    dt=None
    match type:
        case 0:
            dt= time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        case 1:
            dt=time.strftime('%Y-%m-%d', time.localtime())
        case 2:
            dt = time.strftime('%H:%M:%S', time.localtime())
    return(dt)
    pass

#判断字符串f是否是字符串s的子串
def f_find(s,f):
    if s.find(f)>=0:
        return(True)
    else:
        return(False)
    pass

#获取游标查询结果
def f_getres(conn,sql):
    try:
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            row=cur.execute(sql)
            f_getcolbysql(conn,sql,1)
            return(cur.fetchall())
    except Exception as e:
        logging.error(e)
    pass

#查询查询结果
def f_dispres(conn,sql):
    try:
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            row=cur.execute(sql)
            #print(row)
            #print(cur.lastrowid)
            f_getcolbysql(conn,sql,1)
            for i in (cur.fetchall()):
                print(i)
            #conn.close()
    except Exception as e:
        logging.error(e)
    pass

#不带参数插入一条记录
def f_insert_one(conn,sql):
    try:
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            cur.execute(sql)
            conn.commit()
            #conn.close()
            return(cur.rowcount)
    except Exception as e:
        logging.error(e)
    pass

#带参数插入一条记录
def f_insert_one1(conn,sql, val):
    try:
        print(sql,val)
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            cur.execute(sql, val)
            conn.commit()
            return(cur.rowcount)
    except Exception as e:
        logging.error(e)
    pass

#带参数插入多条数据
def f_insert_many(conn,sql, val):
    try:
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            cur.executemany(sql, val)
            conn.commit()
            return(cur.rowcount)
    except Exception as e:
        logging.error(e)
    pass

#带参数删除一条数据
def f_delete_one(conn,sql,val):
    try:
        print(sql,val)
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            cur.execute(sql,val)
            conn.commit()
            return(cur.rowcount)
    except Exception as e:
        logging.error(e)
    pass

#带参数更新数据
def f_update(conn,sql, val=None):
    try:
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            if(val==None):
                cur.execute(sql)
            else:
                cur.execute(sql, val)
            conn.commit()
            return(cur.rowcount)
    except Exception as e:
        logging.error(e)
    pass

# 调用存储过程
def f_proc(conn, proc, args=[]):
    try:
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            ret = cur.callproc(proc, args)
            print(ret)
            res = cur.fetchall()
            conn.commit()
            for i in res:
                print(i)
    except Exception as e:
        print(e)
        #conn.rollback()
    pass

# 数据库连接127

#SSH连接线上ptkc测试环境
server_ssh = SSHTunnelForwarder(
            ssh_address_or_host=('172.18.6.153', 22),
            ssh_username='admin',
            ssh_password='wd123456',
            remote_bind_address=('172.18.2.135', 3306))

def f_fetch(conn,sql,type='all'):
    try:
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            row=cur.execute(sql)
            if(type.lower()=='one'):
                res = cur.fetchone()
            if(type.lower()=='all'):
                res = cur.fetchall()
            return(res)
    except Exception as e:
        print(e)
    pass

def f_dispform(conn,sql):
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cur:
            row=cur.execute(sql)
            res=cur.fetchall()
            df=pd.DataFrame(res)
            print(df)
    except Exception as e:
        print(e)
    pass

def f_sshconn(servername='wdms'):
    try:
        if(servername.lower()=='wdms'):
            server= SSHTunnelForwarder(
                ssh_address_or_host=('172.18.6.153', 22),
                ssh_username='admin',
                ssh_password='wd123456',
                remote_bind_address=('127.0.0.1', 3306))
            return (server)
        elif(servername.lower()=='ptkc'):
            server= SSHTunnelForwarder(
                ssh_address_or_host=('172.18.6.153', 22),
                ssh_username='admin',
                ssh_password='wd123456',
                remote_bind_address=('127.0.0.1', 3306))
            return(server)
    except Exception as e:
        print(e)
    pass
def f_conn_jks(jks_url,username,password):

    pass

def f_conn_nacos(jks_url,username,password):

    pass

def f_conn(x):
    conn=None
    match x:
        case 'l'|'local':   #本机
            conn = pymysql.connect(host='localhost', user='root', password='000000', database='xl')
            #return(conn)
        case 'test'|'dev'|'ptkc':        #跑腿快车测试环境
            conn= pymysql.connect( host='192.168.2.41', user='wd_local', password='wd_PTKC', database='runfast_trade')
        case 'ptkc_prod'|'prod'|'pro'|'pre'|'hd':        #跑腿快车生产环境
            conn= pymysql.connect( host='172.18.6.153',port=13306, user='wd_test', password='wd2021ptkc@test', database='runfast_trade')
            #return(conn)
        case 'zt'|'zentao': #禅道
            conn = pymysql.connect( host='172.18.2.135', user='test', password='test@123', database='zentao')
    return(conn)
    pass
def f_conn_local():
    #def f_conn(database='mysqldemo', host='127.0.0.1', port=3306, user='root', password='000000'):
    try:
        conn = pymysql.connect(**config_local)
        #conn = pymysql.connect(host=host,port=port,user=user, password=password, database=database,charset='utf8')
        return(conn)
    except Exception as e:
        logging.error(e)
    pass

def f_conn_ptkc(database='runfast',host='172.18.6.153', port=3306, user='wd_local', password='wd_PTKC'):
    try:
        conn = pymysql.connect(host=host,port=port,user=user, password=password, database=database,charset='utf8')
        return(conn)
    except Exception as e:
        logging.error(e)
    pass

def f_conn_wdms(database='runfast_trade',host='172.18.2.135', port=3306, user='test', password='test@123'):
    try:
        server_ssh1 = SSHTunnelForwarder(
            ssh_address_or_host=('172.18.6.153', 22),
            ssh_username='admin',
            ssh_password='wd123456',
            remote_bind_address=(host, port) )

        print('\033[31m正在尝试ssh连接... \033[0m',end='')
        #with SSHTunnelForwarder(('172.18.6.153',22),ssh_username='admin',ssh_password='wd123456',remote_bind_address=('172.18.6.153',port)) as server:
        #    server.start()
        server=f_sshconn('wdms')
        server.start()
        print('\033[32mssh连接成功！ssh server启动成功！\033[0m')
        #conn = pymysql.connect(host=host,port=port,user=user, password=password, database=database,charset='utf8')
        conn = pymysql.connect(**config_wdms)
        return(conn)
    except Exception as e:
        print(e)
        logging.error(e)
    pass

def f_conn_devops(database='runfast_trade',host='t3nod1ciqw0bkmo.oceanbase.aliyuncs.com', port=3306, user='runfast_test', password='test@123'):
    try:
        conn = pymysql.connect(**config_devops)

        return (conn)
    except Exception as e:
        print(e)
        logging.error(e)
    pass

# 数据库连接127
def f_conn127(p_dbname):
    try:
        conn = pymysql.connect(host='127.0.0.1',port=3306, user='root', password='000000', database=p_dbname,charset='utf8')
        return(conn)
    except Exception as e:
        logging.error(e)
    pass

# 数据库连接181
def f_conn181(p_dbname):
    try:
        conn = pymysql.connect(host='192.168.2.181',port=3306, user='root', password='000000', database=p_dbname,charset='utf8')
        return(conn)
    except Exception as e:
        logging.error(e)
    pass

# 数据库连接41
def f_conn41_33062():
    try:
        conn = pymysql.connect(host='192.168.2.40', port=33062,user='root', password='123456', database='runfast',charset='utf8')
        return(conn)
    except Exception as e:
        logging.error(e)
    pass

# 数据库连接41
def f_conn41_33066():
    try:
        conn = pymysql.connect(host='192.168.2.40', port=33066,user='root', password='123456', database='runfast_history',charset='utf8')
        return(conn)
    except Exception as e:
        logging.error(e)
    pass

# 数据库连接41
def f_conn41_33069():
    try:
        conn = pymysql.connect(host='192.168.2.40', port=33069,user='root', password='123456', database='runfast_trade',charset='utf8')
        return(conn)
    except Exception as e:
        logging(e)
    pass

def f_conn41():
    try:
        conn = pymysql.connect(host='192.168.2.41', port=3306,user='wd_local', password='wd123456', database='runfast',charset='utf8')
        return(conn)
    except Exception as e:
        logging.error(e)
    pass
# 数据库连接51
def f_conn51():
    try:
        conn = pymysql.connect(host='192.168.2.51', port=3306,user='root', password='wd2021@gxptkc51', database='runfast',charset='utf8')
        return(conn)
    except Exception as e:
        logging.error(e)
    pass

# 数据库连接54
def f_conn54():
    try:
        conn = pymysql.connect(host='192.168.2.54', port=3306,user='root', password='123456', database='runfast',charset='utf8')
        return(conn)
    except Exception as e:
        logging.error(e)
    pass

# 数据库连接54
def f_conn_online():
    try:
        conn = pymysql.connect(host='120.24.237.51', port=3306,user='test', password='test@123', database='runfast',charset='utf8')
        return(conn)
    except Exception as e:
        logging.error(e)
    pass

#查询数据库版本
def f_get_db_version(conn):
    try:
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            cur.execute("select version()")
            data = cur.fetchone()
            print(" Database Version:%s" % data)
            #return({"code":code_ok,"success":success_ok,"msg":"数据库版本号","version":'+"".join(tuple(data))+'})
            #return({"code":code_ok,"success":success_ok,"msg":"数据库版本号","version":tuple(data)})
            return({"code":code_ok,"success":success_ok,"msg":"数据库版本号","version":data})
    except Exception as e:
        logging.error(e)
    pass

#查询全部数据库
#@app.route('/listalldb', methods=['get','post'])
def f_listalldb():
    conn=f_conn_local()
    with conn.cursor(cursor=pymysql.cursors.DictCursor) as cur:
        sql='show databases;'
        cur.execute(sql)
        data=[]
        text={'code':200,'success':True,}
        data.append(text)
        for i in cur:
            text={'dbname':i[0]}
            data.append(text)
        return(json.dumps(data,default=str,ensure_ascii=False,indent=4))
    pass

#睡眠n秒
def f_sleep(n):
    time.sleep(n)
    pass

def f_islower(s):
    ret=s.islower()
    return(ret)
    pass

#反转字符串大小写
def f_swapcase(s):
    return(s.swapcase())
    pass

#字符串大写
def f_upper(s):
    return(s.upper())
    pass
	
#字符串小写
def f_lower(s):
    return(s.lower())
    pass
	
def f_isupper(s):
    ret=s.isupper()
    return(ret)
    pass

#查询指定数据库
def f_listdbbynameb():
    dbname=request.values.get('dbname')
    if dbname:
        conn=f_conn_local()
        with conn.cursor(cursor=pymysql.cursors.DictCursor) as cur:
            sql='show databases;'
            cur.execute(sql)
            data=[]
            text={'code':200,'success':True,}
            data.append(text)
            for i in cur:
                text={'dbname':i[0]}
                data.append(text)
            return(json.dumps(data,default=str,ensure_ascii=False,indent=4))
    else:
        msg={'code':10001,'success':False,'msg':'数据库名不能为空!'}
        return(json.dumps(msg,default=str,ensure_ascii=False,indent=4))
    pass



#目录操作
#遍历目录及子目录下的文件
def f_dir01(path):
    for root, dirs, files in os.walk(path):
        print('\033[31m', root, '\033[0m')
        print('\t\033[32m', dir, '\033[0m')
        for f in files:
            print('\t\t', f)
    pass

def f_dir02(path):
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            print('\033[32m', file_path,'\033[0m')
            f_dir02(file_path)
        else:
            print('\t\033[33m', file_path,'\033[0m')
    pass

def f_dir03(path):
    files = glob.glob(os.path.join(path, '*'))
    for file in files:
        if os.path.isdir(file):
            print('\033[34m', file,'\033[0m')
            f_dir03(file)
        else:
            print('\t', file)
    pass

def f_dir04(path):
    files=[file.name for file in path.rglob('*.*')]
    for f in files:
        # print(f)
        if(os.path.isdir(f)):
            print('\033[31m',f,'\033[0m')
        else:
            print('\t\033[32m',f,'\033[0m')
    pass

def f_dir05(path):
    files = os.listdir(path)
    for file in files:
        file_path = os.path.join(path, file)
        if os.path.isfile(file_path):
            print('\t',file)
        elif os.path.isdir(file_path):
            print('\033[31m',file_path,'\033[0m')
            f_dir05(file_path)
    pass


#用list(f_dir06(path))获取结果
def f_dir06(path):
    files = os.listdir(path)
    for file in files:
        file_path = os.path.join(path, file)
        if os.path.isfile(file_path):
            yield file
            print('\t',file)
        elif os.path.isdir(file_path):
            print('\033[31m',file,'\033[0m')
            yield from f_dir06(file_path)
    pass

files = []
def f_dir07(path):
    for item in os.scandir(path):
        if item.is_file():
            files.append(item.path)
        else:
            print('\033[31m',x.f_isdir(item),'\033[0m',item.path)
            f_dir07(item)
    return(files)
    pass

