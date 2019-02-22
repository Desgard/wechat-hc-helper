from wxpy import *
import os


GROUP_NAME = "字节跳动实习内推"
bot = Bot(console_qr=True, cache_path=True)
friends = bot.friends

related_group: Group = None
if len(bot.groups().search(GROUP_NAME)) > 0:
    related_group = bot.groups().search(GROUP_NAME)[0]


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
    group = bot.groups().search("")
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
    """
    处理邀请加群信息
    :param msg:
    :return:
    """
    if valid_msg(msg):
        msg.sender.send('点击加群')
        group = bot.groups().search(GROUP_NAME)
        if len(group) <= 0:
            msg.sender.send('读取群信息失败')
        else:
            msg.sender.send(group[0].name)
            gp = group[0]
            len_mem = len(gp.members)
            global related_group
            related_group = gp
            if len_mem >= 100:
                # gp.add(users=[msg.sender], use_invitation=True)
                msg.sender.send("自动拉好友接口失效，等待手动拉好友。")
            else:
                msg.sender.send_image(os.path.join(os.getcwd(), 'qrcode.jpg'))

    else:
        msg.sender.send('hello {user_name},忘记填写加群口令了,去填写吧'.format(user_name=msg.sender.name))

embed()
