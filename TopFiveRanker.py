class TopFiveRanker:
    def __init__(self):
        self.data = [(None, None, None, None, None, 0.0)] * 6

    def update_if_greater(self, score, is_greeater):
        pointer = 5
        self.data[pointer] = score
        if pointer > 0 and is_greeater(self.data[pointer], self.data[pointer - 1]):
            upcast_score(self.data, pointer, is_greeater)

    def get_data(self):
        return self.data


def is_greater(item1, item2):
    return item1[5] > item2[5]


def upcast_score(list, index, is_greater):
    while index > 0 and is_greater(list[index], list[index - 1]):
        list[index], list[index - 1] = list[index - 1], list[index]
        index -= 1


# data_structure = TopFiveRanker()
# data = [(None, None, None, None, None, 0.1),
#         (None, None, None, None, None, 0.2),
#         (None, None, None, None, None, 0.5),
#         (None, None, None, None, None, 0.1),
#         (None, None, None, None, None, 0.2),
#         (None, None, None, None, None, 0.6),
#         (None, None, None, None, None, 0.22),
#         (None, None, None, None, None, 0.72),
#         ]
#
# for i in data:
#     data_structure.update_if_greater(i, is_greater)
#
# print(data_structure.get_data())
