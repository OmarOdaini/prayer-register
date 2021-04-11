from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from os.path import dirname, abspath
from time import sleep

def main(Registrants, Shifts):
    for person in Registrants:
        try:
            # New Chrome driver
            try: 
                driver = GetDriver()
            except Exception as error:
                print("Failed create a driver instance, Error: {}".format(error))
            

            ##### 1) Get to IAR Jummah page
            driver.get("https://raleighmasjid.org/jumaa")
            assert "The Islamic Association of Raleigh - Jumuah Registration" in driver.title


            ##### 2) Get to eventbrite registration page
            driver.get(GetLinkfromBtn("Register for Jumuah Shifts", driver))
            assert "IAR Jumu'ah Registration" in driver.title

            ##### 3) Click "Select A Date" (TODO: make it based on text instead)
            try: 
                GetLinkfromBtnByXPATH("//button[starts-with(@id, 'eventbrite-widget-modal-trigger-')]", driver).click()
            except Exception as error:
                print("Failed to find or click 'Select A Date', Error: {}".format(error))


            # switch iframe (to access pop-ups)
            try: 
                driver.switch_to.frame(driver.find_element_by_xpath("//iframe[starts-with(@id, 'eventbrite-widget-modal-')]"))
            except Exception as error:
                print("Failed to switch iframe, Error: {}".format(error))


            ##### 4) Select tickets for Jummah
            try: 
                ClickCatagory("Fri, 11:00 AM - 3:15 PM EDT", driver)
            except Exception as error:
                print("Failed to select tickets, Error: {}".format(error))


            ##### 5) Select a shift
            try: 
                SelectCatagory(Shifts[person['catagory']][person['timeslot']], driver)
                ClickRegister(driver)
            except Exception as error:
                print("Failed to select from shifts list, Error: {}".format(error))


            ##### 6) Fill out form
            try: 
                FillContactInfo(person['firstname'], person['lastname'], person['email'], person['phone'], driver)
                ClickRegister(driver)
            except Exception as error:
                print("Failed to fill out personal info page, Error: {}".format(error)) 

        except Exception as error:
            print("Failed to Register, Error: {}".format(error))
        else:
            sleep(5) 
            print("Tickets were sent to: {}".format(person['email']))
            driver.quit()

def GetDriver():
    # Chrome (chrome driver is assumed to be inside the same dir)
    chromePath = "{}/chromedriver".format(dirname(abspath(__file__)))
    # options object
    options = Options()
    # silent mode
    options.add_argument('--headless')
    options.add_argument('--disable-gpu') 
    return Chrome(chromePath, options=options)

def SelectCatagory(catagory, driver):
    # Select dropdown XPATH relative to catagory title
    TitletoSelectPath = "../../div[2]/div/div/div/div/div[2]/select"
    number = 1
    # Relateive XPATH based on catagory name
    incrementXPATH = "//h3[text()='{}']/{}/option[text()='{}']".format(catagory, TitletoSelectPath, number)
    # Increment 
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, incrementXPATH))).click()

def ClickCatagory(catagory, driver):
    btnText = "Tickets"
    # Relateive XPATH based on catagory name
    incrementXPATH = "//div[text()='{}']/../../../div[2]/div/button[text()='{}']".format(catagory, btnText)
    # click 
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, incrementXPATH))).click()

def FillContactInfo(fname, lname, email, phone, driver):
    # Text feild IDs
    inputForm = {
            "buyer.N-first_name" : fname,
            "buyer.N-last_name" : lname,
            "buyer.N-email" : email,
            "buyer.confirmEmailAddress" : email,
            "buyer.N-cell_phone" : phone
        }

    # clickables IDs
    clickables = [
        # COVID Questionnaire
        "radio-buyer.U-33803592-0",
        "radio-buyer.U-33803594-0",
        "radio-buyer.U-33803598-0",
        "radio-buyer.U-33956774-0",
        "radio-buyer.U-37596875-0",

        # marketing subscription (uncheck)
        "organizer-marketing-opt-in",
         "eb-marketing-opt-in"
        ]

    for key in inputForm:
        textFeild = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.ID, key)))
        textFeild.send_keys(inputForm[key])  
        
    for clickable in clickables:
        checkbox = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.ID, clickable)))
        driver.execute_script("arguments[0].click();", checkbox)

def ClickRegister(driver):
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[text()='Register']"))
    ).click()
    sleep(5)

def GetLinkfromBtn(text, driver):
    return WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, text))
    ).get_attribute('href')

def GetLinkfromBtnByXPATH(xpath, driver):
    return WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, xpath))
    )

if __name__ == "__main__":
    # People to register
    Registrants = [
        ############################################################################################Q
        # FOLLOW THE EXAMPLE BELOW FOR PESONAL INFO FORMAT (only update the right side after colon):
        # {
        #     "catagory": "men or women",
        #     "timeslot": "timeslot",
        #     "firstname": "firstname", 
        #     "lastname": "lastname",
        #     "email": "email to get tickets",
        #     "phone": "phone #"
        # }
        ############################################################################################
    ]
    # Shifts details
    Shifts = {
        "men": {
            "11:00": "Men 1st Shift (11:00 AM)",
            "12:00": "Men 2nd Shift (12:00 PM)",
            "1:00": "Men 3rd Shift (1:00 PM)",
            "3:00": "Men 4th Shift (3:00 PM)"
        },
        "women": {
            "11:00": "Women 1st Shift (11:00 AM)",
            "12:00": "Women 2nd Shift (12:00 PM)",
            "1:00": "Women 3rd Shift (1:00 PM)",
            "3:00": "Women 4th Shift (3:00 PM)"
        }
    }
    # call main function
    main(Registrants, Shifts)