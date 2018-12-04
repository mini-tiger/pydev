# coding: utf-8
# from sqlalchemy import Column, ForeignKey, INTEGER, Index, String, TIMESTAMP, Table, text
# from sqlalchemy.dialects.mysql.types import MEDIUMINT, TINYINT
# from sqlalchemy.orm import relationship
# from sqlalchemy.ext.declarative import declarative_base
# 
# Base = declarative_base()
# metadata = Base.metadata

# use flask_sqlalchemy
from __future__ import absolute_import
from bk_site import db
from sqlalchemy import Index

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://falcon:123456@192.168.31.230/alarms'


class Abc(db.Model):
    __tablename__ = 'abc'
    id = db.Column(db.Integer, primary_key=True)
    a = db.Column(db.String(255, u'utf_unicode_ci'))
    b = db.Column(db.DATETIME)

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __repr__(self):
        return '<User %r>' % self.a
#########################################################################


# class Abc(Base):
#     __tablename__ = 'abc'
#     a = Column(String(255), nullable=False, primary_key=True)
#     b = Column(String(255), nullable=Fal se)

# class NodeInfo(db.Model):
#     __tablename__ = 'nodeinfo'
#     id = db.Column(db.Integer, primary_key=True)
#     uuid = db.Column(db.String(64), nullable=False, unique=True)
#     ip = db.Column(db.String(64), nullable=False)
#     user = db.Column(db.String(12), nullable=False)
#     passwd = db.Column(db.String(24), nullable=False)
#     port = db.Column(db.Interval, nullable=True)
#     nodeinstall = db.relationship("nodeinstall", backref=db.backref("nodeinfo", uselist=False))
#
#
# class NodeInstall(db.Model):
#     __tablename__ = 'nodeinstall'
#     success = db.Column(db.Boolean, nullable=False)
#     note = db.Column(db.TEXT, nullable=False)
#     runtime = db.Column(db.DATETIME, nullable=False)
#     nodeinfo_id = db.Column(db.Integer, db.ForeignKey('nodeinfo.id'))

##  alarm db
class EventCase(db.Model):
    __tablename__ = 'event_cases'
    __table_args__ = (
        Index('endpoint', 'endpoint', 'strategy_id', 'template_id'),
    )

    id = db.Column(db.String(50), primary_key=True, server_default=db.text("''"))
    endpoint = db.Column(db.String(100), nullable=False)
    metric = db.Column(db.String(200), nullable=False)
    func = db.Column(db.String(50))
    cond = db.Column(db.String(200), nullable=False)
    note = db.Column(db.String(500))
    max_step = db.Column(db.INTEGER)
    current_step = db.Column(db.INTEGER)
    priority = db.Column(db.INTEGER, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    timestamp = db.Column(db.TIMESTAMP, nullable=False, server_default=db.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    update_at = db.Column(db.TIMESTAMP)
    closed_at = db.Column(db.TIMESTAMP)
    closed_note = db.Column(db.String(250))
    user_modified = db.Column(db.INTEGER)
    tpl_creator = db.Column(db.String(64))
    expression_id = db.Column(db.INTEGER)
    strategy_id = db.Column(db.INTEGER)
    template_id = db.Column(db.INTEGER)
    process_note = db.Column(db.INTEGER)
    process_status = db.Column(db.String(20), server_default=db.text("'unresolved'"))


class User(db.Model):
    __tablename__ = 'user'
    __table_args__ = {u'schema': 'uic'}

    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    passwd = db.Column(db.String(64), nullable=False, server_default=db.text("''"))
    cnname = db.Column(db.String(128), nullable=False, server_default=db.text("''"))
    email = db.Column(db.String(255), nullable=False, server_default=db.text("''"))
    phone = db.Column(db.String(16), nullable=False, server_default=db.text("''"))
    im = db.Column(db.String(32), nullable=False, server_default=db.text("''"))
    qq = db.Column(db.String(16), nullable=False, server_default=db.text("''"))
    role = db.Column(db.SMALLINT, nullable=False, server_default=db.text("'0'"))
    creator = db.Column(db.INTEGER, nullable=False, server_default=db.text("'0'"))
    created = db.Column(db.TIMESTAMP, nullable=False, server_default=db.text("CURRENT_TIMESTAMP"))


class EventNote(db.Model):
    __tablename__ = 'event_note'

    id = db.Column(db.INTEGER, primary_key=True)
    event_caseId = db.Column(db.ForeignKey(u'event_cases.id', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True)
    note = db.Column(db.String(300))
    case_id = db.Column(db.String(20))
    status = db.Column(db.String(15))
    timestamp = db.Column(db.TIMESTAMP, nullable=False, server_default=db.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    user_id = db.Column(db.ForeignKey(u'uic.user.id', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True)

    event_case = db.relationship('EventCase')
    user = db.relationship(u'User')


class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    event_caseId = db.Column(db.ForeignKey(u'event_cases.id', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True)
    step = db.Column(db.INTEGER)
    cond = db.Column(db.String(200), nullable=False)
    status = db.Column(db.INTEGER, server_default=db.text("'0'"))
    timestamp = db.Column(db.TIMESTAMP, nullable=False, server_default=db.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    event_case = db.relationship('EventCase', backref='_EventCase')

    def __init__(self, event_caseId=None, step=None, cond=None, status=None, timestamp=None, event_case=None):
        self.event_case=event_case
        self.step=step
        self.cond=cond

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self


# falcon_portal

class Action(db.Model):
    __tablename__ = 'action'
    __bind_key__ = 'falcon_portal'
    id = db.Column(db.Integer, primary_key=True)
    uic = db.Column(db.String(255, u'utf8_unicode_ci'), nullable=False, server_default=db.text("''"))
    url = db.Column(db.String(255, u'utf8_unicode_ci'), nullable=False, server_default=db.text("''"))
    callback = db.Column(db.Integer, nullable=False, server_default=db.text("'0'"))
    before_callback_sms = db.Column(db.Integer, nullable=False, server_default=db.text("'0'"))
    before_callback_mail = db.Column(db.Integer, nullable=False, server_default=db.text("'0'"))
    after_callback_sms = db.Column(db.Integer, nullable=False, server_default=db.text("'0'"))
    after_callback_mail = db.Column(db.Integer, nullable=False, server_default=db.text("'0'"))


class AlertLink(db.Model):
    __tablename__ = 'alert_link'
    __bind_key__ = 'falcon_portal'
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(16, u'utf8_unicode_ci'), nullable=False, unique=True, server_default=db.text("''"))
    content = db.Column(db.Text, nullable=False)
    create_at = db.Column(db.TIMESTAMP, nullable=False, server_default=db.text("CURRENT_db.TIMESTAMP"))


class Cluster(db.Model):
    __tablename__ = 'cluster'
    __bind_key__ = 'falcon_portal'
    id = db.Column(db.Integer, primary_key=True)
    grp_id = db.Column(db.Integer, nullable=False)
    numerator = db.Column(db.String(10240, u'utf8_unicode_ci'), nullable=False)
    denominator = db.Column(db.String(10240, u'utf8_unicode_ci'), nullable=False)
    endpoint = db.Column(db.String(255, u'utf8_unicode_ci'), nullable=False)
    metric = db.Column(db.String(255, u'utf8_unicode_ci'), nullable=False)
    tags = db.Column(db.String(255, u'utf8_unicode_ci'), nullable=False)
    ds_type = db.Column(db.String(255, u'utf8_unicode_ci'), nullable=False)
    step = db.Column(db.Integer, nullable=False)
    last_update = db.Column(db.TIMESTAMP, nullable=False, server_default=db.text("CURRENT_db.TIMESTAMP ON UPDATE CURRENT_db.TIMESTAMP"))
    creator = db.Column(db.String(255, u'utf8_unicode_ci'), nullable=False)


class Expression(db.Model):
    __tablename__ = 'expression'
    __bind_key__ = 'falcon_portal'
    id = db.Column(db.Integer, primary_key=True)
    expression = db.Column(db.String(1024, u'utf8_unicode_ci'), nullable=False)
    func = db.Column(db.String(16, u'utf8_unicode_ci'), nullable=False, server_default=db.text("'all(#1)'"))
    op = db.Column(db.String(8, u'utf8_unicode_ci'), nullable=False, server_default=db.text("''"))
    right_value = db.Column(db.String(16, u'utf8_unicode_ci'), nullable=False, server_default=db.text("''"))
    max_step = db.Column(db.Integer, nullable=False, server_default=db.text("'1'"))
    priority = db.Column(db.Integer, nullable=False, server_default=db.text("'0'"))
    note = db.Column(db.String(1024, u'utf8_unicode_ci'), nullable=False, server_default=db.text("''"))
    action_id = db.Column(db.Integer, nullable=False, server_default=db.text("'0'"))
    create_user = db.Column(db.String(64, u'utf8_unicode_ci'), nullable=False, server_default=db.text("''"))
    pause = db.Column(db.Integer, nullable=False, server_default=db.text("'0'"))

grp_host = db.Table(
    'grp_host',
    db.Column('host_id', db.Integer, db.ForeignKey('host.id')),
    db.Column('grp_id', db.Integer, db.ForeignKey('grp.id')),
    info = {'bind_key': "falcon_portal"}
)


grp_tpl = db.Table(
    'grp_tpl',
    db.Column('grp_id', db.Integer, db.ForeignKey('grp.id')),
    db.Column('tpl_id', db.Integer, db.ForeignKey('tpl.id')),
    db.Column('bind_user', db.String(64, u'utf8_unicode_ci'), nullable=False, server_default=db.text("''")),
    info = {'bind_key': "falcon_portal"}
)

class Grp(db.Model):
    __tablename__ = 'grp'
    __bind_key__ = 'falcon_portal'
    id = db.Column(db.Integer, primary_key=True)
    grp_name = db.Column(db.String(255, u'utf8_unicode_ci'), nullable=False, unique=True, server_default=db.text("''"))
    create_user = db.Column(db.String(64, u'utf8_unicode_ci'), nullable=False, server_default=db.text("''"))
    create_at = db.Column(db.TIMESTAMP, nullable=False, server_default=db.text("CURRENT_db.TIMESTAMP"))
    come_from = db.Column(db.Integer, nullable=False, server_default=db.text("'0'"))
    host = db.relationship('Host', secondary=grp_host, backref="_host", lazy="dynamic")
    tpl = db.relationship('Tpl', secondary=grp_tpl, backref="_tpl", lazy="dynamic")

    def __repr__(self):
        return '<grpt: %r>' %self.id


class Host(db.Model):
    __tablename__ = 'host'
    __bind_key__ = 'falcon_portal'
    id = db.Column(db.Integer, primary_key=True)
    hostname = db.Column(db.String(255, u'utf8_unicode_ci'), nullable=False, unique=True, server_default=db.text("''"))
    ip = db.Column(db.String(16, u'utf8_unicode_ci'), nullable=False, server_default=db.text("''"))
    agent_version = db.Column(db.String(16, u'utf8_unicode_ci'), nullable=False, server_default=db.text("''"))
    plugin_version = db.Column(db.String(128, u'utf8_unicode_ci'), nullable=False, server_default=db.text("''"))
    maintain_begin = db.Column(db.Integer, nullable=False, server_default=db.text("'0'"))
    maintain_end = db.Column(db.Integer, nullable=False, server_default=db.text("'0'"))
    update_at = db.Column(db.TIMESTAMP, nullable=False, server_default=db.text("CURRENT_db.TIMESTAMP ON UPDATE CURRENT_db.TIMESTAMP"))
    hostcol = db.Column(db.VARCHAR(45))
    Manufacturer = db.Column(db.VARCHAR(45))
    ProductName = db.Column(db.VARCHAR(45))
    Version = db.Column(db.VARCHAR(45))
    SerialNumber = db.Column(db.VARCHAR(45))


class Mockcfg(db.Model):
    __tablename__ = 'mockcfg'
    __bind_key__ = 'falcon_portal'
    id = db.Column(db.BIGINT, primary_key=True)
    name = db.Column(db.String(255, u'utf8_unicode_ci'), nullable=False, unique=True, server_default=db.text("''"))
    obj = db.Column(db.String(10240, u'utf8_unicode_ci'), nullable=False, server_default=db.text("''"))
    obj_type = db.Column(db.String(255, u'utf8_unicode_ci'), nullable=False, server_default=db.text("''"))
    metric = db.Column(db.String(128, u'utf8_unicode_ci'), nullable=False, server_default=db.text("''"))
    tags = db.Column(db.String(1024, u'utf8_unicode_ci'), nullable=False, server_default=db.text("''"))
    dstype = db.Column(db.String(32, u'utf8_unicode_ci'), nullable=False, server_default=db.text("'GAUGE'"))
    step = db.Column(db.Integer, nullable=False, server_default=db.text("'60'"))
    mock = db.Column(db.Float(asdecimal=True), nullable=False, server_default=db.text("'0'"))
    creator = db.Column(db.String(64, u'utf8_unicode_ci'), nullable=False, server_default=db.text("''"))
    t_create = db.Column(db.DateTime, nullable=False)
    t_modify = db.Column(db.TIMESTAMP, nullable=False, server_default=db.text("CURRENT_db.TIMESTAMP ON UPDATE CURRENT_db.TIMESTAMP"))


class PluginDir(db.Model):
    __tablename__ = 'plugin_dir'
    __bind_key__ = 'falcon_portal'
    id = db.Column(db.Integer, primary_key=True)
    grp_id = db.Column(db.Integer, nullable=False, index=True)
    dir = db.Column(db.String(255, u'utf8_unicode_ci'), nullable=False)
    create_user = db.Column(db.String(64, u'utf8_unicode_ci'), nullable=False, server_default=db.text("''"))
    create_at = db.Column(db.TIMESTAMP, nullable=False, server_default=db.text("CURRENT_db.TIMESTAMP"))


class Strategy(db.Model):
    __tablename__ = 'strategy'
    __bind_key__ = 'falcon_portal'
    id = db.Column(db.Integer, primary_key=True)
    metric = db.Column(db.String(128, u'utf8_unicode_ci'), nullable=False, server_default=db.text("''"))
    tags = db.Column(db.String(256, u'utf8_unicode_ci'), nullable=False, server_default=db.text("''"))
    max_step = db.Column(db.Integer, nullable=False, server_default=db.text("'1'"))
    priority = db.Column(db.Integer, nullable=False, server_default=db.text("'0'"))
    func = db.Column(db.String(16, u'utf8_unicode_ci'), nullable=False, server_default=db.text("'all(#1)'"))
    op = db.Column(db.String(8, u'utf8_unicode_ci'), nullable=False, server_default=db.text("''"))
    right_value = db.Column(db.String(64, u'utf8_unicode_ci'), nullable=False)
    note = db.Column(db.String(128, u'utf8_unicode_ci'), nullable=False, server_default=db.text("''"))
    run_begin = db.Column(db.String(16, u'utf8_unicode_ci'), nullable=False, server_default=db.text("''"))
    run_end = db.Column(db.String(16, u'utf8_unicode_ci'), nullable=False, server_default=db.text("''"))
    tpl_id = db.Column(db.Integer, nullable=False, index=True, server_default=db.text("'0'"))


class Tpl(db.Model):
    __tablename__ = 'tpl'
    __bind_key__ = 'falcon_portal'
    id = db.Column(db.Integer, primary_key=True)
    tpl_name = db.Column(db.String(255, u'utf8_unicode_ci'), nullable=False, unique=True, server_default=db.text("''"))
    parent_id = db.Column(db.Integer, nullable=False, server_default=db.text("'0'"))
    action_id = db.Column(db.Integer, nullable=False, server_default=db.text("'0'"))
    create_user = db.Column(db.String(64, u'utf8_unicode_ci'), nullable=False, index=True, server_default=db.text("''"))
    create_at = db.Column(db.TIMESTAMP, nullable=False, server_default=db.text("CURRENT_db.TIMESTAMP"))
