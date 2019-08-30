from .models_declare import engin
from .models_declare import DailyTask, QuestionPunchOn
from sqlalchemy.orm import sessionmaker

import datetime

session = sessionmaker(bind=engin)()

def insert_daily_task(question_link: str, learning_link: str, msg: str) -> bool:
    """
    增加每日一题
    :return:
    """
    exist, _ = check_daily_exist()
    if exist:
        return False

    now = datetime.datetime.now()
    daily_task = DailyTask(create_date=now,
                           create_day=now.strftime('%Y-%m-%d'),
                           question_link=question_link,
                           learning_link=learning_link,
                           wechat_msg=msg)
    session.add(daily_task)
    session.commit()
    return True

def insert_punch_on(user_name: str, solve_link: str) -> bool:
    """
    每日打卡
    :param user_name: 用户名
    :param solve_link: 题解链接
    :param daily_task_id: daily task id
    :return:
    """
    now = datetime.datetime.now()
    day = now.strftime('%Y-%m-%d')
    q = list(session.query(DailyTask).filter(DailyTask.create_day == day))
    if len(q) > 0:
        daily_task = q[0]
        daily_task_id = daily_task.id
        punch_on_item = QuestionPunchOn(user_name=user_name,
                                        create_date=now,
                                        solve_link=solve_link,
                                        daily_task_id=daily_task_id)
        session.add(punch_on_item)
        session.commit()
        return True

    return False

def check_daily_exist() -> (bool, str):
    """
    检查是否有每日一题
    :return:
    """
    now = datetime.datetime.now()
    day = now.strftime('%Y-%m-%d')
    q = list(session.query(DailyTask).filter(DailyTask.create_day == day))
    exist = len(q) > 0
    if exist:
        daily_task = q[0]
        link = daily_task.question_link
        return exist, link
    return exist, None

def check_daily_rank(day: str = None) -> list:
    """
    查看某一天榜单
    :param day:
    :return:
    """
    if day is None:
        now = datetime.datetime.now()
        day = now.strftime('%Y-%m-%d')
    q = list(session.query(DailyTask).filter(DailyTask.create_day == day))
    if len(q) > 0:
        daily_task_id = q[0].id
        punches = list(session.query(QuestionPunchOn).filter(QuestionPunchOn.daily_task_id == daily_task_id))
        res = [{'user': p.user_name, 'solve': p.solve_link} for p in punches]
        return res
    return []
