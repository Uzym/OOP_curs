from aiogram.utils.helper import Helper, HelperMode, ListItem

class BotStates(Helper):
    mode = HelperMode.snake_case

    BOT_WAIT_A_PHOTO = ListItem()
    BOT_WAIT_A_FILTER = ListItem()
    BOT_WAIT_A_PROCESS = ListItem()
    BOT_PROCESS_COMPLETE = ListItem()

if __name__ == '__main__':
    print(BotStates.all())
