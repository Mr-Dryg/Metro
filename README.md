# Метро

Моделирование пропускной способности метро при различном количестве составов с помощью асинхронного программирования.

## Станции

Метрополитен состоит из одной ветки и 5 станций:
- Рокоссовкая
- Соборная
- Кристалл
- Заречная
- Библиотека

## Работа программы

Одновременно в одном составе может находится не более 400 человек, на одной платформе - не более 1000. Каждую секудну на станцию заходит человек, который хочет побраться до одной из 5 станций.<br>
Если на станции оказывется более 1000 человек, программа сообщает о недостатке составов.<br>
Если в течение 10 минут моделирования ни на одной из станций не оказывается болеее 1000 человек, программа сообщает об успехе.
