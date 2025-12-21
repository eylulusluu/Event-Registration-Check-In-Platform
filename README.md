# Event Registration & Check-In Platform

A Python terminal application for managing event registrations and participant check-ins.

## Features
- Add new participants  
- Check-in attendees  
- View registered users  
- Simple terminal interface  

## Setup
1. Clone this repository:
   ```bash
   git clone https://github.com/eylulusluu/Event-Registration-Check-In-Platform.git
## Usage

### 1. Organizer Menu
- Create new events
- Add sessions/workshops
- Update or cancel events
- View event reports (attendance, revenue)

### 2. Staff Menu
- Register attendees
- Assign tickets and seats
- Check attendee status
- Promote waitlist

### 3. Attendee Menu
- View your registrations
- Check ticket status
- Cancel or transfer registration

### Example Flow
1. Organizer creates an event "Python Conference 2025" with 100 seats.
2. Attendee registers for the event.
3. Registration reaches capacity → waitlist is activated automatically.
4. On event day, staff checks in attendees via confirmation code.
5. System generates badges and logs check-in times.
6. Organizer generates attendance and revenue reports.

### Data Files
- `data/events.json` – Stores all event and session information.
- `data/attendees.json` – Stores all attendee profiles.
- `data/registrations.json` – Stores all registrations and ticket assignments.

## Testing
Automated tests are provided to validate:
- Capacity enforcement
- Waitlist promotion
- Check-in workflow

Run tests with:
pytest tests/

Tests are run using:
py -m pytest tests/


