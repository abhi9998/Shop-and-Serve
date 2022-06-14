import React, { useState, useEffect, useContext } from "react";
import { AuthContext } from "../context/AuthContext";
import { useNavigate } from "react-router";
import { GetMyOrders } from "../api/getmyorder";
import { GetOtherPersonDetails } from "../api/getotherpersondetails";
import styled from "styled-components";
import { Form } from "react-bootstrap";
import OrderCard from "../components/OrderCard";

const Wrapper = styled.div`
  width: 80%;
  margin-left: auto;
  margin-right: auto;
`;

const MyOrder = () => {
  const navigate = useNavigate();
  const { storeTokenInfo, getTokenInfo } = useContext(AuthContext);

  const [orders, setOrders] = useState([]);
  const [displayOrders, setDisplayOrders] = useState([]);
  const [orderStatus, setOrderStatus] = useState([]);

  useEffect(async () => {
    if (getTokenInfo() === null) navigate("/login");

    const [statusOfOrders, statusWiseOrderArray] = await GetMyOrders(
      getTokenInfo().id,
      getTokenInfo().token
    );

    setOrders(statusWiseOrderArray);
    setOrderStatus(statusOfOrders);
  }, [getTokenInfo, navigate]);

  const handleStatusSelect = (e) => {
    // console.log("status selected", e.target.value);

    let objectOrder = {};
    setDisplayOrders([]);
    for (let i = 0; i < orders.length; i++) {
      objectOrder = orders[i];
      if (Object.keys(objectOrder)[0] === e.target.value) {
        setDisplayOrders(objectOrder[e.target.value]);
        return;
      }
    }
  };

  const handleOrderClick = async (e) => {
    let objectForDetails = {};
    displayOrders.map((order) => {
      if (order.id === parseInt(e.target.value)) {
        objectForDetails = order;
      }
    });

    let acceptorDetails = {};
    if (objectForDetails.acceptedby !== undefined)
      acceptorDetails = await GetOtherPersonDetails(
        objectForDetails.acceptedby,
        getTokenInfo().token
      );

    let state = {};
    let text = null;

    if (objectForDetails["status"] === "checkedout") {
      text = "completed";
    }

    let body = {};
    body = {
      ...body,
      placerid: getTokenInfo().id,
      acceptorid: null,
    };
    state = { ...state, body };
    state = {
      ...state,
      objectForDetails,
      text,
      from: "/showmyorder",
      acceptorDetails,
    };

    // console.log("here in myorder", state);
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
        Orders I placed
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

export default MyOrder;
