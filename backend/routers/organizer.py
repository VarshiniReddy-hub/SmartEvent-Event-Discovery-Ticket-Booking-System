from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from database import get_db
from models import Event, Booking
from routers.auth import get_current_user


router = APIRouter(
    prefix="/api/v1/organizer",
    tags=["Organizer"]
)


# =========================
# ORGANIZER ANALYTICS
# =========================

@router.get("/analytics")
def get_organizer_analytics(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    # Only ORGANIZER can access this API
    if current_user.role != "ORGANIZER":
        raise HTTPException(
            status_code=403,
            detail="Organizer access required"
        )

    events = (
        db.query(Event)
        .filter(
            Event.organizer_id == current_user.id
        )
        .all()
    )

    result = []

    for event in events:

        booking_count = (
            db.query(func.count(Booking.id))
            .filter(
                Booking.event_id == event.id,
                Booking.booking_status != "CANCELLED"
            )
            .scalar()
        )

        tickets_sold = (
            db.query(
                func.coalesce(
                    func.sum(
                        Booking.ticket_quantity
                    ),
                    0
                )
            )
            .filter(
                Booking.event_id == event.id,
                Booking.booking_status != "CANCELLED"
            )
            .scalar()
        )

        total_revenue = (
            db.query(
                func.coalesce(
                    func.sum(
                        Booking.total_price
                    ),
                    0
                )
            )
            .filter(
                Booking.event_id == event.id,
                Booking.booking_status != "CANCELLED"
            )
            .scalar()
        )

        result.append({
            "event_id": event.id,
            "event_title": event.title,
            "total_tickets": event.total_tickets,
            "tickets_sold": tickets_sold,
            "remaining_tickets": event.available_tickets,
            "booking_count": booking_count,
            "total_revenue": total_revenue
        })

    return result