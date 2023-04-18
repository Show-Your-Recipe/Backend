from typing import List
from uuid import uuid4

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.requests import Request

from app.common.consts import MAX_API_KEY, MAX_API_WHITELIST
from app.database.conn import db
from app.database.schema import Users, ApiKeys, ApiWhiteLists
from app import models as m
from app.errors import exceptions as ex
import string
import secrets

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

from app.models import MarketBag

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument("--single-process")
options.add_argument('--window-size=1920,1080')
options.add_argument("--disable-dev-shm-usage")

router = APIRouter(prefix='/market')

@router.post("/inbag")
async def register(market_info: MarketBag):

    # market(user_info.id, user_info.pw, user_info.item)
    driver = webdriver.Chrome('/usr/local/bin/chromedriver', chrome_options=options)
    driver.implicitly_wait(time_to_wait=5)

    driver.get("https://www.kurly.com/member/login")
    driver.find_element(By.XPATH, '//*[@id="__next"]/div[3]/div[2]/form/div[1]/div[1]/div/input').send_keys(market_info.id)
    driver.find_element(By.XPATH, '//*[@id="__next"]/div[3]/div[2]/form/div[1]/div[2]/div/input').send_keys(market_info.pw)
    driver.find_element(By.XPATH, '//*[@id="__next"]/div[3]/div[2]/form/div[3]/button[1]').click()

    driver.implicitly_wait(time_to_wait=5)
    time.sleep(3)

    driver.find_element(By.XPATH, '//*[@id="gnb_search"]').send_keys(market_info.item)
    driver.find_element(By.XPATH, '//*[@id="submit"]').click()

    # click the first food and add to cart
    time.sleep(5)
    driver.find_element(By.XPATH, '//*[@id="container"]/div/div[2]/div[2]/div[1]/div[2]').click()
    driver.find_element(By.XPATH, '//*[@id="product-atf"]/section/div[5]/div[3]/div/button').click()

    driver.quit()

    return "success"
    # return JSONResponse(status_code=400, content=dict(msg="NOT_SUPPORTED"))
