import React, { useState, useEffect, useContext } from "react";
import { useNavigate, useLocation } from "react-router";
import { ChangeState } from "../api/changeorderstatus";
import { AuthContext } from "../context/AuthContext";
import styled from "styled-components";
import { toast } from "react-toastify";
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
      {person === undefined ? (
        <></>
      ) : (
        <OrderDetailContainer>
          <div
            style={{
              fontWeight: 500,
            }}
          >
            {title}
          </div>
          <DetailField label="Name" data={person.name} />
          <DetailField label="Email" data={person.email} />
          <DetailField label="Contact No" data={person.mobile} />
          <DetailField label="Address" data={person.address} />
          <DetailField label="City" data={person.city} />
          <DetailField label="Pincode" data={person.pincode} />
        </OrderDetailContainer>
      )}

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

const ChangeOrderStatus = () => {
  const navigate = useNavigate();
  const { state } = useLocation();
  const { getTokenInfo } = useContext(AuthContext);
  let buttonText = "";

  // console.log(JSON.stringify(state));
  if (state.text === "checkedout") {
    buttonText = "Check out Order";
  } else if (state.text === "completed") {
    buttonText = "Complete the Order";
  } else {
    buttonText = "";
  }

  useEffect(async () => {
    if (getTokenInfo() === null) navigate("/login");
  }, [getTokenInfo, navigate]);

  const handleStateChange = async (e) => {
    let orderid = state.objectForDetails.id;
    let body = state.body;

    body = { ...body, orderid };
    let endpoint = "";

    if (state.text === "checkedout") {
      endpoint = "/api/order/checkout";
    } else if (state.text === "completed") {
      endpoint = "/api/order/complete";
    }

    const responseData = await ChangeState(
      body,
      endpoint,
      getTokenInfo().token
    );

    if (responseData["error"] === undefined) {
      toast(`order status changed to ${state.text}`);
      if (state.from === "/showmyorder") navigate("/showmyorder");
      else {
        navigate("/showpickedorder");
      }
    } else {
      console.log("error orccured in acception");
    }
  };

  return (
    <div>
      {buttonText !== "" && (
        <Button
          style={{ float: "right", marginRight: "10%", marginTop: "1%" }}
          onClick={handleStateChange}
        >
          {buttonText}
        </Button>
      )}
      {state.placerDetails === undefined ? (
        <Detail
          person={state.acceptorDetails[0]}
          order={state.objectForDetails}
          title="Accepted By"
        />
      ) : (
        <Detail
          person={state.placerDetails[0]}
          order={state.objectForDetails}
          title="Ordered By"
        />
      )}
    </div>
  );
};

export default ChangeOrderStatus;
