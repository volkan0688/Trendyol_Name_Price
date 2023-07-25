from tkinter import *
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import os

window = Tk()
window.title("Trendyol - Name/Price List")
window.minsize(width=400, height=300)
window.config(padx=20, pady=20, background="grey")


def search_list():
    try:
        my_product = entry_product.get()
    except ValueError:
        print("Lütfen geçerli bir arama kelimesi girin.")
        return

    try:
        my_max = int(entry_max.get())
    except ValueError:
        print("Lütfen geçerli bir sayı girin.")
        return

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.maximize_window()
    driver.get("https://www.trendyol.com/")

    try:
        popup_close = WebDriverWait(driver, 10).until(
            expected_conditions.element_to_be_clickable((By.ID, "Combined-Shape")))
        popup_close.click()
    except Exception as e:
        print("Pop-up kapatılamadı:", e)

    WebDriverWait(driver, 10).until(expected_conditions.visibility_of_element_located(
        (By.XPATH, "/html/body/div[1]/div[1]/div/div[2]/div/div/div[2]/div/div/div/input")))
    search_bar = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/div[2]/div/div/div[2]/div/div/div/input")
    search_bar.send_keys(my_product)
    search_bar.send_keys(Keys.RETURN)

    WebDriverWait(driver, 10).until(expected_conditions.visibility_of_element_located((By.CLASS_NAME, "p-card-img")))

    with open('results.txt', 'w', encoding='utf-8') as f:
        product_id = 1
        while True:
            veri1 = driver.find_elements(By.CLASS_NAME, "p-card-img")
            veri2 = driver.find_elements(By.CLASS_NAME, "prc-box-dscntd")

            for index, (element1, element2) in enumerate(zip(veri1, veri2), start=1):
                name = element1.get_attribute("alt")
                price = element2.text
                f.write(f"{product_id}: Ürün Adı: {name}, Fiyatı: {price}\n")
                product_id += 1

                if product_id > my_max:
                    break

            if product_id > my_max:
                break

            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.SPACE)
            time.sleep(3)

    window.destroy()

    os.startfile('results.txt')




# Product label
label_product = Label(text="Aramak istediğiniz ürün:")
label_product.config(bg="grey", font=('Helvetica', 13, 'italic'))
label_product.config(padx=10, pady=10)
label_product.pack()

# Weight entry
entry_product = Entry(width=20)
entry_product.config(font=('Helvetica', 13, 'italic'))
entry_product.pack()
entry_product.focus()
entry_product.bind("<Return>", lambda event: search_list())

# Weight label
label_max = Label(text="Maksimum kaç ürün listelensin:")
label_max.config(bg="grey", font=('Helvetica', 13, 'italic'))
label_max.config(padx=10, pady=10)
label_max.pack()

# Weight entry
entry_max = Entry(width=20)
entry_max.config(font=('Helvetica', 13, 'italic'))
entry_max.pack()
entry_max.bind("<Return>", lambda event: search_list())

def button_clicked():
    search_list()

button = Button(text="Listele", command=search_list, font=('Helvetica', 13, 'italic'))
button.place(x=155, y=150)


window.mainloop()