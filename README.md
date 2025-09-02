# bag2mp4

## Подготовка к работе
- Установить расширение Remote Development в VScode
- Исправить переменные .devcontainer на свои 
- Собрать и открыть контейнер через DevContainer

## Использование
Ваши файлы должны находиться в контейнере, внутри контейнера должно быть активировано .venv
- python3 bag2bag.py --bag [путь до ros bag] --out [путь для сохранения нового bag] 
  - Конвертирует .bag/.mcap в формат metadata.yaml + .db3
  - Печатает топики (Topics), содержащие картинки
- python3 convert_ros.py --bag [путь до ros bag (директория с metadata.yaml и .db3)] --out [выходная директория до видео] --topic [название топика]
  - Создает из картинок видео
  - Удаляет директория с картинками

## Пример использования
1. Конвертировать файл в формат ros2-bag. В bag файле могут находиться пакеты, зависимостей для расшифровки которых может быть не предустановлено в базовом контейнере (Missing msgtype in destination, copying from source), эти топики будут пропущены, однако, как правило, для работы с картинками все пакеты уже есть.
<img width="1490" height="359" alt="image" src="https://github.com/user-attachments/assets/6053a26d-645b-4c87-8ac8-4260acd6ea63" />

2. Извлечь из директории с ros2-bag картинки и конверитровать их в .mp4 (20fps)
<img width="1291" height="73" alt="image" src="https://github.com/user-attachments/assets/a72531e5-b675-4e86-8030-e25470f8bc40" />
<img width="1409" height="493" alt="image" src="https://github.com/user-attachments/assets/e5d19a0c-2f3a-47c8-bfd0-e573eb403000" />
