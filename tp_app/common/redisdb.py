# coding:utf-8
import redis
from tp_app.config import REDIS_URL
from tp_app.config import REDIS_EX


class RedisDB:
    def __init__(self, redis_url=REDIS_URL, db: int = 0):
        self.client = redis.Redis.from_url(redis_url + str(db))
        self.pipe = self.client.pipeline()

    @property
    def status(self):
        return self.client.ping()

    def session_set_user_info(self, token, user_info, ex=REDIS_EX):
        return self.client.set(token, user_info, ex=ex)

    def session_get_user_info(self, token):
        return self.client.get(token)

    def session_del_token(self, token):
        return self.client.delete(token)

    def execute_command(self, command):
        return self.client.execute_command(command)


if __name__ == '__main__':
    r = RedisDB()
#     print(r.status)
    print(r.execute_command('keys *'))
