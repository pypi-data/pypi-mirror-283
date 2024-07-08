import numpy
import xbandits.algo.ucb as ucb
import xbandits.core.rollout as rollout
from xbandits.core.regret import realized_rewards


def test_score_nd():
    mean_rewards = numpy.array(
        [
            [0.1, 0.2, 0.3],
            [0.4, 0.5, 0.6]
        ]
    )
    trial_counts = numpy.array(
        [
            [0, 10, 2],
            [3, 4, 5]
        ]
    )
    t = 12
    scores = ucb.score(t, mean_rewards, trial_counts)
    assert numpy.allclose(
        scores,
        [
            [
                numpy.inf, 0.2 + numpy.sqrt(2 * numpy.log(t) / 10),
                0.3 + numpy.sqrt(2 * numpy.log(t) / 2)
            ],
            [
                0.4 + numpy.sqrt(2 * numpy.log(t) / 3),
                0.5 + numpy.sqrt(2 * numpy.log(t) / 4),
                0.6 + numpy.sqrt(2 * numpy.log(t) / 5)
            ]
        ]
    )


def test_select_arm_nd():
    mean_rewards = numpy.array(
        [
            [0.1, 0.2, 0.3],
            [0.4, 0.5, 0.6]
        ]
    )
    trial_counts = numpy.array(
        [
            [0, 10, 2],
            [3, 4, 5]
        ]
    )
    t = 12
    selected_arm = ucb.select_arm(t, mean_rewards, trial_counts)
    assert numpy.allclose(selected_arm, [0, 0])


def test_play_nd():
    num_envs, rounds, arms = 50, 100000, 10
    rng = numpy.random.default_rng(0)
    env = numpy.stack(
        [
            rng.binomial(
                1, p=numpy.linspace(0.1, 0.9, arms), size=(rounds, arms)
            )
            for _ in range(num_envs)
        ], axis=0
    )
    decisions = rollout.play(
        env,
        ucb.initialize, ucb.select_arm, ucb.update
    )
    one_hot_decisions = numpy.eye(arms)[decisions]
    freq = numpy.mean(one_hot_decisions, axis=-2)
    assert numpy.argmax(freq, axis=-1).tolist() == \
        [arms - 1 for _ in range(num_envs)]

    ucb_rewards = numpy.sum(realized_rewards(env, decisions), axis=-1)
    random_rewards = numpy.sum(numpy.mean(env, axis=-1), axis=-1)
    assert numpy.all(ucb_rewards > random_rewards)
