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
