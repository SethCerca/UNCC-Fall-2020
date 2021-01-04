from vi_util import P, getIndexOfState, getPolicyForGrid, printPolicyForGrid
import numpy as np
import math


class State():
    def __init__(self, x, y):
        self.x = x
        self.y = y


# Populates the list with State objects
def fill_states():
    list_states = np.zeros(11).reshape(-1, 1)
    for y in range(1, 4):
        for x in range(1, 5):
            if (not x == 2) or (not y == 2):
                new_state = State(x, y)
                np.append(list_states, new_state, axis=0)

    return list_states


def get_expected_utility(actions, state, S, transition_model, utilities):
    max_value = []
    #print("here 3")

    current_state = getIndexOfState(S, state.x, state.y)

    up = getIndexOfState(S, state.x, state.y + 1)
    right = getIndexOfState(S, state.x + 1, state.y)
    left = getIndexOfState(S, state.x - 1, state.y)
    down = getIndexOfState(S, state.x, state.y - 1)

    if (state.x == 1) or (state.x == 3 and state.y == 2):
        left = getIndexOfState(S, state.x, state.y)
    elif (state.x == 4) or (state.x == 1 and state.y == 2):
        right = getIndexOfState(S, state.x, state.y)
    elif (state.y == 1) or (state.x == 2 and state.y == 3):
        down = getIndexOfState(S, state.x, state.y)
    elif (state.y == 3) or (state.x == 2 and state.y == 1):
        up = getIndexOfState(S, state.x, state.y)

    #print('[' + str(S[up].x) + ', ' + str(S[up].y) + ']')
    #print('[' + str(S[left].x) + ', ' + str(S[left].y) + ']')

    # Calculates the expected utility for the up direction
    max_value.append(.8 * utilities[up] + .1 * utilities[left] + .1 * utilities[right])

    # Calculates the expected utility for the down direction
    max_value.append(.8 * utilities[down] + .1 * utilities[left] + .1 * utilities[right])

    # Calculates the expected utility for the left direction
    max_value.append(.8 * utilities[left] + .1 * utilities[down] + .1 * utilities[up])

    # Calculates the expected utility for the right direction
    max_value.append(.8 * utilities[right] + .1 * utilities[down] + .1 * utilities[up])
    #print(max(max_value))
    #print("here 4")

    utilities[current_state] = max(max_value)

    #print('current state: [' + str(S[current_state].x) + ', ' + str(S[current_state].y) + ']')

    return utilities


def value_iterations(S, A, P, R_states, discount, tr):
    gamma = 1
    delta = 1
    u_prime = np.zeros(11).reshape((-1, 1))
    #print("here 1")

    while delta > 0:
        u = u_prime

        for x in range(len(S)):

            if x == tr[0]:
                u_prime[x] == -1
            elif x == tr[1]:
                u_prime[x] == 1
            max = get_expected_utility(A, S[x], S, P, u)
            #print("max: " + str(max))
            u_prime[x] = R_states + (discount * np.amax(P * max))
            #print("here 2")
            #print("u = " + str(u))
            #print("u_prime = " + str(u_prime))
            #print("delta: " + str(delta))
            if delta > (u_prime[x] - u[x]):
                delta = math.fabs(u_prime[x] - u[x])
        #print("delta: " + str(delta))
    return u


def main():
    actions = ['u', 'r', 'd', 'l']
    states = fill_states()
    reward = np.array([-0.04, -0.25, -0.01, -0.04, -0.25, -0.01])
    discount = np.array([1.0, 1.0, 1.0, 0.5, 0.5, 0.5])
    terminals = [6, 10]
    u = value_iterations(states, actions, P, reward[0], discount[0], terminals)
    """"
    u_prime = np.array([0.5, 0.5, 0.5, 0.5, 0.5, 1.0, 0.5, 0.5, 0.5, 0.5, -1.0])
    u = get_expected_utility(actions, states[0], states, P, u_prime)
    u[0] = reward[0] + discount[0] * np.amax(P * u)
    print("u: " + str(u))
    u = get_expected_utility(actions, states[0], states, P, u)
    print("u: " + str(u))
    """
    print(u)
    print()
    policy = getPolicyForGrid(states, u, actions, P, terminals)
    print(policy)
    print()
    printPolicyForGrid(policy, 4, 3, [2, 2])

if __name__ == "__main__":
    main()
