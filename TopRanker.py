class TopRanker:
    def __init__(self, n):
        self.data = [(None, None, None, None, None, 0.0)] * (n + 1)

    def update_if_greater(self, score, is_greeater):
        pointer = len(self.data) - 1
        self.data[pointer] = score
        if pointer > 0 and is_greeater(self.data[pointer], self.data[pointer - 1]):
            upcast_score(self.data, pointer, is_greeater)

    def get_data(self):
        self.data.pop()
        return self.data


def is_greater(item1, item2):
    return item1[5] > item2[5]


def upcast_score(list, index, is_greater):
    while index > 0 and is_greater(list[index], list[index - 1]):
        list[index], list[index - 1] = list[index - 1], list[index]
        index -= 1

# def is_greater(item1, item2):
#     return item1[5] > item2[5]
#
#
# data_structure = TopRanker(5)
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
# print(len(data_structure.get_data()))
