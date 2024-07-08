import numpy


def realized_rewards(
    envs: numpy.ndarray,
    selected_arms: numpy.ndarray
):
    """Calculate the realized rewards for the selected arms
    in each environment.

    Parameters
    ----------
    envs : numpy.ndarray
        a numpy array of shape (..., num_arms) where
        contains the rewards for each arm at a given time step
        in each environment.

    selected_arms : numpy.ndarray
       a numpy array of shape (...) where contains the selected arms
       at each time step in each environment.

    Returns
    -------
    inst_rewards : numpy.ndarray
        a numpy array of shape (...) where the realized rewards
        for the selected arms are stored.
    """
    *_, num_arms = envs.shape
    embedding = numpy.eye(num_arms)[selected_arms]
    inst_rewards = numpy.sum(envs * embedding, axis=-1)
    return inst_rewards
