import requests


def get_auth_url():
    weibo_auth_url = "https://api.weibo.com/oauth2/authorize"
    redirect_url = "http://127.0.0.1:8000/complete/weibo/"
    auth_url = weibo_auth_url+"?client_id={client_id}&redirect_uri={redirect_url}".format(client_id=3561651994,
                                                                                          redirect_url=redirect_url)
    print(auth_url)


def get_access_token(code=""):
    access_token_url = "https://api.weibo.com/oauth2/access_token"
    re_dict = requests.post(access_token_url, data={
        "client_id": 3561651994,
        "client_secret": "53457ae30997172ba08981b1f470d537",
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "http://34.87.131.11:8000/index/complete/weibo/",
    })
    pass


def get_user_info(access_token="", uid=""):
    user_url = "https://api.weibo.com/2/users/show.json?access_token={token}&uid={uid}".format(token=access_token,
                                                                                               uid=uid)
    print(user_url)

if __name__ == "__main__":
    get_auth_url()
    #get_access_token("7c4edaa94722a7dd81f4fdff506abba0")

    #get_user_info()