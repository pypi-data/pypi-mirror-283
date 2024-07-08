import numpy


def play(
    env: numpy.ndarray,
    state_init_func: callable,
    arm_sel_func: callable,
    state_upd_func: callable,
):
    """Play a bandit game.

    A bandit game is a game where the player is presented with a set of arms,
    each with an unknown reward.
    The player's goal is to maximize the total reward
    by selecting the arms to play.
    At each round, the player selects **an** arm to play,
    receives a reward, and updates the states of the game.

    Parameters
    ----------
    env : numpy.ndarray
        the environment of the bandit game.
        It should be a numpy array of shape (..., num_rounds, num_arms)
        where the last dimension represents the rewards of each arm.
    state_init_func : callable
        a function that initializes the states of the bandit game.
        It should have the signature
        `state_init_func(
        p_dims: Tuple[int], num_arms: int
        ) -> List[numpy.ndarray]`.
    arm_sel_func : callable
        a function that selects the arms to play.
        It should have the signature
        `arm_sel_func(t: int, *states: numpy.ndarray) -> numpy.ndarray`.
    state_upd_func : callable
        a function that updates the states of the bandit game.
        It should have the signature
        `state_upd_func(
        sel_arms: numpy.ndarray,
        recv_rewards: numpy.ndarray,
        *states: numpy.ndarray
        ) -> List[numpy.ndarray]`.

    Returns
    -------
    numpy.ndarray
        a numpy array of shape (..., num_rounds)
        where the selected arms are stored.
    """
    # dimensions of env and states should match
    *p_dims, num_rounds, num_arms = env.shape
    p_dims_tuple = tuple(p_dims)
    states = state_init_func(p_dims_tuple, num_arms)
    if states is not None:
        for i, state in enumerate(states):
            assert p_dims_tuple == state.shape[:len(p_dims)], \
                f"env and state_{i}'s shape mismatch: \
                    {p_dims_tuple} != {state.shape[:len(p_dims)]}"
    else:
        assert False, f"{state_init_func.__name__} returned None"

    decisions = numpy.zeros(env.shape[:-1], dtype=int)
    # play the game
    for t in range(num_rounds):
        sel_arms = arm_sel_func(t, *states)
        env_snapshot = env[..., t, :]
        sel_arms_embedding = numpy.eye(num_arms)[sel_arms]
        recv_rewards = numpy.sum(env_snapshot * sel_arms_embedding, axis=-1)
        states = state_upd_func(sel_arms, recv_rewards, *states)

        decisions[..., t] = sel_arms
    return decisions
