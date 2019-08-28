from sqlalchemy import create_engine
from sqlalchemy import Column, Date, Integer, String, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base


# 连接数据库
engin = create_engine('sqlite:///guabot.db', echo=True)

# 基本类
Base = declarative_base()


class DailyTask(Base):
    __tablename__ = 'daily_task'

    # 字段
    id = Column(Integer, primary_key=True)
    create_date = Column(Date)
    question_link = Column(Text)
    learning_link = Column(Text)
    wechat_msg = Column(Text)

    def __str__(self):
        return f'#{self.id} {self.create_date}'


class QuestionPunchOn(Base):
    __tablename__ = 'question_punch_on'

    id = Column(Integer, primary_key=True)
    user_name = Column(String(64))
    create_date = Column(Date)
    solve_link = Column(Text)

    def __str__(self):
        return f'#{self.user_name} #{self.create_date}'


Base.metadata.create_all(engin)
