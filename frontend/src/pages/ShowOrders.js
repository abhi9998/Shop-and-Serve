import React, { useState, useEffect, useContext } from "react";
import { AuthContext } from "../context/AuthContext";
import { useNavigate } from "react-router";
import { GetGroupCall } from "../api/getgroup";
import { GetOrderCall } from "../api/getorder";
import { GetOtherPersonDetails } from "../api/getotherpersondetails";
import styled from "styled-components";
import { Form } from "react-bootstrap";
import OrderCard from "../components/OrderCard";

const Wrapper = styled.div`
  width: 80%;
  margin-left: auto;
  margin-right: auto;
`;

const ShowOrders = () => {
  const navigate = useNavigate();
  const { storeTokenInfo, getTokenInfo } = useContext(AuthContext);

  const [myGroups, setMyGroups] = useState([]);
  const [stores, setStores] = useState([]);
  const [orders, setOrders] = useState([]);
  const [displayOrders, setDisplayOrders] = useState([]);

  const [isPartOfGroup, setIsPartOfGroup] = useState(false);

  useEffect(async () => {
    if (getTokenInfo() === null) navigate("/login");
    // console.log("going to fetch groups of user");
    const groupData = await GetGroupCall(
      getTokenInfo().id,
      getTokenInfo().token
    );
    if (groupData > 0) setIsPartOfGroup(true);
    setMyGroups(groupData);
  }, [getTokenInfo, navigate]);

  const handleGroupSelect = async (e) => {
    setDisplayOrders([]);
    const groupId = e.target.value;
    const [storeList, orderDataStoreWise] = await GetOrderCall(
      groupId,
      getTokenInfo().token
    );
    // console.log("data is ", JSON.stringify(orderDataStoreWise));
    // console.log("data is ", storeList);
    setStores(storeList);
    setOrders(orderDataStoreWise);
  };

  const handleStoreSelect = async (e) => {
    let objectOrder = {};
    setDisplayOrders([]);
    for (let i = 0; i < orders.length; i++) {
      objectOrder = orders[i];
      if (Object.keys(objectOrder)[0] == e.target.value) {
        setDisplayOrders(objectOrder[e.target.value]);
        return;
      }
    }
  };

  const handleOrderClick = async (e) => {
    let objectForDetails = {};

    displayOrders.map((order) => {
      if (order.id == e.target.value) {
        objectForDetails = order;
        // console.log(order);
      }
    });

    let acceptorDetails = {};
    if (objectForDetails.orderedby !== undefined)
      acceptorDetails = await GetOtherPersonDetails(
        objectForDetails.orderedby,
        getTokenInfo().token
      );

    let state = {};
    state = { ...state, objectForDetails, acceptorDetails };
    //console.log("here from show orders", JSON.stringify(state));
    navigate("/detailorder", { state });
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
        New Orders in your Groups
      </div>

      <div
        style={{
          marginTop: "2%",
          float: "center",
          textAlign: "center",
          fontSize: "20px",
        }}
      >
        Group
      </div>
      <Form
        style={{
          width: "50%",
          marginLeft: "auto",
          marginRight: "auto",
          textAlign: "center",
          paddingTop: "1%",
        }}
      >
        <Form.Group className="mb-3">
          <Form.Select onChange={handleGroupSelect}>
            <option key={-1}> Select Group </option>
            {myGroups.map((group) => {
              return (
                <option key={group.id} value={group.id}>
                  {group.name}
                </option>
              );
            })}
          </Form.Select>
        </Form.Group>
      </Form>

      <div
        style={{
          marginTop: "2%",
          float: "center",
          textAlign: "center",
          fontSize: "20px",
        }}
      >
        Store
      </div>

      <Form
        style={{
          width: "50%",
          marginLeft: "auto",
          marginRight: "auto",
          textAlign: "center",
          paddingTop: "0.25%",
        }}
      >
        <Form.Group className="mb-3">
          <Form.Select onChange={handleStoreSelect}>
            <option key={-1}> Select Store </option>
            {stores.map((store) => {
              return (
                <option key={store} value={store}>
                  {store}
                </option>
              );
            })}
          </Form.Select>
        </Form.Group>
      </Form>

      <div style={{ width: "100%", float: "left" }}>
        {displayOrders.map((order) => {
          if (order.orderedby != getTokenInfo().id)
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

export default ShowOrders;
