from logic.login import scan




def without_login(url):
    print("======================================================================")
    print("ALL LOGIN PAGE TESTS")
    scan(url)
    print("======================================================================")



def with_login():
    return

without_login("http://127.0.0.1:8080/login.php")