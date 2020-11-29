import atexit
import sys

from utils import *
from query_yes_no import query_yes_no


listener = query_yes_no('Do you want to have a listener? [yes/no]')
driver = get_driver()
print('Driver up and running.')

if listener == True:
    open_bustabit(driver, "https://www.bustabit.com/play")
    print('Crawler on bustabit.com')

    while True:
        get_multiplier_value(driver)
else:
    starting_game_number = input("Enter the first game number: ")
    finishing_game_number = input("Enter the last game number: ")

    get_previous_games_data(
                            driver,
                            int(starting_game_number),
                            int(finishing_game_number)
                            )


    print("job done")
    sys.exit()

atexit.register(exit_handler(driver))
