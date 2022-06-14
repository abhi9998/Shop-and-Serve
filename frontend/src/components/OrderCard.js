import React from "react";
import { Button, Card } from "react-bootstrap";

import styled from "styled-components";

const Wrapper = styled.div`
  width: 24%;
  height: 100%;
  position: relative;
  display: inline-block;
  margin: 2%;
`;
const Content = styled.div``;

const OrderCard = ({ order, handleOrderClick }) => {
  return (
    <Wrapper>
      <Content>
        <Card>
          <Card.Title></Card.Title>
          <Card.Body>
            <div>Store: {order.storename}</div>
            <div>Ordered on: {order.createdtime.substring(0, 10)}</div>
            <div>Order Amount: {order.orderamount}</div>
            <div>Tip Amount: {order.tipamount}</div>
          </Card.Body>
          <Card.Footer style={{ backgroundColor: "#aaa" }}>
            <Button
              onClick={handleOrderClick}
              value={order.id}
              style={{ background: "#111", float: "right" }}
            >
              Show Detail
            </Button>
          </Card.Footer>
        </Card>
      </Content>
    </Wrapper>
  );
};

export default OrderCard;
