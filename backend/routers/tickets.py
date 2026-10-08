import os
import uuid

import qrcode
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from database import get_db
from models import Booking, Ticket
from schemas import TicketResponse
from security import bearer_scheme, get_current_user


router = APIRouter(
    prefix="/api/v1/tickets",
    tags=["Tickets"]
)


# =========================
# GENERATE TICKET
# =========================

@router.post(
    "/booking/{booking_id}",
    response_model=TicketResponse,
    status_code=status.HTTP_201_CREATED
)
def generate_ticket(
    booking_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(
        bearer_scheme
    ),
    db: Session = Depends(get_db)
):
    current_user = get_current_user(
        credentials=credentials,
        db=db
    )

    booking = (
        db.query(Booking)
        .filter(Booking.id == booking_id)
        .first()
    )

    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )

    if booking.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to generate a ticket for this booking"
        )

    if booking.booking_status != "CONFIRMED":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ticket can only be generated for a confirmed booking"
        )

    existing_ticket = (
        db.query(Ticket)
        .filter(Ticket.booking_id == booking.id)
        .first()
    )

    if existing_ticket:
        return existing_ticket

    ticket_code = f"SME-{uuid.uuid4().hex[:12].upper()}"

    os.makedirs(
        "static/qrcodes",
        exist_ok=True
    )

    qr_file_name = f"{ticket_code}.png"

    qr_file_path = os.path.join(
        "static",
        "qrcodes",
        qr_file_name
    )

    qr_data = (
        f"SmartEvent Ticket\n"
        f"Ticket Code: {ticket_code}\n"
        f"Booking ID: {booking.id}\n"
        f"Event ID: {booking.event_id}"
    )

    qr_image = qrcode.make(qr_data)
    qr_image.save(qr_file_path)

    qr_code_url = f"/static/qrcodes/{qr_file_name}"

    new_ticket = Ticket(
        booking_id=booking.id,
        ticket_code=ticket_code,
        qr_code_url=qr_code_url
    )

    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)

    return new_ticket


# =========================
# GET MY TICKETS
# =========================

@router.get(
    "/my-tickets",
    response_model=list[TicketResponse]
)
def get_my_tickets(
    credentials: HTTPAuthorizationCredentials = Depends(
        bearer_scheme
    ),
    db: Session = Depends(get_db)
):
    current_user = get_current_user(
        credentials=credentials,
        db=db
    )

    bookings = (
        db.query(Booking)
        .filter(Booking.user_id == current_user.id)
        .all()
    )

    booking_ids = [
        booking.id
        for booking in bookings
    ]

    if not booking_ids:
        return []

    tickets = (
        db.query(Ticket)
        .filter(Ticket.booking_id.in_(booking_ids))
        .all()
    )

    return tickets


# =========================
# VERIFY TICKET
# =========================

@router.get(
    "/verify/{ticket_code}",
    response_model=TicketResponse
)
def verify_ticket(
    ticket_code: str,
    credentials: HTTPAuthorizationCredentials = Depends(
        bearer_scheme
    ),
    db: Session = Depends(get_db)
):
    get_current_user(
        credentials=credentials,
        db=db
    )

    ticket = (
        db.query(Ticket)
        .filter(Ticket.ticket_code == ticket_code)
        .first()
    )

    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )

    return ticket