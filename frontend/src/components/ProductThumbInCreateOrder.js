import React, { useContext, useState, useRef, useEffect } from "react";
import styled from "styled-components";

import { Button, Card } from "react-bootstrap";

import { CartContext } from "../context/CartContextProvider";

const Container = styled.div`
  background: #ddd;
  margin: 10px;
  position: relative;
  display: inline-block;
  width: 30%;
  padding: 10px;
`;

const ProductThumbInCreateOrder = ({
  product,
  products,
  totalCartValue,
  updateCartValue,
}) => {
  const [cart, setCart] = useContext(CartContext);

  const handleAddProduct = (event) => {
    let priceToAdd = 0;
    if (cart.findIndex((o) => o.id.toString() === event.target.value) !== -1) {
      let newCart = [];
      cart.map((product) => {
        if (product.id.toString() === event.target.value) {
          product.count = product.count + 1;
          priceToAdd = product.price;
        }
        newCart.push(product);
      });
      setCart(newCart);
    } else {
      let newProduct = products.filter(
        (o) => o.id.toString() === event.target.value
      )[0];
      newProduct.count = 1;
      priceToAdd = newProduct.price;
      setCart([...cart, newProduct]);
    }
    updateCartValue(parseInt(totalCartValue) + parseInt(priceToAdd));
  };

  const handleRemoveProduct = (event) => {
    let priceToSubtract = 0;
    if (cart.findIndex((o) => o.id.toString() === event.target.value) !== -1) {
      let newCart = [];
      cart.map((product) => {
        if (product.count > 0 && product.id.toString() === event.target.value) {
          product.count = product.count - 1;
          priceToSubtract = product.price;
        }
        if (product.count > 0) {
          newCart.push(product);
        }
      });
      setCart(newCart);
    }
    updateCartValue(parseInt(totalCartValue) - parseInt(priceToSubtract));
  };

  return (
    <Container>
      <Card>
        <Card.Body>{product.name}</Card.Body>
        <Card.Footer style={{ background: "#bbb" }}>
          <div style={{ float: "right" }}>
            <Button
              variant={"dark"}
              style={{ float: "right" }}
              value={product.id}
              onClick={handleAddProduct}
            >
              +
            </Button>{" "}
            <Button
              variant="dark"
              style={{
                float: "right",
                marginRight: "10px",
                marginLeft: "10px",
              }}
              value={product.id}
              onClick={handleRemoveProduct}
            >
              -
            </Button>
            <div style={{ float: "left" }}>{product.count > 0 ? ('Qty'): ('')} {product.count}</div>
          </div>
          <div style={{ float: "left", marginRight: "10px" }}>
            {'price: '}{product.price}{" "}
          </div>
        </Card.Footer>
      </Card>
    </Container>
  );
};

export default ProductThumbInCreateOrder;
