import __init__
import unittest
import sys
from typing import List

from Commons import UserId, Uid, Password
from Domains.Entities import UserVO, User
from Applications.Usecases import CreateUser, LoginUser
from Applications.Usecases.AppUsecaseExtention import convert_to_Password_with_hashing
from Applications.Results import (
    Fail,
    Fail_CheckUser_IDNotFound,
    Fail_CreateUser_IDAlreadyExists,
)

import Tests.Applications.Usecases.storage_selecter as test_selector


class test_user_services(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = "test"
        print(sys._getframe(0).f_code.co_name)

    @classmethod
    def tearDownClass(cls):
        "Hook method for deconstructing the class fixture after running all tests in the class."
        print(sys._getframe(0).f_code.co_name)

    def setUp(self):
        "Hook method for setting up the test fixture before exercising it."
        print("\t", sys._getframe(0).f_code.co_name)
        factory = test_selector.get_test_factory("user_service_test_")

        migrate = test_selector.get_usecase_migration(factory)
        # 깔끔하게 지우고 시작
        if migrate.check_exist_user():
            migrate.delete_user()
        # 테이블 생성
        migrate.create_user()

        # 기본세팅
        repo = test_selector.get_user_storage(factory)
        create_user = CreateUser(repo)
        login_user = LoginUser(repo)

        users = []
        u = create_user.create("taks123", "1Q2w3e4r!@$", "takgyun Lee")
        users.append(u)
        u = create_user.create("hahahoho119", "1B2n3m4!@", "Ho Han")
        users.append(u)
        u = create_user.create("mygun7749", "$1Awb5$123", "Guna Yoo")
        users.append(u)

        self.create_user = CreateUser(repo)
        self.login_user = LoginUser(repo)

    def tearDown(self):
        "Hook method for deconstructing the test fixture after testing it."
        print("\t", sys._getframe(0).f_code.co_name)
        factory = test_selector.get_test_factory("user_service_test_")
        # 썻으면 삭제
        migrate = test_selector.get_usecase_migration(factory)
        if migrate.check_exist_user():
            migrate.delete_user()

        self.assertFalse(migrate.check_exist_user())

    def test_login_user_로그인_안_되는거_확인(self):
        print("\t\t", sys._getframe(0).f_code.co_name)

        user: UserVO = self.login_user.login("tak123", "1Q2w3e4r!@$")

        self.assertDictEqual(
            {"type": "IDNotFound"},
            user.__dict__,
        )

        user = self.login_user.login("hahahoho119", "2N3m4!@")

        self.assertDictEqual(
            {"type": "PasswardNotCorrect"},
            user.__dict__,
        )

    def test_login_user_잘_로그인_되는거_확인(self):
        print("\t\t", sys._getframe(0).f_code.co_name)

        user = self.login_user.login("taks123", "1Q2w3e4r!@$")
        match user:
            case _ if isinstance(user, Fail):
                self.assertTrue(False)
            case _:
                pass

        self.assertDictEqual(
            {
                "user_id": UserId(account="taks123"),
                "name": "takgyun Lee",
                "uid": Uid(idx=1),
            },
            user.__dict__,
        )

        user = self.login_user.login("hahahoho119", "1B2n3m4!@")

        self.assertDictEqual(
            {
                "user_id": UserId(account="hahahoho119"),
                "name": "Ho Han",
                "uid": Uid(idx=2),
            },
            user.__dict__,
        )

        user = self.login_user.login("mygun7749", "$1Awb5$123")

        self.assertDictEqual(
            {
                "user_id": UserId(account="mygun7749"),
                "name": "Guna Yoo",
                "uid": Uid(idx=3),
            },
            user.__dict__,
        )

    def test_result(self):
        print("\t\t", sys._getframe(0).f_code.co_name)
        self.assertEqual({"type": "basic"}, Fail(type="basic").__dict__)

        self.assertTrue(issubclass(Fail_CreateUser_IDAlreadyExists, Fail))
        self.assertTrue(isinstance(Fail_CreateUser_IDAlreadyExists(), Fail))
        self.assertEqual(
            {"type": "IDAlreadyExists"}, Fail_CreateUser_IDAlreadyExists().__dict__
        )

        self.assertTrue(issubclass(Fail_CheckUser_IDNotFound, Fail))
        self.assertTrue(isinstance(Fail_CheckUser_IDNotFound(), Fail))
        self.assertEqual({"type": "IDNotFound"}, Fail_CheckUser_IDNotFound().__dict__)

    def test_start_data(self):
        print("\t\t", sys._getframe(0).f_code.co_name)
        user = self.login_user.login("taks123", "1Q2w3e4r!@$")

        self.assertDictEqual(
            {
                "user_id": UserId(account="taks123"),
                "name": "takgyun Lee",
                "uid": Uid(idx=1),
            },
            user.__dict__,
        )

        user = self.login_user.login("hahahoho119", "1B2n3m4!@")

        self.assertDictEqual(
            {
                "user_id": UserId(account="hahahoho119"),
                "name": "Ho Han",
                "uid": Uid(idx=2),
            },
            user.__dict__,
        )

        user = self.login_user.login("mygun7749", "$1Awb5$123")

        self.assertDictEqual(
            {
                "user_id": UserId(account="mygun7749"),
                "name": "Guna Yoo",
                "uid": Uid(idx=3),
            },
            user.__dict__,
        )

    def test_중복_아이디_생성하는지_확인(self):
        print("\t\t", sys._getframe(0).f_code.co_name)

        # 중복 아이디
        ret = self.create_user.create("taks123", "1Q2w3e4r!@$", "takgyun Lee")
        match ret:
            case _ if isinstance(ret, Fail):
                self.assertTrue(True)
            case _:
                print(ret.__dict__)
                self.assertTrue(False)


def main():
    unittest.main()


if __name__ == "__main__":
    main()
