from registration import promote_waitlist

def test_waitlist_promotion():
    registrations = [
        {"id": "R1", "event_id": "E1", "status": "confirmed"},
        {"id": "R2", "event_id": "E1", "status": "waitlist"}
    ]

    promoted = promote_waitlist(registrations, "E1")

    assert promoted["status"] == "confirmed"
