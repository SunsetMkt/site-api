import flask


def cfstyle(msg='未知消息',
            status='未知状态',
            statuscode='200',
            time='未知时间',
            whathappened='不知道。',
            whatcanido='不知道。',
            footer=''):
    return flask.render_template('cfstyle.html',
                                 msg=msg,
                                 status=status,
                                 statuscode=statuscode,
                                 time=time,
                                 whathappened=whathappened,
                                 whatcanido=whatcanido,
                                 footer=footer)
