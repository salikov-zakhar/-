import random


class randomizer:
    def __init__(self, items_num):
        self.current_item = 0
        self.items = [i for i in range(items_num)]
        random.shuffle(self.items)

    def get_number(self):
        if self.current == len(self.items):
            self.current = 0
            self.shuffle()

        item = self.items[self.current]
        self.current += 1
        return item

    def shuffle(self):
        random.shuffle(self.items)

    def reset(self):
        self.current = 0
        self.shuffle()


randomizer = randomizer(7)
get_number = randomizer.get_number
reset = randomizer.reset
