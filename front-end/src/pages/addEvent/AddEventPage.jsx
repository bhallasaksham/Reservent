import React, { useState, useEffect } from "react";
import { MainLayout } from "../../layouts";
import axios from "axios";
import { Form, Button, Row, Col, Offcanvas, Card } from "react-bootstrap";
import styles from "./AddEventPage.module.css";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import { RoomCard, CustomBadge } from "../../components";
import {
  PlusSquare,
  PencilSquare,
  PersonPlusFill,
  CheckCircleFill,
  ArrowLeftCircleFill,
} from "react-bootstrap-icons";
import { useHistory } from "react-router-dom";
import { getRoundedDate, addMinutes } from "../../tools";

export const AddEventPage = () => {
  const history = useHistory();

  const [title, setTitle] = useState();
  const [description, setDescription] = useState();
  const [startDate, setStartDate] = useState(new Date());
  const [startTime, setStartTime] = useState(getRoundedDate(new Date()));
  const [endTime, setEndTime] = useState(
    addMinutes(getRoundedDate(new Date()), 60)
  );
  const [numOfParticipant, setNumOfParticipant] = useState();
  const [showSidebar, setShowSidebar] = useState(false);
  const [selectedRoom, setSelectedRoom] = useState();
  const [curGuest, setCurGuest] = useState("");
  const [guestList, setGuestList] = useState([]);

  const searchRooms = () => {
    setShowSidebar(true);
    setSelectedRoom(null);
  };

  const chooseRoom = (room) => {
    console.log("select: " + room.id, room.name);
    setSelectedRoom(room);
    setShowSidebar(false);
  };

  const deleteRoom = (room) => {
    console.log("delete: " + room.id, room.name);
    setSelectedRoom(null);
  };

  const fakeRoom = { id: 1, name: "room 118", size: 6 };

  const addGuest = (guest) => {
    if (curGuest != "") {
      // TODO: check guest here
      if (guestList.includes(guest)) {
        alert(`You have already invited ${guest}`);
      } else {
        guestList.push(guest);
        setGuestList(guestList);
      }
      setCurGuest("");
    }
    console.log(guestList);
  };

  const deleteGuest = (guest) => {
    setGuestList(guestList.filter((item) => item !== guest));
    console.log(guestList);
  };

  const handleSubmit = (event) => {
    event.preventDefault(); // the default action that belongs to the event will not occur - whether we need this?

    //reset the values of input fields ?

    alert(
      "title: " +
        title +
        "\ndes: " +
        description +
        "\ndate: " +
        startDate +
        "\nstime: " +
        startTime +
        "\netime: " +
        endTime +
        "\nnum of p: " +
        numOfParticipant +
        "\ninvite guests: " +
        guestList +
        "\nroom: " +
        selectedRoom.name
    );
  };

  return (
    <MainLayout>
      <h1 className="page-title">Add New Event</h1>
      <Form className={styles["add-event-form"]} onSubmit={handleSubmit}>
        <h2>Event Details</h2>
        <Form.Group className="mb-3" controlId="formTitle">
          <Form.Label>Title</Form.Label>
          <Form.Control
            type="text"
            placeholder="Enter title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
          />
        </Form.Group>

        <Form.Group className="mb-3" controlId="formDescription">
          <Form.Label>Description</Form.Label>
          <Form.Control
            type="text"
            placeholder="Enter description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
          />
        </Form.Group>

        <Row>
          <Col md={4}>
            <Form.Group className="mb-3" controlId="formDate">
              <Form.Label>Date</Form.Label>
              <DatePicker
                className={`styles["date-picker"] form-control`}
                showIcon
                selected={startDate}
                onChange={(date) => setStartDate(date)}
                isClearable
                placeholderText="Choose date (MM/DD/YYYY)"
              />
            </Form.Group>
          </Col>
          <Col md={5}>
            <Form.Group className="mb-3" controlId="formTime">
              <Form.Label>Time</Form.Label>
              <Row>
                <Col>
                  <DatePicker
                    className={`styles["date-picker"] form-control`}
                    selected={startTime}
                    onChange={(time) => setStartTime(time)}
                    showTimeSelect
                    showTimeSelectOnly
                    isClearable
                    timeIntervals={15}
                    timeCaption="Time"
                    dateFormat="h:mm aa"
                    placeholderText="Choose start time"
                  />
                </Col>
                <Col xs="auto">
                  <span>-</span>
                </Col>
                <Col>
                  <DatePicker
                    className={`styles["date-picker"] form-control`}
                    selected={endTime}
                    onChange={(time) => setEndTime(time)}
                    showTimeSelect
                    showTimeSelectOnly
                    isClearable
                    timeIntervals={15}
                    timeCaption="Time"
                    dateFormat="h:mm aa"
                    placeholderText="Choose end time"
                  />
                </Col>
              </Row>
            </Form.Group>
          </Col>
        </Row>
        {/* <div className={styles["note-info"]}>Based on Pacific Time</div> */}

        <Row>
          <Col md={3}>
            <Form.Group className="mb-3" controlId="formNumOfParticipant">
              <Form.Label>Number of Participants</Form.Label>
              <Form.Control
                type="number"
                placeholder="Enter number"
                value={numOfParticipant}
                onChange={(e) => setNumOfParticipant(e.target.value)}
              />
            </Form.Group>

            <Form.Group className="mb-3" controlId="formRoom">
              <Form.Label>Room</Form.Label>
              <div>
                {selectedRoom != null && (
                  <div className={styles["room-badge-group"]}>
                    <CustomBadge
                      content={selectedRoom.name}
                      deleteContent={() => deleteRoom(selectedRoom)}
                    />
                  </div>
                )}
                {selectedRoom == null && (
                  <PlusSquare
                    className={styles["search-room-button"]}
                    onClick={searchRooms}
                  />
                )}
                {selectedRoom != null && (
                  <PencilSquare
                    className={styles["search-room-button"]}
                    onClick={searchRooms}
                  />
                )}

                <Offcanvas
                  show={showSidebar}
                  placement={"end"}
                  onHide={() => setShowSidebar(false)}
                >
                  <Offcanvas.Header closeButton>
                    <Offcanvas.Title>Available Rooms</Offcanvas.Title>
                  </Offcanvas.Header>
                  <Offcanvas.Body>
                    <RoomCard
                      room={fakeRoom}
                      chooseRoom={() => chooseRoom(fakeRoom)}
                    />
                  </Offcanvas.Body>
                </Offcanvas>
              </div>
            </Form.Group>
          </Col>
          <Col>
            <Form.Group className="mb-3" controlId="formInviteGuests">
              <Form.Label>Invite Guests</Form.Label>
              <div>
                <div className={styles["input-guest-wrapper"]}>
                  <Form.Control
                    type="email"
                    placeholder="Enter email address"
                    value={curGuest}
                    onChange={(e) => setCurGuest(e.target.value)}
                  />
                  <PersonPlusFill
                    className={styles["add-guest-button"]}
                    onClick={() => addGuest(curGuest)}
                  />
                </div>
              </div>
              <div className={styles["guest-badge-group"]}>
                {guestList?.map((guest) => (
                  <CustomBadge
                    content={guest}
                    deleteContent={() => deleteGuest(guest)}
                  />
                ))}
              </div>
            </Form.Group>
          </Col>
        </Row>

        <Row>
          <Col>
            <Button
              variant="danger"
              className={styles["form-button"]}
              onClick={() => history.push("/")}
            >
              <ArrowLeftCircleFill />
              Cancel
            </Button>
          </Col>
          <Col>
            <Button
              variant="primary"
              type="submit"
              className={styles["form-button"]}
            >
              <CheckCircleFill />
              Confirm
            </Button>
          </Col>
        </Row>
      </Form>
    </MainLayout>
  );
};

// TODO: more styles on form & cards
// TODO: find a better waty for note-info
// TODO: handle required fields
