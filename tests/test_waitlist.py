from registration import promote_waitlist


def test_waitlist_promotion():
    registrations = [
        {
            "id": "R1",
            "event_id": "E1",
            "status": "confirmed",
            "seat": 1
        },
        {
            "id": "R2",
            "event_id": "E1",
            "status": "waitlist",
            "seat": None
        }
    ]

    promoted = promote_waitlist(registrations, "E1")

    assert promoted is not None
    assert promoted["status"] == "confirmed"
    assert promoted["seat"] == 2

