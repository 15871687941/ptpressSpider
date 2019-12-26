import requests
import math

# 1、取得所有大类的API:https://www.ptpress.com.cn/bookinfo/getFirstParent GET 无参数

# 2、取得大类下面的小类API:https://www.ptpress.com.cn/bookinfo/getBookTagByParentId POST 参数
# parentId: a15a734f-0ae9-41d7-9012-6ef9de2e71c8

# 3、书籍列表API:https://www.ptpress.com.cn/bookinfo/getBookListForEBTag POST 参数
# page: 1
# rows: 18
# bookTagId: a15a734f-0ae9-41d7-9012-6ef9de2e71c8
# orderStr: hot

# 4、书籍详情API:https://www.ptpress.com.cn/bookinfo/getBookDetailsById
# bookId: b255ec08-2a95-4c21-b58b-432f4ebbc1fa

session = requests.session()

parentCategoryUrl = "https://www.ptpress.com.cn/bookinfo/getFirstParent"

subCategoryUrl = "https://www.ptpress.com.cn/bookinfo/getBookTagByParentId"

bookListUrl = "https://www.ptpress.com.cn/bookinfo/getBookListForEBTag"

bookDetailUrl = "https://www.ptpress.com.cn/bookinfo/getBookDetailsById"


response = session.get(url=parentCategoryUrl)

if response.status_code != 200:
    raise Exception("父类目录估计有什么反爬措施，请添加相应的防反爬措施!!!")
for parentTag in response.json()["data"]:
    print(parentTag["tagId"], parentTag["tagName"])
    data = {
        "parentId": parentTag["tagId"]
    }
    response = session.post(url=subCategoryUrl, data=data)
    if response.status_code != 200:
        raise Exception("子类目录估计有什么反爬措施，请添加相应的防反爬措施!!!")
    for subTag in response.json()["data"]:
        print(subTag["tagId"], subTag["tagName"])
        data = {
            "page": 1,
            "rows": 18,
            "bookTagId": subTag["tagId"],
            "orderStr": "hot"
        }
        response = session.post(url=bookListUrl, data=data)
        if response.status_code != 200:
            raise Exception("书籍列表估计有什么反爬措施，请添加相应的防反爬措施!!!")
        bookCount = int(response.json()["data"]["total"])
        maxPage = math.ceil(bookCount / 18)
        for page in range(1, maxPage + 1):
            data["page"] = page
            response = session.post(url=bookListUrl, data=data)
            print(response.json())


