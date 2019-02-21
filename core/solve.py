from wxpy import *

bot = Bot(console_qr=True, cache_path=True)
friends = bot.friends

def valid_msg(msg):
    '''
    验证信息
    :param msg:
    :return:
    '''
    return '我要内推' in msg.text.lower()


def invite(user):
    '''
    邀请用户方法
    :param user: User 对象
    :param bot: Bot 对象
    :return:
    '''
    group = bot.groups().search("Sepicat")
    user.send(group.name)
    if len(group) > 0:
        group[0].add_members(user, use_invitation=True)


@bot.register(msg_types=FRIENDS)
def new_friends(msg):
    '''
    处理加好友
    :param msg:
    :return:
    '''
    user = msg.card.accept()
    if valid_msg(msg):
        invite(user)
    else:
        user.send('hello {user_name},忘记填写加群口令了,去填写吧'.format(user_name=user.name))


@bot.register(Friend, msg_types=TEXT)
def exist_friends(msg):
    if valid_msg(msg):
        msg.sender.send('点击加群')
        group = bot.groups().search("Sepicat")
        if len(group) <= 0:
            msg.sender.send('读取群信息失败')
        else:
            msg.sender.send('读取群信息成功')
            msg.sender.send(group[0].name)
        group[0].add_members(users=[msg.sender], use_invitation=True)

    else:
        msg.sender.send('hello {user_name},忘记填写加群口令了,去填写吧'.format(user_name=msg.sender.name))

embed()
