# Задание 2. Config

В этом файле хранятся константы с числом процессов, классы и теги для обработки содержания веб-страниц и
URL-адреса для парсинга. 

### Код

    URLS = [
        'https://skillbox.ru/media/code/kak-stat-tsennym-kadrom-6-sovetov-dlya-karernogo-rosta-razrabotchika/',
        'https://skillbox.ru/media/design/kak-stat-dizaynerom-luchshie-professionalnye-kursy-graficheskogo-dizayna/',
        'https://skillbox.ru/media/management/kak-stat-prodaktmenedzherom-i-nuzhno-li-dlya-etogo-obrazovanie/',
        'https://skillbox.ru/media/management/produktovyy-analitik-chem-on-zanimaetsya-skolko-zarabatyvaet-i-kak-im-stat/',
        'https://skillbox.ru/media/code/qainzhener-kto-eto-chem-on-zanimaetsya-i-kak-im-stat/',
        'https://skillbox.ru/media/management/kto-takoy-restorator-skolko-on-zarabatyvaet-i-kak-im-stat/',
        'https://skillbox.ru/media/marketing/kak-stat-eventmenedzherom-gde-uchitsya-i-poluchat-prakticheskie-navyki/',
        'https://skillbox.ru/media/marketing/kak-stat-seospetsialistom-i-chto-osvoit-chtoby-zarabatyvat-bolshe-80-tysyach-rubley/'
        ]
    
    NUM_THREADS = 4
    HTML_CLASS = 'stk-reset stk-theme_26309__style_large_header'
    HTML_TAG = 'h2'
