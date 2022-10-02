## Простой Web crawler

### Описание проекта
Проект содержит реализацию `web crawler`, который скачивает содержимое заданной страницы, сохраняет его в директорию, 
а затем извлекакает все дочерние ссылки, указанные на странице, и рекурсивно обходит их до заданной глубины, обрабатывая таким же образом. 
Содержимое всех обработанных ссылок сохраняется в папку `data`. Каждой ссылке присваивается уникальный целочисленный id, который и служит названием html-файла. 

Пример названия файла: 
`3.html`

Кроме того, список всех обработанных ссылок сохраняется в файле `urls.txt`. Каждая строча содержит id и ссылку, разделенные пробелом.

Пример строки файла: 
`7 https://www.programiz.com/python-programming/datetime/strftime`

------------
### Использование
Сейчас в репозитории в качестве примера находятся директория`data` и файл `urls.txt`. Они были получены с помощью следующей команды:

```commandline
python main.py -url https://www.programiz.com/python-programming/global-local-nonlocal-variables -walk-depth 1
```

Если Вы хотите запустить `web-crawler` на другом сайте, выполните в терминале следующие команды:
```commandline
git clone git@github.com:alexandraizhevskaya/project_simple_webrawler.git
cd project_simple_webrawler
pip install -r requirements.txt
python main.py -url  your_url_link -walk-depth 1
```
*Параметры*:
* `-url`: str - Ссылка на сайт, который Вы хотите обработать. Обязательный параметр
* `-walk-depth`: int - Глубина обхода - сколько уровней связанных ссылок Вы хотите обработать. Обязательный параметр

-----------------
### Структура репозитория
* `crawler_class.py` - файл с классом `SimpleCrawler`, в методе которого `crawl` реализован рекурсивный обход ссылок
* `main.py` - скрипт, запускающий функцию `run_crawling` из консоли
* `requirements.txt` - requirements для настройки окружения
* `data` - пример директории с htmls-файлами обработанных страниц 
* `urls.txt` - пример файла со списком обработанных url-ссылок и их id

------------
### Ограничения 
Основой `web crawler` являются библиотечки `requests` и `beautifoulsoup`. К сожалению, он не умеет обрабатывать блокировки:(

При возникновении подобных проблем появляется сообщение об ошибке: 

`Probably, the site is blocking crawler:(`

Также, если при отправке запроса пришел ответ, но его код не 200, появляется предупреждение, что ссылка была обработана, но статус не корректный:

`Request status code for id 12 is not 200. Please, search the meaning of the following request status: 403`

#### *Важно*  
В текущей реализации если при запускке crawler у Вас уже есть папка `data` и файл  `urls.txt` - они будут удалены и перезаписаны: в них кладется результат обхода запрошенной страницы.

----------------
### Особенности реализации

`Crawler` тестировался преимущественно на следующих сайтах:
* https://habr.com/ru/all/
* https://www.programiz.com/python-programming/global-local-nonlocal-variables

Обход реализован с помощью рекурсии. Уникальность посещенных страниц поддерживается благодаря множеству,
в которое каждая новая ссылка кладется перед обработкой. Соответственно, после такой проверки запускается обработка ссылки и она добавляется в список посещенных.
Класс может использоватс сам по себе. Поэтому в его метод добавлены параметры `data_dir` и `file_name`, чтобы можно было выбрать, куда записывать результат.
Кроме того, чтобы можно было запускать один инстанс класса для обхода нескольких файлов, у него есть метод `reboot`, который очищает множество посещенных вершин и устанавливает значение индекса 1.

При рекурсивном обходе обрабатываются только "дочерние" ссылки - мы не идем обходить весь интернет.
Глубина 0 означает, что мы обрабатываем только исходную ссылку и никуда дальше не идем.

При ошибках и блокировках выводится предупреждение, что возникла ошибка и не удалось обработать ссылку, но сам рекурсивный обход продолжается.
Сохраняются соответственно те страницы, которые удалось обработать.

Для простоты реализована перезапись файла и директории с результатом, если  они уже есть. Вообще хорошая идея их тоже передавать как необязательные параметры скрипта, чтобы можно было выбрать, куда писать результат.