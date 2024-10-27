import asyncio
import os

# import project files
import functions as fcs

# Aiogram files
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor

data = {
    "AWAIT_DATA": False
}

# Указываем папку для сохранения файлов
SAVE_DIR = './saved_files'
os.makedirs(SAVE_DIR, exist_ok=True)

TOKEN = '8037037876:AAFhwpS3tDBRKxtpsyfwtdISemYxTzkY_7Y'
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=["start"])
async def process_start(msg: types.Message):
    """On start"""
    await bot.send_message(msg.from_id, 'Привет! Я могу предсказать финансовые показатели на следующий месяц.'
                           '\n\nПришли файл .excel')
    data['AWAIT_DATA'] = True


@dp.message_handler(content_types=types.ContentTypes.DOCUMENT)
async def handle_document(msg: types.Message):
    """On csv"""
    if (data['AWAIT_DATA']):
        document = msg.document
        # Проверка, является ли файл CSV
        file_info = await bot.get_file(document.file_id)
        file_path = file_info.file_path
        
        # Скачиваем файл
        path_id = "{}".format(msg.from_id)
        await bot.download_file(file_path, os.path.join(SAVE_DIR, path_id, document.file_name))

        await msg.reply("Файл успешно сохранен.")
        data['AWAIT_DATA'] = False

        df = fcs.make_dataset('dfr.xlsx')
        # df_reserve = df.copy()

        # Создаем список новых имен столбцов
        # new_column_names = list(map(chr, range(ord('A'), ord('A') + len(df.columns))))

        # Переименовываем столбцы DataFrame
        # df.columns = new_column_names
        # Убираем месяцы и номера
        df = df.drop(['Месяц', 'Номер'], axis=1)

        columns = df.columns #список колонок
        txt = "Ожиданемые показатели в следующем месяце:\n\n"
        for i in range(len(columns)):
            txt += f"{df.columns[i]}: {int(fcs.new_value(df, columns[i], 1))}\n"
            print(columns[i], fcs.new_value(df, columns[i], 1) )
            
        await bot.send_message(msg.from_id, txt)


# Основная асинхронная функция
async def main():   
    print('HERE MAIN')
    # Бот в фоновом режиме
    await dp.start_polling()

# Запускаем программу, выполняя обе задачи параллельно
asyncio.run(main())
