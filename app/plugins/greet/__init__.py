import logging
from app.commands import Command


class GreetCommand(Command):
    def execute(self):
        logging.info("Hello, this is a calculator with statistical operations!")

        mylist_tuple = (1,2,3,4)
        mylist = [1,2,3,4]

        

        print("Hello, this is a calculator with statistical operations!")