from czo import NetLib


def test_generate_ip_list_v4():
    l1 = ['1.0.0.1', '1.0.0.2', '1.0.0.3']
    l2 = ['188.188.1.1', '188.188.1.2', '188.188.1.3']
    v4 = {
        "a": 188,
        "b": 188,
        "c": 1,
        "d": 1,
    }
    assert NetLib.generate_ip_list(3) == l1
    assert NetLib.generate_ip_list(3, **v4) == l2


def test_generate_ip_list_v6():
    l1 = ['2001:db8:0:42:0:8a2e:370:1',
          '2001:db8:0:42:0:8a2e:370:2', '2001:db8:0:42:0:8a2e:370:3']
    l2 = ['240e:c0a8:1:1:1:1:1:1',
          '240e:c0a8:1:1:1:1:1:2', '240e:c0a8:1:1:1:1:1:3']
    v6 = {
        "a": "240e",
        "b": "c0a8",
        "c": "1",
        "d": "1",
        "e": "1",
        "f": "1",
        "g": "1",
        "h": "1",
    }
    assert NetLib.generate_ip_list(3, True) == l1
    assert NetLib.generate_ip_list(3, True, **v6) == l2
