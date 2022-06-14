import React, { useState, useEffect, useContext, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { useLocation } from "react-router-dom";

import { Button, Check } from "react-bootstrap";

import { CartContext } from "../context/CartContextProvider";
import API from "../API";

import GroupCard from "../components/GroupCard";
import { toast } from "react-toastify";
import { AuthContext } from "../context/AuthContext";
import styled from "styled-components";

toast.configure();
const GroupContainer = styled.div`
  width: 40%;
  align-items: left;
  display: block;
  margin-left: auto;
  margin-right: auto;
  margin-top: 5%;
`;
const GroupSelectNewOrder = () => {
  const [cart, setCart, storeid, setStoreid] = useContext(CartContext);
  const { getTokenInfo } = useContext(AuthContext);
  const navigate = useNavigate();
  const [groups, setGroups] = useState([]);
  const [selectedGroups, setSelectedGroups] = useState([]);
  const location = useLocation();

  const handleOnClick = async () => {
    const data = {
      orderDetails: {
        orderedby: getTokenInfo().id,
        storeid: storeid,
        description: location.state.description,
        tipamount: parseInt(location.state.tip),
        orderamount: location.state.totalamount,
      },
      orderItems: [],
      group: [],
    };
    cart.map((product) => {
      data["orderItems"].push({
        productid: product.id,
        quantity: product.count,
        price: parseInt(product.price),
      });
    });

    selectedGroups.map((group) => {
      data["group"].push(parseInt(group));
    });

    const success = await API.placeOrder(data);
    if (success == true) {
      setCart([]);
      toast("Order placed successfully.");

      // TODO: Make post call to create order
      navigate("/home");
    } else {
      toast("Something went wrong...please load wallet amount.");
    }
  };

  useEffect(async () => {
    if ((await API.getGroupNames(setGroups)) == false) {
      toast("Failed loading groups.");
    }
  }, [setGroups]);

  const handleGroupSelect = useCallback((event) => {
    if (event.target.checked) {
      setSelectedGroups([...selectedGroups, event.target.value]);
    } else {
      setSelectedGroups(
        selectedGroups.filter((group) => group !== event.target.value)
      );
    }
  });

  return (
    <>
      <div
        style={{
          textAlign: "center",
          fontSize: "200%",
          marginTop: "5%",
        }}
      >
        Select Groups to post order.
      </div>
      <GroupContainer>
        {groups.map((group) => {
          return (
            <GroupCard
              group={group}
              key={group.groupid.id}
              handleGroupSelect={handleGroupSelect}
            />
          );
        })}
        <Button
          variant="dark"
          style={{ marginLeft: "80%" }}
          onClick={handleOnClick}
        >
          Place order
        </Button>
      </GroupContainer>
    </>
  );
};

export default GroupSelectNewOrder;
