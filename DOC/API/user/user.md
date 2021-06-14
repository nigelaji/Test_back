### Restful: User

- 创建用户
    - URI: `/users`
    - Method: `POST`
    - Headers:

          {
            "Content-Type": "application/json",
            "Set-Cookie": "token"
          }
        
    - Fields:
    
        |参数名称|是否必填|数据类型|描述|
        |---|---|---|---|
        |username|否|String(30)|用户名称|
        |user_code|是|String(18)|用户账号|
        |email|是|Email|邮箱|
        |phone|否|Phone|手机号|
        |remark|否|String(256)|备注|
    
    - Response:
        - Success
        
              {
                'code': 200,
                'data': {
                  "id": 1
                },
                'msg': '创建成功'
              }
        - Fail
        
              {
                'code': 498,
                'data':{},
                'msg':'参数填写错误',
                ’detail‘: '邮箱已存在'
              }
    
- 删除用户
    - URI: `/users/{id}`
    - Method: `DELETE`
    - Headers:

          {
            "Set-Cookie": "token"
          }

    - Response:
        - Success
        
              {
                'code': 200,
                'data': {},
                'msg': '删除成功'
              }

- 修改用户
    - URI: `/users/{id}`
    - Method: `PUT`
    - Headers:

          {
            "Content-Type": "application/json",
            "Set-Cookie": "token"
          }
        
    - Fields:
    
        |参数名称|是否必填|数据类型|描述|
        |---|---|---|---|
        |username|否|String(30)|用户名称|
        |user_code|是|String(18)|用户账号|
        |email|是|Email|邮箱|
        |phone|否|Phone|手机号|
        |remark|否|String(256)|备注|

    - Response:
        - Success
        
          {
            'code': 200,
            'data': {},
            'msg': '删除成功'
          }

- 获取用户详情
    - URI: `/users/{id}`
    - Method: `GET`
    - Headers:

          {
            "Set-Cookie": "token"
          }

    - Response:
        - Success
        
              {
                  'code': 200,
                  'data': {
                    'user_id': self.id,
                    'username': self.username,
                    'user_code': self.user_code,
                    'email': self.email,
                    'phone': self.phone,
                    'create_time': dump_datetime(self.create_time),
                    'update_time': dump_datetime(self.update_time),
                    'locked': self.locked,
                    'locked_time': dump_datetime(self.locked_time),
                    'unlocked_time': dump_datetime(self.unlocked_time),
                    'remark': self.remark,    
                  },
                  'msg': ''
              }


- 查询用户列表
    - URI: `/users`
    - Method: `GET`
    - Headers:

          {
            "Set-Cookie": "token"
          }

    - Response:
        - Success
        
          {
            'code': 200,
            'data': [
                {
                    'user_id': self.id,
                    'username': self.username,
                    'user_code': self.user_code,
                    'email': self.email,
                    'phone': self.phone,
                    'create_time': dump_datetime(self.create_time),
                    'update_time': dump_datetime(self.update_time),
                    'locked': self.locked,
                    'locked_time': dump_datetime(self.locked_time),
                    'unlocked_time': dump_datetime(self.unlocked_time),
                    'remark': self.remark,    
                },
                ...
            ],
            'msg': ''
          }

- 获取用户配置
    - URI: `/user/profile`
    - Method: `GET`
    - Headers:

          {
            "Set-Cookie": "token"
          }

    - Response:
        - Success
        
              {
                'code': 200,
                'data': {
                    ...
                },
                'msg': ''
              }

- 解锁定账户
    - URI: `/user/lock`
    - Method: `GET`
    - Headers:

          {
            "Set-Cookie": "token"
          }

    - Response:
        - Success
        
              {
                'code': 200,
                'data': {},
                'msg': '账户已锁定'
              }