source ./config/.env

uvicorn main:user_management_app --reload --host 0.0.0.0 --port $USER_MANAGEMENT_SERVICE_PORT & uvicorn main:room_reservation_app --reload --host 0.0.0.0 --port $ROOM_RESERVATION_SERVICE_PORT & uvicorn main:event_app --reload --host 0.0.0.0 --port $EVENT_SERVICE_PORT & uvicorn main:admin_app --reload --host 0.0.0.0 --port $ADMIN_SERVICE_PORT