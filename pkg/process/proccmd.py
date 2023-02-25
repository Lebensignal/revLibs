import plugins.revLibs.pkg.process.revss as revss

def process_command(session_name: str, **kwargs) -> str:
    """处理命令"""

    cmd = kwargs['command']
    params = kwargs['params']

    reply_message = ""

    if cmd == 'reset':
        session: revss.RevSession = revss.get_session(session_name)
        if len(params) >= 1:
            prompt_whole_name = session.reset(params[0])
            reply_message = "已重置会话，使用情景预设: {}".format(prompt_whole_name)
        else:
            session.reset()
            reply_message = "已重置会话"
    elif cmd == 'list':
        session: revss.RevSession = revss.get_session(session_name)
        page = 1
        if len(params)>=1:
            page = int(params[0])
        
        cbinst = session.get_rev_lib_inst()
        from revChatGPT.V1 import Chatbot
        assert isinstance(cbinst, Chatbot)

        conversations = cbinst.get_conversations((page-1)*10, 10)

        reply_message = "会话列表 (第{}页) 本页{}个会话:\n".format(page, len(conversations))
        for conversation in conversations:
            reply_message += "#{}: {}\n".format(conversation['id'], conversation['create_time'])

    elif cmd == 'prompt':
        # cbinst = session.get_rev_lib_inst()
        # from revChatGPT.V1 import Chatbot
        # assert isinstance(cbinst, Chatbot)
        # reply_message = str(cbinst.get_msg_history(session.conversation_id))
        reply_message = "正在使用逆向库，暂不支持查看历史消息"
    elif cmd == "last":
        reply_message = "正在使用逆向库，暂不支持切换到前一次会话"
    elif cmd == "next":
        reply_message = "正在使用逆向库，暂不支持切换到后一次会话"
    elif cmd == "resend":
        session: revss.RevSession = revss.get_session(session_name)
        if session.__ls_prompt__ == "":
            reply_message = "没有上一条成功回复的消息"
        else:
            reply_message = session.resend()

    return reply_message