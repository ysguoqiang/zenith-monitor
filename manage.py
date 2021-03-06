# 作者：Forec
# 最后修改日期：2016-12-24
# 邮箱：forec@bupt.edu.cn
# 关于此文件：此文件为服务器的管理入口，注册了数据库初始化、shell控
#    制、测试等函数。

import os, time
COV = None
if os.environ.get('ZENITH_COVERAGE'):
    import coverage
    # 启动检测
    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()

from app           import create_app, db
from app.models    import User, Device
from app.devices   import deviceTable, Bulb, TV, AirCondition, PC
from flask_script  import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app('default')
    # 按配置方案创建应用

manager = Manager(app)
    # 注册管理器

migrate = Migrate(app, db)
    # 注册数据库迁移

# make_shell_context 将模型注册到管理器
def make_shell_context():
    return dict(
            app=app,
            db=db,
            User=User,
            Device = Device,
            Bulb = Bulb,
			TV = TV,
			PC = PC,
			AirCondition = AirCondition,
            deviceTable = deviceTable)

# 向管理器注册shell指令
manager.add_command("shell", Shell(make_context=make_shell_context))

# 向管理器注册数据库迁移指令
manager.add_command("db", MigrateCommand)

# 管理器注册测试指令
@manager.command
def test(coverage=False):
    """Run the unit tests"""
    if coverage and not os.environ.get('ZENITH_COVERAGE'):
        import sys
        os.environ['ZENITH_COVERAGE'] = '1'
        # 重启全局部分
        os.execvp(sys.executable, [sys.executable] + sys.argv)    
    #import unittest
    #tests = unittest.TestLoader().discover("tests")
    #unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'temp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir) 

# 管理器注册初始化数据库指令
@manager.command
def init():
    '''Init the database'''
    db.drop_all()
    db.session.commit()
    db.create_all()
    u1 = User(email='forec@bupt.edu.cn',
             nickname='Forec',
             password='zenithdm',
             confirmed=True,
             about_me='这个人很懒，什么都没有留下')
    u2 = User(email='test@test.com',
             nickname='设备管理测试员',
             monitor_url="http://monitor.cross.forec.cn",
             token_hash='9490544C18C15B21286685B41F825684',
             password='zenithdm',
             confirmed=True,
             about_me='我是顶点云设备管理平台测试者')
    db.session.add(u1)
    db.session.add(u2)

    d1 = Bulb(name = '主卧照明',
              code='E1A9013A447E',
             owner = u2,
             interval = 5,
             about = '主卧右四大灯照明'
             )

    d2 = Bulb(name = '书房台灯',
             owner = u2,
              code='BA8120601307',
             interval = 3,
             about = '书房书橱右上第二个台灯'
             )

    d3 = Bulb(name = '厨房照明',
             owner = u2,
              code='LI29F2MV9D7Z',
             interval = 3,
             about = '厨房油烟机灯光'
             )

    d4 = TV(name = '客厅电视',
             owner = u2,
             code='CE683231033B',
             interval = 5,
             about = '65536 寸 TCL 彩电'
             )

    d5 = AirCondition(
            name = '客房柜式空调',
            owner = u2,
            code='EFID2141FJKD',
             interval = 5,
             about = '客房柜式 GL 203 空调'
             )

    d6 = PC(
        name = '树莓派',
        owner= u2,
        code = 'JFIDEO2193FJ',
        interval = 5,
        about = '宿舍里留守的树莓派'
    )

    db.session.add(d1)
    db.session.add(d2)
    db.session.add(d3)
    db.session.add(d4)
    db.session.add(d5)
    db.session.add(d6)
    db.session.commit()

# 清空数据库并初始化测试用户
@manager.command
def simple_init():
    '''Simple Init the database'''
    db.drop_all()
    db.create_all()
    u = User(email='forec@bupt.edu.cn',
             nickname='Forec',
             password='zenith',
             confirmed=True,
             about_me='顶点云设备管理员')
    db.session.add(u)
    u = User(email='test@test.com',
             nickname='测试者',
             password='zenith',
             confirmed=True,
             about_me='欢迎来到顶点云设备管理的线上测试')
    db.session.add(u)
    u = User(email='dragoncat@forec.cn',
             nickname='龙猫',
             password='zenith',
             confirmed=True,
             about_me='我是最萌的')
    db.session.add(u)
    u = User(email='non1996@forec.cn',
             nickname='non1996',
             password='zenith',
             confirmed=True,
             about_me='听说你要开车')
    db.session.add(u)
    u = User(email='rabbit@forec.cn',
             nickname='飞翔的兔子',
             password='zenith',
             confirmed=True,
             about_me='一只热爱生活的兔子')
    db.session.add(u)
    db.session.commit()

if __name__ == "__main__":
    manager.run()
