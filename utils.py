import matplotlib.pyplot as plt
import numpy as np


def int_input(message):
    while True:
        try:
            output = int(input(message))
        except ValueError:
            print('Det skal være et heltal, prøv igen.\n')
            continue
        return output


def ask_Y_n(message):
    while True:
        answer = input(message)
        if answer in ['Y', 'y']:
            return True
        elif answer in ['n', 'N']:
            return False


def in_range(dar):
    if len(dar) > 2 or len(dar) == 0:
        return False

    for digit in dar:
        if digit not in [str(i) for i in range(10)]:
            return False
    if int(dar) in [i + 1 for i in range(20)]:
        return True
    return False


def is_double(dar):
    if (dar[0] in ['D', 'd']) and in_range(dar[1:]):
        return True
    elif dar in ['BE', 'be', 'Be', 'bE']:
        return True
    return False

# https://medium.com/@symon.kopec/smart-way-to-create-dartboard-heat-map-plot-in-python-using-matplotlib-c6c1fb2b3cb1


def dartboard_heatmap(shots, title='Heatmap'):
    shots = np.array(shots)
    fig, axi = plt.subplots(subplot_kw={'projection': 'polar'})
    fig.set_size_inches((10, 10))

    # the 5,20,1 etc. field grids
    plt.thetagrids(list(range(9, 369, 18)),
                   [20, 5, 12, 9, 14, 11, 8, 16, 7, 19, 3, 17, 2, 15, 10, 6, 13, 4, 18, 1], verticalalignment='center', horizontalalignment='center')
    # the proportions radius of inners and outer circle
    rad = np.linspace(0, 10.5, 21)
    rem = (2 * np.pi)/21
    azm = np.linspace(0-rem/2, 2 * np.pi-rem/2, 21)

    axi.set_rgrids(list(range(0, 360, 18)),
                   [20, 5, 12, 9, 14, 11, 8, 16, 7, 19, 3, 17, 2, 15, 10, 6, 13, 4, 18, 1])

    # radius, r fields outer and inner bullseye
    axi.set_rticks([0.3, 0.8, 5.5, 6, 10.0])
    axi.set_theta_zero_location("N", offset=0.0)
    axi.set_yticklabels([])

    radius, theta = np.meshgrid(rad, azm)
    z_values = []
    for point in [20, 5, 12, 9, 14, 11, 8, 16, 7, 19, 3, 17, 2, 15, 10, 6, 13, 4, 18, 1]:
        bm = ('BE' == shots).sum() + ('be' == shots).sum() + \
            ('Be' == shots).sum() + ('bE' == shots).sum()
        bo = ('25' == shots).sum()
        qp = (f'{point}' == shots).sum()
        dp = (f'D{point}' == shots).sum() + (f'd{point}' == shots).sum()
        tp = (f'T{point}' == shots).sum() + (f't{point}' == shots).sum()
        z_field = [bm, bo, qp, qp, qp, qp, qp, qp, qp,
                   qp, qp, tp, qp, qp, qp, qp, qp, qp, qp, dp]
        z_values.append(z_field)

    plt.pcolormesh(theta, radius, z_values, cmap='Blues')
    plt.colorbar(label="throws", orientation="vertical",
                 fraction=0.046, pad=0.2)
    axi.grid(True)
    axi.set_title(title, va='bottom')
    plt.show()
