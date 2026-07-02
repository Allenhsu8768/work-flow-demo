from db_model import model_register
from db_model.db_connect import db_session

loaddata = {
    "department": [
        {
            "id" : 2,
            "department_name" : "後台管理部門",
            "manager_id" : 2,
            "create_time" : "2026-06-22T22:42:34.380Z",
            "update_time" : "2026-06-22T22:46:04.771Z"
        },
        {
            "id" : 1,
            "department_name" : "人事部門",
            "manager_id" : 3,
            "create_time" : "2026-06-22T22:42:34.380Z",
            "update_time" : "2026-06-22T22:48:19.501Z"
        },
        {
            "id" : 6,
            "department_name" : "專案管理部",
            "manager_id" : 4,
            "create_time" : "2026-06-22T22:51:18.479Z",
            "update_time" : "2026-06-23T19:21:30.214Z"
        },
        {
            "id" : 4,
            "department_name" : "研發技術部",
            "manager_id" : 5,
            "create_time" : "2026-06-22T22:51:18.479Z",
            "update_time" : "2026-06-23T23:53:31.856Z"
        },
        {
            "id" : 5,
            "department_name" : "業務部",
            "manager_id" : 6,
            "create_time" : "2026-06-22T22:51:18.479Z",
            "update_time" : "2026-06-23T23:54:16.113Z"
        },
        {
            "id" : 7,
            "department_name" : "行政部門",
            "manager_id" : 7,
            "create_time" : "2026-06-23T18:10:01.824Z",
            "update_time" : "2026-06-23T23:54:28.317Z"
        }
    ],
    "users": [
        {
            "id" : 1,
            "name" : "Allen",
            "email" : "notbook7787@gmail.com",
            "password" : "qwe66519",
            "root_user" : True,
            "department_id" : 2,
            "create_time" : "2026-06-22T22:45:25.060Z",
            "update_time" : "2026-06-22T22:45:25.060Z"
        },
        {
            "id" : 2,
            "name" : "Tommy",
            "email" : "Tommy@gmail.com",
            "password" : "qwe66519",
            "root_user" : False,
            "department_id" : 1,
            "create_time" : "2026-06-22T22:48:15.683Z",
            "update_time" : "2026-06-22T22:48:15.683Z"
        },
        {
            "id" : 3,
            "name" : "Ellen",
            "email" : "Ellen@gmail.com",
            "password" : "qwe66519",
            "root_user" : False,
            "department_id" : 6,
            "create_time" : "2026-06-23T19:20:54.538Z",
            "update_time" : "2026-06-23T19:20:54.538Z"
        },
        {
            "id" : 4,
            "name" : "Alice Wang",
            "email" : "alice.wang@example.com",
            "password" : "qwe66519",
            "root_user" : False,
            "department_id" : 1,
            "create_time" : "2026-06-23T22:32:40.863Z",
            "update_time" : "2026-06-23T22:32:40.863Z"
        },
        {
            "id" : 5,
            "name" : "Bob Li",
            "email" : "bob.li@example.com",
            "password" : "qwe66519",
            "root_user" : False,
            "department_id" : 1,
            "create_time" : "2026-06-23T22:32:40.863Z",
            "update_time" : "2026-06-23T22:32:40.863Z"
        },
        {
            "id" : 6,
            "name" : "Carol Chen",
            "email" : "carol.chen@example.com",
            "password" : "qwe66519",
            "root_user" : False,
            "department_id" : 1,
            "create_time" : "2026-06-23T22:32:40.863Z",
            "update_time" : "2026-06-23T22:32:40.863Z"
        },
        {
            "id" : 7,
            "name" : "David Huang",
            "email" : "david.huang@example.com",
            "password" : "qwe66519",
            "root_user" : False,
            "department_id" : 2,
            "create_time" : "2026-06-23T22:32:40.863Z",
            "update_time" : "2026-06-23T22:32:40.863Z"
        },
        {
            "id" : 8,
            "name" : "Eva Liu",
            "email" : "eva.liu@example.com",
            "password" : "qwe66519",
            "root_user" : False,
            "department_id" : 2,
            "create_time" : "2026-06-23T22:32:40.863Z",
            "update_time" : "2026-06-23T22:32:40.863Z"
        },
        {
            "id" : 9,
            "name" : "Frank Chang",
            "email" : "frank.chang@example.com",
            "password" : "qwe66519",
            "root_user" : False,
            "department_id" : 4,
            "create_time" : "2026-06-23T22:32:40.863Z",
            "update_time" : "2026-06-23T22:32:40.863Z"
        },
        {
            "id" : 10,
            "name" : "Grace Yang",
            "email" : "grace.yang@example.com",
            "password" : "qwe66519",
            "root_user" : False,
            "department_id" : 4,
            "create_time" : "2026-06-23T22:32:40.863Z",
            "update_time" : "2026-06-23T22:32:40.863Z"
        },
        {
            "id" : 11,
            "name" : "Henry Wu",
            "email" : "henry.wu@example.com",
            "password" : "qwe66519",
            "root_user" : False,
            "department_id" : 5,
            "create_time" : "2026-06-23T22:32:40.863Z",
            "update_time" : "2026-06-23T22:32:40.863Z"
        },
        {
            "id" : 12,
            "name" : "Irene Lin",
            "email" : "irene.lin@example.com",
            "password" : "qwe66519",
            "root_user" : False,
            "department_id" : 7,
            "create_time" : "2026-06-23T22:32:40.863Z",
            "update_time" : "2026-06-23T22:32:40.863Z"
        },
        {
            "id" : 13,
            "name" : "Jack Zhou",
            "email" : "jack.zhou@example.com",
            "password" : "qwe66519",
            "root_user" : False,
            "department_id" : 6,
            "create_time" : "2026-06-23T22:32:40.863Z",
            "update_time" : "2026-06-23T22:32:40.863Z"
        }
    ],
    "leave_type": [
        {
            "id" : 2,
            "type" : "病假",
            "description" : "因疾病或醫療原因所請的休假",
            "create_time" : "2026-06-23T18:15:28.610Z",
            "update_time" : "2026-06-23T18:15:28.610Z"
        },
        {
            "id" : 3,
            "type" : "事假",
            "description" : "個人私事需要請假的休假",
            "create_time" : "2026-06-23T18:15:28.610Z",
            "update_time" : "2026-06-23T18:15:28.610Z"
        },
        {
            "id" : 4,
            "type" : "婚假",
            "description" : "配偶結婚時所請的休假",
            "create_time" : "2026-06-23T18:15:28.610Z",
            "update_time" : "2026-06-23T18:15:28.610Z"
        },
        {
            "id" : 5,
            "type" : "喪假",
            "description" : "因親屬逝世、需要處理後事或照顧家庭所提供的休假.",
            "create_time" : "2026-06-23T19:16:08.589Z",
            "update_time" : "2026-06-23T19:16:08.589Z"
        },
        {
            "id" : 1,
            "type" : "特休假",
            "description" : "公司規定的年度帶薪休假",
            "create_time" : "2026-06-23T18:15:28.610Z",
            "update_time" : "2026-06-23T18:15:28.610Z"
        }
    ],
    "department_manager": [
        {
            "id" : 2,
            "user_id" : 1,
            "is_ceo" : False,
            "create_time" : "2026-06-22T22:45:56.709Z",
            "update_time" : "2026-06-22T22:45:56.709Z"
        },
        {
            "id" : 3,
            "user_id" : 2,
            "is_ceo" : False,
            "create_time" : "2026-06-22T22:48:17.618Z",
            "update_time" : "2026-06-22T22:48:17.618Z"
        },
        {
            "id" : 4,
            "user_id" : 3,
            "is_ceo" : False,
            "create_time" : "2026-06-23T19:21:19.335Z",
            "update_time" : "2026-06-23T19:21:19.335Z"
        },
        {
            "id" : 5,
            "user_id" : 9,
            "is_ceo" : False,
            "create_time" : "2026-06-23T23:53:16.035Z",
            "update_time" : "2026-06-23T23:53:16.035Z"
        },
        {
            "id" : 6,
            "user_id" : 11,
            "is_ceo" : False,
            "create_time" : "2026-06-23T23:54:10.242Z",
            "update_time" : "2026-06-23T23:54:10.242Z"
        },
        {
            "id" : 7,
            "user_id" : 12,
            "is_ceo" : False,
            "create_time" : "2026-06-23T23:54:22.268Z",
            "update_time" : "2026-06-23T23:54:22.268Z"
        }
    ],
    "leave_request_day_record": [
        {
            "id" : 2,
            "leave_type_id" : 1,
            "user_id" : 2,
            "days" : 14,
            "create_time" : "2026-06-23T21:40:02.741Z",
            "update_time" : "2026-06-23T21:40:02.741Z"
        },
        {
            "id" : 3,
            "leave_type_id" : 1,
            "user_id" : 3,
            "days" : 14,
            "create_time" : "2026-06-23T21:40:02.741Z",
            "update_time" : "2026-06-23T21:40:02.741Z"
        },
        {
            "id" : 4,
            "leave_type_id" : 2,
            "user_id" : 1,
            "days" : 30,
            "create_time" : "2026-06-23T21:40:02.741Z",
            "update_time" : "2026-06-23T21:40:02.741Z"
        },
        {
            "id" : 5,
            "leave_type_id" : 2,
            "user_id" : 2,
            "days" : 30,
            "create_time" : "2026-06-23T21:40:02.741Z",
            "update_time" : "2026-06-23T21:40:02.741Z"
        },
        {
            "id" : 6,
            "leave_type_id" : 2,
            "user_id" : 3,
            "days" : 30,
            "create_time" : "2026-06-23T21:40:02.741Z",
            "update_time" : "2026-06-23T21:40:02.741Z"
        },
        {
            "id" : 7,
            "leave_type_id" : 3,
            "user_id" : 1,
            "days" : 18,
            "create_time" : "2026-06-23T21:40:02.741Z",
            "update_time" : "2026-06-23T21:40:02.741Z"
        },
        {
            "id" : 8,
            "leave_type_id" : 3,
            "user_id" : 2,
            "days" : 18,
            "create_time" : "2026-06-23T21:40:02.741Z",
            "update_time" : "2026-06-23T21:40:02.741Z"
        },
        {
            "id" : 9,
            "leave_type_id" : 3,
            "user_id" : 3,
            "days" : 18,
            "create_time" : "2026-06-23T21:40:02.741Z",
            "update_time" : "2026-06-23T21:40:02.741Z"
        },
        {
            "id" : 10,
            "leave_type_id" : 4,
            "user_id" : 1,
            "days" : 8,
            "create_time" : "2026-06-23T21:40:02.741Z",
            "update_time" : "2026-06-23T21:40:02.741Z"
        },
        {
            "id" : 11,
            "leave_type_id" : 4,
            "user_id" : 2,
            "days" : 8,
            "create_time" : "2026-06-23T21:40:02.741Z",
            "update_time" : "2026-06-23T21:40:02.741Z"
        },
        {
            "id" : 12,
            "leave_type_id" : 4,
            "user_id" : 3,
            "days" : 8,
            "create_time" : "2026-06-23T21:40:02.741Z",
            "update_time" : "2026-06-23T21:40:02.741Z"
        },
        {
            "id" : 13,
            "leave_type_id" : 5,
            "user_id" : 1,
            "days" : 8,
            "create_time" : "2026-06-23T21:40:02.741Z",
            "update_time" : "2026-06-23T21:40:02.741Z"
        },
        {
            "id" : 14,
            "leave_type_id" : 5,
            "user_id" : 2,
            "days" : 8,
            "create_time" : "2026-06-23T21:40:02.741Z",
            "update_time" : "2026-06-23T21:40:02.741Z"
        },
        {
            "id" : 15,
            "leave_type_id" : 5,
            "user_id" : 3,
            "days" : 8,
            "create_time" : "2026-06-23T21:40:02.741Z",
            "update_time" : "2026-06-23T21:40:02.741Z"
        },
        {
            "id" : 1,
            "leave_type_id" : 1,
            "user_id" : 1,
            "days" : 18,
            "create_time" : "2026-06-23T21:40:02.741Z",
            "update_time" : "2026-06-23T21:47:29.933Z"
        },
        {
            "id" : 16,
            "leave_type_id" : 2,
            "user_id" : 11,
            "days" : 30,
            "create_time" : "2026-06-23T22:49:54.488Z",
            "update_time" : "2026-06-23T22:49:54.488Z"
        },
        {
            "id" : 17,
            "leave_type_id" : 1,
            "user_id" : 11,
            "days" : 12,
            "create_time" : "2026-06-23T22:49:54.488Z",
            "update_time" : "2026-06-23T22:49:54.488Z"
        },
        {
            "id" : 18,
            "leave_type_id" : 3,
            "user_id" : 11,
            "days" : 18,
            "create_time" : "2026-06-23T22:49:54.488Z",
            "update_time" : "2026-06-23T22:49:54.488Z"
        },
        {
            "id" : 19,
            "leave_type_id" : 4,
            "user_id" : 11,
            "days" : 8,
            "create_time" : "2026-06-23T22:49:54.488Z",
            "update_time" : "2026-06-23T22:49:54.488Z"
        },
        {
            "id" : 20,
            "leave_type_id" : 5,
            "user_id" : 11,
            "days" : 8,
            "create_time" : "2026-06-23T22:49:54.488Z",
            "update_time" : "2026-06-23T22:49:54.488Z"
        },
        {
            "id" : 21,
            "leave_type_id" : 2,
            "user_id" : 12,
            "days" : 30,
            "create_time" : "2026-06-23T22:49:54.488Z",
            "update_time" : "2026-06-23T22:49:54.488Z"
        },
        {
            "id" : 22,
            "leave_type_id" : 1,
            "user_id" : 12,
            "days" : 12,
            "create_time" : "2026-06-23T22:49:54.488Z",
            "update_time" : "2026-06-23T22:49:54.488Z"
        },
        {
            "id" : 23,
            "leave_type_id" : 3,
            "user_id" : 12,
            "days" : 18,
            "create_time" : "2026-06-23T22:49:54.488Z",
            "update_time" : "2026-06-23T22:49:54.488Z"
        },
        {
            "id" : 24,
            "leave_type_id" : 4,
            "user_id" : 12,
            "days" : 8,
            "create_time" : "2026-06-23T22:49:54.488Z",
            "update_time" : "2026-06-23T22:49:54.488Z"
        },
        {
            "id" : 25,
            "leave_type_id" : 5,
            "user_id" : 12,
            "days" : 8,
            "create_time" : "2026-06-23T22:49:54.488Z",
            "update_time" : "2026-06-23T22:49:54.488Z"
        },
        {
            "id" : 26,
            "leave_type_id" : 2,
            "user_id" : 10,
            "days" : 30,
            "create_time" : "2026-06-23T22:49:54.488Z",
            "update_time" : "2026-06-23T22:49:54.488Z"
        },
        {
            "id" : 27,
            "leave_type_id" : 1,
            "user_id" : 10,
            "days" : 12,
            "create_time" : "2026-06-23T22:49:54.488Z",
            "update_time" : "2026-06-23T22:49:54.488Z"
        },
        {
            "id" : 28,
            "leave_type_id" : 3,
            "user_id" : 10,
            "days" : 18,
            "create_time" : "2026-06-23T22:49:54.488Z",
            "update_time" : "2026-06-23T22:49:54.488Z"
        },
        {
            "id" : 29,
            "leave_type_id" : 4,
            "user_id" : 10,
            "days" : 8,
            "create_time" : "2026-06-23T22:49:54.488Z",
            "update_time" : "2026-06-23T22:49:54.488Z"
        },
        {
            "id" : 30,
            "leave_type_id" : 5,
            "user_id" : 10,
            "days" : 8,
            "create_time" : "2026-06-23T22:49:54.488Z",
            "update_time" : "2026-06-23T22:49:54.488Z"
        },
        {
            "id" : 31,
            "leave_type_id" : 2,
            "user_id" : 13,
            "days" : 30,
            "create_time" : "2026-06-23T22:49:54.488Z",
            "update_time" : "2026-06-23T22:49:54.488Z"
        },
        {
            "id" : 32,
            "leave_type_id" : 1,
            "user_id" : 13,
            "days" : 12,
            "create_time" : "2026-06-23T22:49:54.488Z",
            "update_time" : "2026-06-23T22:49:54.488Z"
        },
        {
            "id" : 33,
            "leave_type_id" : 3,
            "user_id" : 13,
            "days" : 18,
            "create_time" : "2026-06-23T22:49:54.488Z",
            "update_time" : "2026-06-23T22:49:54.488Z"
        },
        {
            "id" : 34,
            "leave_type_id" : 4,
            "user_id" : 13,
            "days" : 8,
            "create_time" : "2026-06-23T22:49:54.488Z",
            "update_time" : "2026-06-23T22:49:54.488Z"
        },
        {
            "id" : 35,
            "leave_type_id" : 5,
            "user_id" : 13,
            "days" : 8,
            "create_time" : "2026-06-23T22:49:54.488Z",
            "update_time" : "2026-06-23T22:49:54.488Z"
        },
        {
            "id" : 36,
            "leave_type_id" : 2,
            "user_id" : 5,
            "days" : 30,
            "create_time" : "2026-06-23T22:49:54.488Z",
            "update_time" : "2026-06-23T22:49:54.488Z"
        },
        {
            "id" : 37,
            "leave_type_id" : 1,
            "user_id" : 5,
            "days" : 12,
            "create_time" : "2026-06-23T22:49:54.488Z",
            "update_time" : "2026-06-23T22:49:54.488Z"
        },
        {
            "id" : 38,
            "leave_type_id" : 3,
            "user_id" : 5,
            "days" : 18,
            "create_time" : "2026-06-23T22:49:54.488Z",
            "update_time" : "2026-06-23T22:49:54.488Z"
        },
        {
            "id" : 39,
            "leave_type_id" : 4,
            "user_id" : 5,
            "days" : 8,
            "create_time" : "2026-06-23T22:49:54.488Z",
            "update_time" : "2026-06-23T22:49:54.488Z"
        },
        {
            "id" : 40,
            "leave_type_id" : 5,
            "user_id" : 5,
            "days" : 8,
            "create_time" : "2026-06-23T22:49:54.488Z",
            "update_time" : "2026-06-23T22:49:54.488Z"
        },
        {
            "id" : 41,
            "leave_type_id" : 2,
            "user_id" : 8,
            "days" : 30,
            "create_time" : "2026-06-23T22:49:54.488Z",
            "update_time" : "2026-06-23T22:49:54.488Z"
        },
        {
            "id" : 42,
            "leave_type_id" : 1,
            "user_id" : 8,
            "days" : 12,
            "create_time" : "2026-06-23T22:49:54.488Z",
            "update_time" : "2026-06-23T22:49:54.488Z"
        },
        {
            "id" : 43,
            "leave_type_id" : 3,
            "user_id" : 8,
            "days" : 18,
            "create_time" : "2026-06-23T22:49:54.488Z",
            "update_time" : "2026-06-23T22:49:54.488Z"
        },
        {
            "id" : 44,
            "leave_type_id" : 4,
            "user_id" : 8,
            "days" : 8,
            "create_time" : "2026-06-23T22:49:54.488Z",
            "update_time" : "2026-06-23T22:49:54.488Z"
        },
        {
            "id" : 45,
            "leave_type_id" : 5,
            "user_id" : 8,
            "days" : 8,
            "create_time" : "2026-06-23T22:49:54.488Z",
            "update_time" : "2026-06-23T22:49:54.488Z"
        },
        {
            "id" : 46,
            "leave_type_id" : 2,
            "user_id" : 6,
            "days" : 30,
            "create_time" : "2026-06-23T22:49:54.488Z",
            "update_time" : "2026-06-23T22:49:54.488Z"
        },
        {
            "id" : 47,
            "leave_type_id" : 1,
            "user_id" : 6,
            "days" : 12,
            "create_time" : "2026-06-23T22:49:54.488Z",
            "update_time" : "2026-06-23T22:49:54.488Z"
        },
        {
            "id" : 48,
            "leave_type_id" : 3,
            "user_id" : 6,
            "days" : 18,
            "create_time" : "2026-06-23T22:49:54.488Z",
            "update_time" : "2026-06-23T22:49:54.488Z"
        },
        {
            "id" : 49,
            "leave_type_id" : 4,
            "user_id" : 6,
            "days" : 8,
            "create_time" : "2026-06-23T22:49:54.488Z",
            "update_time" : "2026-06-23T22:49:54.488Z"
        },
        {
            "id" : 50,
            "leave_type_id" : 5,
            "user_id" : 6,
            "days" : 8,
            "create_time" : "2026-06-23T22:49:54.488Z",
            "update_time" : "2026-06-23T22:49:54.488Z"
        },
        {
            "id" : 51,
            "leave_type_id" : 2,
            "user_id" : 4,
            "days" : 30,
            "create_time" : "2026-06-23T22:49:54.488Z",
            "update_time" : "2026-06-23T22:49:54.488Z"
        },
        {
            "id" : 52,
            "leave_type_id" : 1,
            "user_id" : 4,
            "days" : 12,
            "create_time" : "2026-06-23T22:49:54.488Z",
            "update_time" : "2026-06-23T22:49:54.488Z"
        },
        {
            "id" : 53,
            "leave_type_id" : 3,
            "user_id" : 4,
            "days" : 18,
            "create_time" : "2026-06-23T22:49:54.488Z",
            "update_time" : "2026-06-23T22:49:54.488Z"
        },
        {
            "id" : 54,
            "leave_type_id" : 4,
            "user_id" : 4,
            "days" : 8,
            "create_time" : "2026-06-23T22:49:54.488Z",
            "update_time" : "2026-06-23T22:49:54.488Z"
        },
        {
            "id" : 55,
            "leave_type_id" : 5,
            "user_id" : 4,
            "days" : 8,
            "create_time" : "2026-06-23T22:49:54.488Z",
            "update_time" : "2026-06-23T22:49:54.488Z"
        },
        {
            "id" : 56,
            "leave_type_id" : 2,
            "user_id" : 9,
            "days" : 30,
            "create_time" : "2026-06-23T22:49:54.488Z",
            "update_time" : "2026-06-23T22:49:54.488Z"
        },
        {
            "id" : 57,
            "leave_type_id" : 1,
            "user_id" : 9,
            "days" : 12,
            "create_time" : "2026-06-23T22:49:54.488Z",
            "update_time" : "2026-06-23T22:49:54.488Z"
        },
        {
            "id" : 58,
            "leave_type_id" : 3,
            "user_id" : 9,
            "days" : 18,
            "create_time" : "2026-06-23T22:49:54.488Z",
            "update_time" : "2026-06-23T22:49:54.488Z"
        },
        {
            "id" : 59,
            "leave_type_id" : 4,
            "user_id" : 9,
            "days" : 8,
            "create_time" : "2026-06-23T22:49:54.488Z",
            "update_time" : "2026-06-23T22:49:54.488Z"
        },
        {
            "id" : 60,
            "leave_type_id" : 5,
            "user_id" : 9,
            "days" : 8,
            "create_time" : "2026-06-23T22:49:54.488Z",
            "update_time" : "2026-06-23T22:49:54.488Z"
        },
        {
            "id" : 61,
            "leave_type_id" : 2,
            "user_id" : 7,
            "days" : 30,
            "create_time" : "2026-06-23T22:49:54.488Z",
            "update_time" : "2026-06-23T22:49:54.488Z"
        },
        {
            "id" : 62,
            "leave_type_id" : 1,
            "user_id" : 7,
            "days" : 12,
            "create_time" : "2026-06-23T22:49:54.488Z",
            "update_time" : "2026-06-23T22:49:54.488Z"
        },
        {
            "id" : 63,
            "leave_type_id" : 3,
            "user_id" : 7,
            "days" : 18,
            "create_time" : "2026-06-23T22:49:54.488Z",
            "update_time" : "2026-06-23T22:49:54.488Z"
        },
        {
            "id" : 64,
            "leave_type_id" : 4,
            "user_id" : 7,
            "days" : 8,
            "create_time" : "2026-06-23T22:49:54.488Z",
            "update_time" : "2026-06-23T22:49:54.488Z"
        },
        {
            "id" : 65,
            "leave_type_id" : 5,
            "user_id" : 7,
            "days" : 8,
            "create_time" : "2026-06-23T22:49:54.488Z",
            "update_time" : "2026-06-23T22:49:54.488Z"
        }
    ]
} 



def process_data(load_data):
    for tablename, records in load_data.items():
        print(f"Processing table: {tablename}")
        model_cls = model_register.get(tablename, None)
        
        with db_session() as session:
            if model_cls is not None:
                for record in records:
                    # Check if the record already exists based on the primary key
                    existing_record = session.get(model_cls, record['id'])
                    if existing_record:
                        # Update the existing record
                        for key, value in record.items():
                            setattr(existing_record, key, value)
                    else:
                        # Create a new record
                        new_record = model_cls(**record)
                        session.add(new_record)
            else:
                print(f"No model class found for table: {tablename}")
        print(f"Finished processing table: {tablename}\n")
        
    return load_data


if __name__ == "__main__":
    process_data(loaddata)