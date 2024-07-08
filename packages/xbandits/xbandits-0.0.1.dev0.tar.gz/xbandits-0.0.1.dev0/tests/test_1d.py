import numpy
import xbandits.algo.ucb as ucb
import xbandits.core.rollout as rollout
from xbandits.core.regret import realized_rewards


def test_score_1d():
    mean_rewards = numpy.array([0.1, 0.2, 0.3])
    trial_counts = numpy.array([0, 1, 2])
    t = 3
    scores = ucb.score(t, mean_rewards, trial_counts)
    assert numpy.allclose(
        scores,
        [
            numpy.inf, 0.2 + numpy.sqrt(2 * numpy.log(t) / 1),
            0.3 + numpy.sqrt(2 * numpy.log(t) / 2)
        ]
    )


def test_select_arm_1d():
    mean_rewards = numpy.array([0.1, 0.2, 0.3])
    trial_counts = numpy.array([0, 1, 2])
    t = 3
    selected_arm = ucb.select_arm(t, mean_rewards, trial_counts)
    assert selected_arm == 0


def test_play_1d():
    rounds, arms = 100000, 10
    rng = numpy.random.default_rng(0)
    env = rng.binomial(
        1, p=numpy.linspace(0.1, 0.9, arms), size=(rounds, arms)
    )
    decisions = rollout.play(env, ucb.initialize, ucb.select_arm, ucb.update)
    one_hot_decisions = numpy.eye(arms)[decisions]
    freq = numpy.mean(one_hot_decisions, axis=-2)
    assert numpy.argmax(freq) == arms - 1

    ucb_rewards = numpy.sum(realized_rewards(env, decisions), axis=-1)
    random_rewards = numpy.sum(numpy.mean(env, axis=-1))
    assert ucb_rewards > random_rewards
