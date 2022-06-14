import React, { useState, useEffect, useContext } from "react";
import { Dropdown, DropdownButton, Form } from "react-bootstrap";
import { AuthContext } from "../context/AuthContext";
import { useNavigate } from "react-router";
import { GetPickedOrder } from "../api/getpickedorder";
import { GetOtherPersonDetails } from "../api/getotherpersondetails";
import styled from "styled-components";
import OrderCard from "../components/OrderCard";

const Wrapper = styled.div`
  width: 80%;
  margin-left: auto;
  margin-right: auto;
`;

const PickedOrder = () => {
  const navigate = useNavigate();
  const { storeTokenInfo, getTokenInfo } = useContext(AuthContext);

  const [orders, setOrders] = useState([]);
  const [displayOrders, setDisplayOrders] = useState([]);
  const [orderStatus, setOrderStatus] = useState([]);

  useEffect(async () => {
    if (getTokenInfo() === null) navigate("/login");
    // console.log("going to fetch groups of user");
    const [statusOfOrders, statusWiseOrderArray] = await GetPickedOrder(
      getTokenInfo().id,
      getTokenInfo().token
    );

    setOrders(statusWiseOrderArray);
    setOrderStatus(statusOfOrders);
  }, [getTokenInfo, navigate]);

  const handleStatusSelect = (event) => {
    // console.log("status selected", e.target.value);
    //console.log(event.target.value);
    let objectOrder = {};
    setDisplayOrders([]);
    //console.log(event.target.value);
    for (let i = 0; i < orders.length; i++) {
      objectOrder = orders[i];
      if (Object.keys(objectOrder)[0] === event.target.value) {
        setDisplayOrders(objectOrder[event.target.value]);
        return;
      }
    }
  };

  const handleOrderClick = async (e) => {
    // console.log("order clicked is ", e.target.value);
    //console.log(e.target.value);
    let objectForDetails = {};
    displayOrders.map((order) => {
      if (order.id === parseInt(e.target.value)) {
        objectForDetails = order;
      }
    });

    let placerDetails = {};
    if (objectForDetails.orderedby !== undefined)
      placerDetails = await GetOtherPersonDetails(
        objectForDetails.orderedby,
        getTokenInfo().token
      );

    let state = {};
    let text = null;
    let body = {};

    if (objectForDetails["status"] === "accepted") {
      text = "checkedout";
    } else if (objectForDetails["status"] === "checkedout") {
      text = "completed";
    }

    //data is sent from here so that ver can decouple change order status page so that it can be used by both compo pickedorder and my orders
    let acceptorid = getTokenInfo().id;
    let placerid = null;

    body = { ...body, acceptorid, placerid };
    state = { ...state, objectForDetails, text, body, placerDetails };
    console.log("here from the picked order", JSON.stringify(state));
    navigate("/changeorderstatus", { state });
  };

  return (
    <Wrapper>
      <div
        style={{
          marginTop: "1%",
          fontWeight: "50x",
          float: "center",

          textAlign: "center",
          fontSize: "30px",
        }}
      >
        Orders To complete
      </div>

      <Form
        style={{
          width: "50%",
          marginLeft: "auto",
          marginRight: "auto",
          textAlign: "center",
          paddingTop: "2%",
        }}
      >
        <Form.Group className="mb-3">
          <Form.Select onChange={handleStatusSelect}>
            <option key={-1}> Select Status Of Order </option>
            {orderStatus.map((status) => {
              return (
                <option key={status} value={status}>
                  {status}
                </option>
              );
            })}
          </Form.Select>
        </Form.Group>
      </Form>
      <div style={{ width: "100%", float: "left" }}>
        {displayOrders.map((order) => {
          return (
            <OrderCard
              handleOrderClick={handleOrderClick}
              key={order.id}
              order={order}
            />
          );
        })}
      </div>
    </Wrapper>
  );
};

export default PickedOrder;
