# -*- coding: UTF-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp
"""
用户登录：
	当用户登录时候，需要对用户提交的用户名和密码进行多种格式校验。如：
	用户不能为空；用户长度必须大于6；
	密码不能为空；密码长度必须大于12；密码必须包含 字母、数字、特殊字符等（自定义正则）；
"""

class RegistrationForm(FlaskForm):
	"""注册表单"""
	email = StringField(u'邮箱', validators=[DataRequired(message=u'邮箱不能为空'),Length(1,64),Email()],
									render_kw={"placeholder": "E-mail: yourname@example.com"})
	username = StringField(u'用户名', validators=[DataRequired(),Length(1,64),Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,u'用户名必须由字母、数字、下划线或.组成')],
										render_kw={"placeholder": "输入昵称"})
	password = StringField(u'密码', validators=[DataRequired(),EqualTo('password2',message=u'密码与确认密码必须一致')])
	password2 = StringField(u'确认密码', validators=[DataRequired()])
	submit = SubmitField(u'注册')

class LoginForm(FlaskForm):
	"""登录表单"""
	email = StringField(u'邮箱', validators=[DataRequired(message=u'邮箱不能为空'),Length(1,64),Email()],
									render_kw={"placeholder": "E-mail: yourname@example.com"})
									# bootstrap框架有过这个提示了，可以不用写message参数
	password = PasswordField(label=u'密码', validators=[DataRequired(message=u'密码不能为空')],
											render_kw={"placeholder": "输入密码"})
	submit = SubmitField(label=u'登陆')


