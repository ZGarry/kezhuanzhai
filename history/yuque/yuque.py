###
###
### 用这个可以创建一篇新的文档，但是总体而言，没什么用。做的东西太薄了，手动创建一下，一摸一样。提醒功能也是一样的。
### 而且还无法放入一篇目录中。不如做个跳转能力差不多饿了
import requests
token = "pOjxLEomTonND2KSTHDMbAqPyn2oxmak5UhjWTID"
API_PATH = "https://www.yuque.com/api/v2"
your_uid = "zfjz"


def get(url):
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "myYuque",
        "X-Auth-Token": token
    }
    response = requests.request(method='GET', url=url, headers=headers)
    return response.json()


def post(url, data):
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "myYuque",
        "X-Auth-Token": token
    }
    response = requests.request(method='POST', url=url, headers=headers, json=data)
    assert response.status_code == 200
    return response.json()


def user_info():
    return get(API_PATH + f"/users/{your_uid}")


def get_all_repo():
    return get(API_PATH + f"/users/{your_uid}/repos")


def find_repo_id_by_name(repo_name):
    for repo in get_all_repo()['data']:
        if repo['name'] == repo_name:
            return repo['id']

    raise RuntimeError(f"repo{repo_name}找不到")


def get_docs(repo_name):
    repo_id = find_repo_id_by_name(repo_name)
    return get(API_PATH + f'/repos/{repo_id}/docs')


# 返回yuque的doc格式
def find_doc(repo_name, doc_name):
    data = get_docs(repo_name)
    for doc in data['data']:
        if doc['title'] == doc_name:
            return doc

    raise RuntimeError(f"doc{doc_name}找不到")


# body_lake/body_html
def get_doc_detail(repo_name, doc_name):
    repo_id = find_repo_id_by_name(repo_name)
    doc = find_doc(repo_name, doc_name)
    slug = doc['slug']
    return get(API_PATH+f"/repos/{repo_id}/docs/{slug}")['data']


def copy_doc(repo_name, old_doc_name, new_doc_name):
    repo_id = find_repo_id_by_name(repo_name)
    content = get_doc_detail(repo_name, old_doc_name)['body_lake']
    data = {
        "title": new_doc_name,
        "format": 'lake',
        "body": content
    }
    return post(API_PATH + f"/repos/{repo_id}/docs", data)


def get_all_dir(repo_name):
    repo_id = find_repo_id_by_name(repo_name)
    return get(API_PATH + f"/repos/{repo_id}/toc")


def dir_uuid(repo_name, dir_name):
    for x in get_all_dir(repo_name)['data']:
        if x['title'] == dir_name:
            return x['uuid']

    raise RuntimeError(f"repo下{repo_name}节点{dir_name}找不到")


def append(doc_id, repo_name, dir_name):
    uuid = dir_uuid(repo_name, dir_name)
    repo_id = find_repo_id_by_name(repo_name)

    data = {
        "action": "appendByDocs",
        "doc_ids":  [doc_id],
        "target_uuid": uuid
    }
    return post(API_PATH + f"/repos/{repo_id}/toc", data)


# print(user_info())
# print(get_all_repo())
# print(find_repo_id_by_name("规划书"))
# print(get_docs("规划书"))
# print(find_doc("规划书", "复制页"))
# print(get_doc_detail("规划书", "财富自由规划书")['body_lake'])
# print(copy_doc("规划书", "财富自由规划书", "复制页"))
# print(get_all_dir("规划书"))
# print(dir_uuid("规划书", "财富自由规划书"))
doc = find_doc("规划书", "复制页")
# print(doc)
print(append(doc['id'], "规划书", "财富自由规划书"))
