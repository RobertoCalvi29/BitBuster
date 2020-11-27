import atexit

from utils import *

exit_command = input("type exit to end the script")

driver = get_driver()
open_bustabit(driver, "https://www.bustabit.com/play")


stop = False

while stop:
    rows = get_bustabit_history(driver)
    get_table_from_csv()
    get_multiplier_value()

atexit.register(exit_handler(driver))
