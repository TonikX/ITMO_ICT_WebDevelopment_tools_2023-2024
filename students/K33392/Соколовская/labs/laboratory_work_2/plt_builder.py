import matplotlib.pyplot as plt


def paint(x, y, title):
    plt.plot(x, y)

    plt.title(title)
    plt.xlabel('Количество')
    plt.ylabel('Время')

    plt.show()
