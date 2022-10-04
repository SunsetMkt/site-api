import flask


def get_ip():
    # Get IP
    # From headers first
    # cf-connecting-ip x-real-ip
    # x-forwarded-for
    # Then from request
    ip = flask.request.headers.get('cf-connecting-ip')
    if ip is None:
        ip = flask.request.headers.get('x-real-ip')
    if ip is None:
        ip = flask.request.headers.get('x-forwarded-for')
    if ip is None:
        ip = flask.request.remote_addr
    return ip


def cfstyle(msg='未知消息',
            status='未知状态',
            statuscode='200',
            time='未知时间',
            whathappened='不知道。',
            whatcanido='不知道。',
            ip='未知',
            footer=''):
    return flask.render_template('cfstyle.html',
                                 msg=msg,
                                 status=status,
                                 statuscode=statuscode,
                                 time=time,
                                 whathappened=whathappened,
                                 whatcanido=whatcanido,
                                 ip=ip,
                                 footer=footer)
