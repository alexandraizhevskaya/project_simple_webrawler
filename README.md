## Маленький Web crawler

### Описание проекта
Проект содержит реализацию `web crawler`, который скачивает содержимое зааданной страницы, сохраняет его в директорию, 
а затем извлекакает все дочерние ссылки, указанные на странице, и рекурсивно обходит их до заданной глубины, обрабатывая таким же образом. 
Содержимое всех обработанных ссылок сохраняется в папку `data`. Каждой ссылке присваивается уникальный целочисленный id, который и служит названием html-файла. 

Пример названия файла: 
`3.html`

Кроме того, список всех обработанных ссылок сохраняется в файле `urls.txt`. Каждая строча содержит id и ссылку, разделенные пробелом.

Пример строки файла: 
`7 https://www.programiz.com/python-programming/datetime/strftime`

## Ограничения 
Основой `web crawler` являются библиотечки `requests` и `beautifoulsoup`. К сожалению, он не умеет обрабатывать блокировки:(

При возникновении подобных проблем появляется сообщение об ошибке: 

`Probably, the site is blocking crawler:(`

Также, если при отправке запроса пришел ответ, но его код не 200, появляется предупреждение, что ссылка была обработана, но статус не корректный:

`Request status code for id 12 is not 200. Please, searc the meaning of the following request status: 403`

#### *Важно*  
В текущей реализации если при запускке crawler у Вас уже есть папка `data` и файл  `urls.txt` - они будут удалены и перезаписаны результатом обхода запрошенной страницы.

### Использование
Сейчас в репозитории в качестве примера находятся директория`data` и файл `urls.txt`. Они были получены с помощью следующей команды:

```commandline
python main.py -url https://www.programiz.com/python-programming/global-local-nonlocal-variables -walk-depth 1
```

Если Вы хотите запустить `web-crawler` на другом сайте, выполните в терминале следующие команды:
```commandline
git clone git@github.com:alexandraizhevskaya/project_simple_webrawler.git
cd test
pip install -r requirements.txt
python main.py -url  your_url_link -walk-depth 2
```
*Параметры*:
* `-url`: str - Ссылка на сайт, который Вы хотите обработать. Обязательный параметр
* `-walk-depth`: int - Глубина обхода - сколько уровней связанных ссылок Вы хотите обработать. Обязательный параметр


### Структура репозитория
* `crawler.py` - файл с функцией n `run_crawling`, где реализован рекурсивный обход ссылок
* `main.py` - скрипт, запускающий функцию `run_crawling` из консоли
* `requirements.txt` - requirements для настройки окружения
* `data` - пример директории с htmls-файлами обработанных страниц 
* `urls.txt` - пример файла со списком обработанных url-ссылок и их id