from checkin import check_in_attendee

def test_check_in():
    registrations = [
        {
            "id": "R1",
            "status": "confirmed",
            "checked_in": False
        }
    ]

    result = check_in_attendee(registrations, "R1")
    assert result["checked_in"] is True

