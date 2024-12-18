import random
from idlelib.colorizer import color_config
import matplotlib.pyplot as plt

import numpy as np
from matplotlib import animation
from matplotlib.lines import Line2D

# 0= our, 1= book
decision_matrix= [[
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, -1],
    [1, 0, 0, 0, 0, 1, 1, 2, 2, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 2, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 1, 1],
    [1, 3, 3, 3, 3, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
],[
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, -1],
    [0, 0, 0, 0, 0, 1, 1, 2, 2, 2],
    [0, 0, 0, 0, 0, 1, 1, 1, 2, 2],
    [0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
    [1, 1, 0, 0, 0, 1, 1, 1, 1, 1],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 1, 1],
    [1, 3, 3, 3, 3, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

]

decision_matrix_soft=[
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, -3, 0, 0, 0, 0, 0],
    [-3, -3, -3, -3, -3, 0, 0, 1, 1, 1],
    [1, 3, 3, 3, 3, 1, 1, 1, 1, 1],
    [1, 1, 3, 3, 3, 1, 1, 1, 1, 1],
    [1, 1, 3, 3, 3, 1, 1, 1, 1, 1],
    [1, 1, 1, 3, 3, 1, 1, 1, 1, 1],
    [1, 1, 1, 3, 3, 1, 1, 1, 1, 1],

]
'''
-3=DS
-1=RS
0 =S
1 =H
2 =RH
3 =DH
'''


def gen_card():
    c = random.randint(1, 13)
    if c == 1: return 11
    if c > 11: return 10
    return c


def dealer(first_cards):
    tot = first_cards[0] + first_cards[1]
    card_sequence = first_cards
    if tot > 21 and 11 in card_sequence:
        card_sequence[card_sequence.index(11)] = 1
        tot -= 10
    while tot < 17:
        c = gen_card()
        card_sequence.append(c)
        tot += c
        if tot > 21 and 11 in card_sequence:
            card_sequence[card_sequence.index(11)] = 1
            tot -= 10
    return tot, card_sequence


def evaluate_winner(player, p_c, house, h_c):
    return ((p_c[0] + p_c[1]) == 21 and (h_c[0] + h_c[1]) != 21) or (player > house and player <= 21) or (
                player <= 21 and house > 21)


def decision_index(tot):
    if tot >18: return 0
    if tot <9: return 10
    return 18-tot

def decision_index_soft(tot):
    if tot >20: return 0
    if tot <13: return 7
    return 20-tot


def player_soft(player_cards, dealer_first):
    tot =sum(player_cards)
    if tot > 21 and 11 in player_cards:
        player_cards[player_cards.index(11)] = 1
        return player(player_cards, dealer_first)
    while (decision_matrix_soft[decision_index_soft(tot)][dealer_first-2]>0)and tot<=21:
        player_cards.append(gen_card())
        tot=sum(player_cards)
        if tot > 21 and 11 in player_cards:
            player_cards[player_cards.index(11)] = 1
            return player(player_cards, dealer_first)
    return sum(player_cards)


def player(player_cards, dealer_first):
    tot =sum(player_cards)
    if 11 in player_cards and SOFT_TRIGGER:
        return player_soft(player_cards, dealer_first)
    if tot > 21 and 11 in player_cards:
        player_cards[player_cards.index(11)] = 1
        tot -= 10
    while (decision_matrix[Matrix][decision_index(tot)][dealer_first-2]>0)and tot<=21:
        player_cards.append(gen_card())
        tot=sum(player_cards)
        if 11 in player_cards and SOFT_TRIGGER:
            return player_soft(player_cards, dealer_first)
        if tot > 21 and 11 in player_cards:
            player_cards[player_cards.index(11)] = 1
            tot -= 10
    return sum(player_cards)


def mach(index):
    # game start
    dealer_first = gen_card()
    dealer_second = gen_card()
    player_cards = [gen_card(), gen_card()]

    #player decision
    tot_player = player(player_cards, dealer_first)
    #game end
    d = dealer([dealer_first, dealer_second])
    winner = evaluate_winner(tot_player, player_cards, d[0], d[1])
    if(DEBUG):print(("win \t" if winner else "lose\t") + "player{" + str(tot_player) + "}: " + str(
        player_cards) + "\t dealer{" + str(d[0]) + "}: " + str(d[1]))
    return 1 if winner else (0 if tot_player==d[0] else -1)


# TEST


import matplotlib.pyplot as plt

N_GAMES=1000        # number of games simulated per test
SOFT_TRIGGER=True   # allow the use of the soft hand decision table for the player
N_TEST=8          # number of test
DEBUG=False          # print each mach result
Matrix=0  #0=ours,  1 = bock

an=[]
buf=[]

fig, ax = plt.subplots()
last=[]
for index in range(N_TEST):
    balance = 0
    balance_history = [0]
    for i in range(N_GAMES):
        balance += mach(i)
        balance_history.append(balance)
    if(DEBUG):print(str(i+1)+") "+str(balance))
    last.append(balance)
    an=balance_history
    buf.append(balance_history)
    #PLOT
    ax.plot(balance_history,color="C"+str(index),linestyle="--")
print(np.mean(last))
textstr="mean balance after 1000 games: "+str(np.mean(last))
line=Line2D([0,N_GAMES],[0,np.mean(last)],color="C0",linestyle="-")
ax.add_line(line)
fig.show()


print(an)
xx=np.arange(len(an))
'''
fig, ax = plt.subplots()
line2, = ax.plot(xx[:3], an[:3])
ax.set(xlim=[0, len(xx)], ylim=[min(an),max(an) ], xlabel='iterction', ylabel='earnings')
def update(frame):
    # for each frame, update the data stored on each artist.
    # update the scatter plot:
    # update the line plot:
    line2.set_xdata(xx[:frame*5:5])
    line2.set_ydata(an[:frame*5:5])
    return line2
ani = animation.FuncAnimation(fig=fig, func=update, frames=int(len(xx)/5), interval=1)
ani.save('animation_drawing.gif', writer='Pillow', fps=600)
#ani.to_jshtml()
'''
lines=[]
fig, ax = plt.subplots()
for i in range(N_TEST):
    lines.append(ax.plot(0,0,color="C"+str(i),linestyle=":")[0])
ax.set(xlim=[0, len(xx)], ylim=[min([min(b) for b in buf]),max([max(b) for b in buf]) ], xlabel='games', ylabel='balance')
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
ax.text(0.01, 0.01, textstr, transform=ax.transAxes, fontsize=9.5,
        verticalalignment='bottom', bbox=props)
def update(frame):
    # for each frame, update the data stored on each artist.
    # update the scatter plot:
    # update the line plot:
    for i in range(N_TEST):
        lines[i].set_xdata(xx[:frame*5:5])
        lines[i].set_ydata(buf[i][:frame*5:5])
    return lines
ani = animation.FuncAnimation(fig=fig, func=update, frames=int(len(xx)/5), interval=1)
ani.save('animation_drawing_our.gif', writer='Pillow', fps=600)