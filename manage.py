from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from app import create_app
from exts import db
from app.models import User, Question
import config

app = create_app(config)
manager = Manager(app)

migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db, User=User, Question=Question)

manager.add_command("shell", Shell(make_context=make_shell_context))
# 添加迁移脚本命令
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
