import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
from docx import Document
from docx.oxml import OxmlElement
from docx import Document
from docx.shared import Inches
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import time



def parser2(string_to_put_in_search:str,date_from:str,date_up:str):
    def add_hyperlink(paragraph, text, url):
        
        # Получаем идентификатор ссылки (relationship id)
        rel_id = paragraph.part.relate_to(url, 'hyperlink', is_external=True)
        
        # Создаем элемент гиперссылки
        hyperlink = OxmlElement('w:hyperlink', {qn('r:id'): rel_id})
        
        # Создаем элемент 'run' и 'text'
        run = OxmlElement('w:r')
        t = OxmlElement('w:t')
        t.text = text
        run.append(t)

        # Создаем свойства для текста (например, подчеркивание и цвет)
        run_properties = OxmlElement('w:rPr')

        # Подчеркивание
        underline = OxmlElement('w:u')
        underline.set(qn('w:val'), 'single')
        run_properties.append(underline)

        # Цвет шрифта
        color = OxmlElement('w:color')
        color.set(qn('w:val'), '0000FF')  # Синий цвет
        run_properties.append(color)

        # Добавляем свойства к run
        run.append(run_properties)

        # Добавляем run в гиперссылку
        hyperlink.append(run)

        # Добавляем гиперссылку в параграф
        paragraph._element.append(hyperlink)

    def parse_SC(search_string:str,date_from:str,date_up:str)->list[list[tuple,tuple,tuple]]:
        # Настройка Selenium
        firefox_options = webdriver.FirefoxOptions()
        firefox_options.add_argument('--headless')  # Оставьте это для фона
        firefox_options.add_argument('--disable-gpu')
        driver = webdriver.Firefox(options=firefox_options)

        # options=firefox_options

        # Открытие сайта и выполнение поиска
        try:
            driver.get('https://vsrf.ru/lk/practice/acts')

            WebDriverWait(driver, 20).until(
                lambda driver: driver.execute_script('return document.readyState') == 'complete'
            )

            # Ожидание загрузки поля поиска
            tick_box = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="numberExact"]'))  # Change to more specific selector if needed
            )
            if tick_box.is_selected():
                tick_box.click()

            # Выбор даты
            from_date = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="actDateFrom"]'))
            )
            to_date = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="actDateTo"]'))
            )
            from_date.send_keys(date_from)
            to_date.send_keys(date_up)

            search_box = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="keywords"]'))  # Change to more specific selector if needed
            )
            search_box.send_keys(search_string)

            # Нажатие на кнопку "Поиск"
            search_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="filter-form"]/div[1]/div[1]/div[2]/div/div[1]/input'))  # Using clickable condition
            )
            search_button.click()

            time.sleep(3)


            # Ожидание загрузки основного контейнера
            container = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div/div[2]/div/div/div[2]/div"))
            )
            # print(container.get_attribute('outerHTML'))

            # print("Контейнер найден!")


            # Извлечение всех элементов с классом, который содержит 'vs-items-body'
            item_bodies = container.find_elements(By.XPATH, "//*[contains(@class, 'vs-items-body')]")

            # Хранилище для данных
            table_data = []

            # Проверка, нашлись ли элементы
            if item_bodies:
                print(f"Найдено {len(item_bodies)} элементов с классом 'vs-items-body'.")

                # Проход по каждому элементу 'vs-items-body'
                for item_body in item_bodies:
                    # Для каждой строки (элемента с классом 'row') извлекаем данные
                    rows = item_body.find_elements(By.XPATH, ".//*[contains(@class, 'row')]")
                    row_data = {}
                    
                    # Извлечение даты (предполагаем, что дата находится в элементе с классом, содержащим 'vs-font-20')
                    date_element = item_body.find_element(By.XPATH, ".//*[contains(@class, 'vs-font-20')]")
                    if date_element:
                        row_data['date'] = date_element.text.strip()  # Убираем лишние пробелы
                    
                    # Извлечение всех деталей иерархии (элементы с классом, содержащим 'vs-item-detail')
                    link_names = item_body.find_elements(By.XPATH, ".//*[contains(@class, 'vs-items-label')]")
                    row_data['link_name'] = [link_name.text.strip() for link_name in link_names if link_name.text.strip()]

                    link_source = item_body.find_elements(By.XPATH, ".//*[contains(@class, 'vs-items-label')]")

                    if link_source:
                        # Получаем ссылки из всех найденных элементов
                        row_data['link_source'] = []
                        for item in link_source:
                            # Находим ссылку внутри каждого элемента
                            link = item.find_element(By.TAG_NAME, 'a')
                            if link:
                                row_data['link_source'].append(link.get_attribute('href'))
                    else:
                        row_data['link_source'] = None
                    
                    # Добавляем собранные данные в таблицу
                    table_data.append(row_data)

                # Вывод данных
                for data in table_data:
                    print(f"Дата: {data.get('date', 'Дата не найдена')}")
                    print(f"Название ссылки: {', '.join(data.get('link_name', []))}")
                    print(f"Ссылка на: {data.get('link_source', 'Дата не найдена')}")
            # else:
            #     print("Элементы с классом 'vs-items-body' не найдены.")


            # Выводим данные
            # for item in table_data:
            #     print(item)

            driver.quit()
            return table_data

        except Exception as e:
            print(f"Error during Selenium script execution: {e}")

        finally:
            driver.quit()



    def add_to_word_file(table_data:list):
        if table_data:
            doc = Document()
            doc.add_heading('Судебная практика КС РФ', 0)
            
            bold_paragraph = doc.add_paragraph()
            bold_run = bold_paragraph.add_run('1. Конституционный Суд РФ:')
            bold_run.bold = True
            
            for record in table_data:
                paragraph = doc.add_paragraph()
                link_text = f"Постановление от {record['date']} № {record['link_name']}"
                add_hyperlink(paragraph, link_text, record['link_source'][0])
                link = f"Ссылка на документ{record['link_source']}"
                # doc.add_paragraph(link_text)
                # doc.add_paragraph(link)
            
            doc.save('Судебная_практика_1.docx')
            print("Документ успешно создан!")
        else:
            print("Не было найдено никаких решений.")

    
    add_to_word_file(parse_SC(string_to_put_in_search,date_from,date_up))