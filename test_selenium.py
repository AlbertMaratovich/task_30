from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


def test_petfriends():
    # Open PetFriends base page:
    driver = webdriver.Chrome()
    driver.get('https://petfriends.skillfactory.ru/')
    driver.set_window_size(1920, 1080)

    element = WebDriverWait(driver, 10).until(lambda x: x.find_element("xpath", "//button[@class='btn btn-success']"))

    # click on the new user button
    btn_newuser = driver.find_element("xpath", "(//button[@class='btn btn-success'])")

    btn_newuser.click()
    element = WebDriverWait(driver, 10).until(lambda x: x.find_element("xpath", "//button[@class='btn btn-success']"))

    # click existing user button
    btn_exist_acc = driver.find_element("xpath", "(//div[@class='text-center']/a)")
    btn_exist_acc.click()
    element = WebDriverWait(driver, 10).until(lambda x: x.find_element("xpath", "//button[@class='btn btn-success']"))

    # add email
    field_email = driver.find_element("id", "email")
    field_email.clear()
    field_email.send_keys("cucumber@mail.com")

    # add password
    field_pass = driver.find_element("id", "pass")
    field_pass.clear()
    field_pass.send_keys("cucumber666")

    # click submit button
    btn_submit = driver.find_element("xpath", "//button[@type='submit']")
    btn_submit.click()
    driver.implicitly_wait(10)

    """Here start homework tasks"""

    # click my pets button
    btn_mypets = driver.find_element("xpath", "//div/ul/li/a[contains(text(),'Мои питомцы')]")
    btn_mypets.click()

    # get number of pets
    get_text_of_pets = driver.find_element("xpath", "//div/div/div[@class='.col-sm-4 left']").text
    string_of_pets = ""
    for i in get_text_of_pets.split("\n")[1]:
        if i.isdigit():
            string_of_pets += i
            if int(string_of_pets) == 0:
                raise Exception("there are no pets in this account")
    number_of_pets = int(string_of_pets)

    # get and check list of pets
    list_of_pets = driver.find_elements("xpath", "//tbody/tr")
    assert len(list_of_pets) == number_of_pets

    # check pets with photo more than a half
    list_of_pets_photo = driver.find_elements("xpath", "//tbody/tr/th/img")
    counter = 0
    for i in range(len(list_of_pets_photo)):
        if list_of_pets_photo[i].get_attribute('src') != '':
            counter += 1
    assert counter >= number_of_pets//2

    # check that all pets have name, age and poroda
    for i in range(len(list_of_pets)):
        characters = driver.find_elements("xpath", "//tbody/tr/td")
        for k in range(len(characters)):
            assert characters[k].text != ""

    # check that pets have unique names
    names = driver.find_elements("xpath", "//tbody/tr/td[1]")
    for i in range(len(list_of_pets)):
        assert names[i].text != ""

    # check that user doesnt have the same pets
    pets = []
    for i in range(len(list_of_pets)):
        dicty = {}
        porodas = driver.find_elements("xpath", "//tbody/tr/td[2]")
        ages = driver.find_elements("xpath", "//tbody/tr/td[3]")
        dicty["name"] = names[i].text
        dicty["poroda"] = porodas[i].text
        dicty["age"] = ages[i].text
        pets.append(dicty)
    for i in pets:
        counted = pets.count(i)
        if counted > 1:
            raise Exception("there are the same pets in list")
