from registration import create_registration

def test_capacity_limit():
    events = [{"id": "E1", "capacity": 1, "price": 100}]
    registrations = []

    r1 = create_registration(registrations, {
        "event_id": "E1",
        "attendee_id": "A1"
    }, events)

    r2 = create_registration(registrations, {
        "event_id": "E1",
        "attendee_id": "A2"
    }, events)

    assert r1["status"] == "confirmed"
    assert r2["status"] == "waitlist"
