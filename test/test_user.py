import unittest
from VerifySystem.test.RequestBase import JsonRequestBase


class TestUser(unittest.TestCase, JsonRequestBase):
    """前后端ajax通信测试
    """

    def data_translation(self):

        data = {
            'username': '张三',
            'password': 123123
        }
        url = f'{self.host}/p/test_data/'
        response = self.post(url, data)
        print(response)

    def create_buser(self):
        """添加商家用户
        """
        url = f'{self.host}/p/create_buser/'
        data = {
            'business_name': "呷哺呷哺",
            'username': "test2",
            'password': "123",
        }
        response = self.post(url, data)
        print(response)

    def query_buser(self):
        """查询商家用户
        """
        url = f'{self.host}/p/query_buser/'
        response = self.get(url)
        print(response)

    def del_buser(self):
        """删除商家用户
        """
        url = f'{self.host}/p/delete_buser/'
        data = {
            'username': "test2",
        }
        response = self.post(url, data)
        print(response)

    def test_all(self):
        # self.data_translation()
        # self.create_buser()
        # self.del_buser()
        self.query_buser()


if __name__ == "__main__":
    unittest.main()
