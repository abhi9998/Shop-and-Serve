import React, { useState, useEffect, useContext } from "react";
import { useNavigate, useLocation } from "react-router";
import { AcceptOrder } from "../api/acceptorder";
import { AuthContext } from "../context/AuthContext";
import { toast } from "react-toastify";
import styled from "styled-components";
import { Button, FloatingLabel, Form } from "react-bootstrap";

toast.configure();
const Wrapper = styled.div`
  padding: 2%;
`;

const PersonDetailContainer = styled.div`
  width: 40%;
  display: inline-block;
`;

const OrderDetailContainer = styled.div`
  width: 40%;
  float: right;
  margin-right: 10%;
  margin-top: 0.5%;
`;

const OrderField = ({ data }) => {
  return (
    <div
      style={{
        borderRadius: "4px solid black",
        boxShadow:
          "0 2px 4px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)",
        padding: "1%",
        backgroundColor: "#e9ecef",
        marginTop: "1%",
      }}
    >
      <FloatingLabel
        style={{
          marginTop: "3%",
        }}
        disabled
      >
        <div disabled>Product Name: {data.name}</div>
        <div disabled>Total Cost: {data.price}</div>
        <div disabled>Total Quantity: {data.quantity}</div>
      </FloatingLabel>
    </div>
  );
};

const DetailField = ({ label, data }) => {
  return (
    <div
      style={{
        borderRadius: "4px solid black",
        boxShadow:
          "0 2px 4px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)",
      }}
    >
      <FloatingLabel label={label} style={{ marginTop: "2%" }}>
        <Form.Control
          type="textarea"
          value={data}
          style={{
            borderRadius: "0",
          }}
          disabled
        />
      </FloatingLabel>
    </div>
  );
};

const Detail = ({ person, order, title }) => {
  return (
    <Wrapper>
      <div
        style={{
          fontWeight: 500,
        }}
      >
        Order Detail
      </div>
      <PersonDetailContainer>
        <DetailField label="Store" data={order.storename} />
        <DetailField label="Description" data={order.description} />
        <DetailField label="Order Amount" data={order.orderamount} />
        <DetailField label="Tip" data={order.tipamount} />
        <DetailField label="Order Status" data={order.status} />
        <DetailField
          label="Created on"
          data={order.createdtime.substr(0, 10)}
        />
        {order.acceptedtime !== null ? (
          <DetailField
            label="Accepted on"
            data={order.acceptedtime.substr(0, 10)}
          />
        ) : (
          <></>
        )}
        {order.checkedouttime !== null ? (
          <DetailField
            label="Checed out on"
            data={order.checkedouttime.substr(0, 10)}
          />
        ) : (
          <></>
        )}
        {order.deliverytime !== null ? (
          <DetailField
            label="Completed on"
            data={order.deliverytime.substr(0, 10)}
          />
        ) : (
          <></>
        )}
      </PersonDetailContainer>

      <div
        style={{
          marginTop: "2%",
          fontWeight: 500,
        }}
      >
        Product Details
      </div>
      <div style={{ width: "30%" }}>
        {order.orderItems.map((item) => {
          return (
            <OrderField
              data={{
                name: item.name,
                quantity: item.quantity,
                price: item.price,
              }}
            ></OrderField>
          );
        })}
      </div>
    </Wrapper>
  );
};

const DetailOrder = () => {
  const navigate = useNavigate();
  const { state } = useLocation();
  const { storeTokenInfo, getTokenInfo } = useContext(AuthContext);

  useEffect(async () => {
    if (getTokenInfo() === null) navigate("/login");
  }, [getTokenInfo, navigate]);

  const handleAcceptOrder = async (e) => {
    let orderid = state.objectForDetails.id;
    let acceptorid = getTokenInfo().id;
    let body = { orderid, acceptorid };

    const responseData = await AcceptOrder(body, getTokenInfo().token);
    if (responseData["error"] === undefined) {
      //console.log("order accepted", JSON.stringify(responseData));
      toast("order accepted successfully");
      navigate("/home");
    } else {
      console.log("error orccured in acception");
    }
  };

  // return (
  //   <div>
  //     <p>{JSON.stringify(state)}</p>

  //     <button onClick={handleAcceptOrder}>Accept this order</button>
  //   </div>
  // );

  return (
    <div>
      <Button
        style={{ float: "right", marginRight: "10%", marginTop: "1%" }}
        onClick={handleAcceptOrder}
      >
        Accept The Order
      </Button>

      <Detail key={state.objectForDetails.id} order={state.objectForDetails} />
    </div>
  );
};

export default DetailOrder;
