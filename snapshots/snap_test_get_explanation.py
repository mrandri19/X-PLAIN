# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import GenericRepr, Snapshot


snapshots = Snapshot()

snapshots['TestGet_explanation::test_get_explanation_adult_naive_bayes 1'] = (
    GenericRepr('<XPLAIN_class.XPLAIN_explainer object at 0x100000000>'),
    [
        0.001845467396144107,
        0.0002994653864815122,
        0.00758969726159231,
        -5.443648409986235e-05,
        0.00395520353182488,
        0.009698075718879262,
        0.0037103410413463767,
        0.006290885597238671,
        0.0004060948020704336,
        0.0004158197181411971,
        -0.0002190625029386828
    ],
    {
        '1,2,3,6,7,8,9,10': 0.451855563622254,
        '1,6': 0.028801042586218406,
        '2,6,10': 0.021247318095803158,
        '3,6,8,9': 0.1654287896037253,
        '3,7': 0.03915199082039855,
        '6,7,8': 0.10757589553664326
    },
    590,
    0.047132997371904906,
    GenericRepr('[Female, Private, Dropout, White, Separated, ... | <=50K]'),
    '<=50K',
    0,
    0.9989885609941589,
)

snapshots['TestGet_explanation::test_get_explanation_zoo_naive_bayes 1'] = (
    GenericRepr('<XPLAIN_class.XPLAIN_explainer object at 0x100000000>'),
    [
        0.01990259243098258,
        -0.0044584473263546975,
        0.03578864797166614,
        0.0711486717690345,
        -0.0053684378527004695,
        -0.003439901428786807,
        -0.005275113194226355,
        -0.0005951191376797338,
        -0.004663949420987135,
        -0.0031316900588670427,
        -0.0051832869916074165,
        -0.005612873950141317,
        -0.003998033550705715,
        -0.005187953323797401,
        -0.005709590940070952,
        -0.002513951572180484
    ],
    {
        '1,2,3,4,8,9,10,11': 0.5929952768272351
    },
    33,
    0.0013287519043954088,
    GenericRepr('[1, 0, 0, 1, 0, ... | mammal] {deer}'),
    'mammal',
    5,
    0.9990739323302471,
)

snapshots['TestGet_explanation::test_get_explanation_zoo_random_forest 1'] = (
    GenericRepr('<XPLAIN_class.XPLAIN_explainer object at 0x100000000>'),
    [
        0.11604938271604937,
        0.020987654320987703,
        0.17407407407407405,
        0.2962962962962963,
        0.0,
        0.0,
        0.0,
        0.07901234567901239,
        0.01728395061728394,
        0.059259259259259234,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0
    ],
    {
        '1,2,3,4,8,9,10,11': 0.5901234567901235
    },
    33,
    0.0024691358024691024,
    GenericRepr('[1, 0, 0, 1, 0, ... | mammal] {deer}'),
    'mammal',
    5,
    1.0,
)
