from context import *

from refspy.languages.english import ENGLISH
from refspy.libraries.en_US import OT, NT
from refspy.manager import Manager
from refspy.range import range
from refspy.reference import reference
from refspy.verse import verse

text = """
Romans 1:1–4 
Romans 1:4–1 
Romans 1:776-777 and 2:3-4
Romans 1:1-2,5-6 and v.9
Rom 1:1-4,9
Rom 1:1-2:4
Rom 1:1a-2:4b
Philemon 3-6 and v.15
1 Cor
1:1-4
2 Cor is the book now
2:1-4
v.4
vv.5-6
"""

__ = Manager(libraries=[OT, NT], language=ENGLISH)


def test_example():
    result = __.find_references(text, include_nones=True)
    assert result[0] == (
        "Romans 1:1–4",
        reference(range(verse(400, 6, 1, 1), verse(400, 6, 1, 4))),
    )
    assert result[1] == ("Romans 1:4–1", None)
    assert result[2] == (
        "Romans 1:776-777",
        reference(range(verse(400, 6, 1, 776), verse(400, 6, 1, 777))),
    )
    assert result[3] == (
        "2:3-4",
        reference(range(verse(400, 6, 2, 3), verse(400, 6, 2, 4))),
    )
    assert result[4] == (
        "Romans 1:1-2,5-6",
        reference(
            range(verse(400, 6, 1, 1), verse(400, 6, 1, 2)),
            range(verse(400, 6, 1, 5), verse(400, 6, 1, 6)),
        ),
    )
    assert result[5] == (
        "v.9",
        reference(
            range(verse(400, 6, 1, 9), verse(400, 6, 1, 9)),
        ),
    )
    assert result[6] == (
        "Rom 1:1-4,9",
        reference(
            range(verse(400, 6, 1, 1), verse(400, 6, 1, 4)),
            range(verse(400, 6, 1, 9), verse(400, 6, 1, 9)),
        ),
    )
    assert result[7] == (
        "Rom 1:1-2:4",
        reference(range(verse(400, 6, 1, 1), verse(400, 6, 2, 4))),
    )
    assert result[8] == (
        "Rom 1:1a-2:4b",
        reference(range(verse(400, 6, 1, 1), verse(400, 6, 2, 4))),
    )
    assert result[9] == (
        "Philemon 3-6",
        reference(range(verse(400, 18, 1, 3), verse(400, 18, 1, 6))),
    )
    assert result[10] == (
        "v.15",
        reference(range(verse(400, 18, 1, 15), verse(400, 18, 1, 15))),
    )
    assert result[11] == (
        "1 Cor\n1:1-4",
        reference(range(verse(400, 7, 1, 1), verse(400, 7, 1, 4))),
    )
    assert result[12] == (
        "2:1-4",
        reference(range(verse(400, 8, 2, 1), verse(400, 8, 2, 4))),
    )
    assert result[13] == (
        "v.4",
        reference(range(verse(400, 8, 2, 4), verse(400, 8, 2, 4))),
    )
    assert result[14] == (
        "vv.5-6",
        reference(range(verse(400, 8, 2, 5), verse(400, 8, 2, 6))),
    )
