from django.test import Client
from django.db import connection


# Create your tests here.
# Please view: https://docs.djangoproject.com/en/3.2/topics/testing/overview/
c = Client()

# Sample check that you can access website
response = c.get("/gift/")
assert(response.status_code == 200)

# 1- Write the test confirming XSS vulnerability is fixed
xss_r_buy = c.get("/buy/", {"director":"200"})
assert(xss_r_buy.context['director'] is None);
xss_r_gift= c.get("/gift/", {"director":"200"})
assert(xss_r_gift.context['director'] is None);


# 2- Write the test confirming CSRF vulnerability is fixed
c.post("/register/", {"uname": "testUser1", "pword":"password", "pword2":"password"})
c.post("/login/", {"uname": "testUser1", "pword":"password", "pword2":"password"})

c.post("/register/", {"uname": "testUser2", "pword":"password", "pword2":"password"})
c.post("/login/", {"uname": "testUser2", "pword":"password", "pword2":"password"})

csrf_res=c.post("/gift/0/", {"amount":"9999", "username":"testUser1", "csrf":"false"})
assert(csrf_res.status_code==404)


# 3- Write the test confirming SQL Injection attack is fixed
with open('bad.gftcrd', 'rb') as fp:
    sql_r = c.post("/use/", {"card_supplied": "True", "card_data": fp,
    "card_fname": "bad.gftcrd" })
    assert(sql_r.context["card_found"] is None)
