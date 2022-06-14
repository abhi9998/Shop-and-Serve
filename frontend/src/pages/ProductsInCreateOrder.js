import React, { useState, useEffect, useContext, useCallback } from "react";
import { Button } from "react-bootstrap";
import { Navigate, useParams } from "react-router-dom";
import { useNavigate, useLocation } from "react-router-dom";
import styled from "styled-components";

import API from "../API";

import { CartContext } from "../context/CartContextProvider";

import ProductThumbInCreateOrder from "../components/ProductThumbInCreateOrder";
import { AuthContext } from "../context/AuthContext";

const EmptyStore = () => {
  return <>Empty store no products available.</>;
};

const Content = styled.div`
  width: 80%;
  margin-left: auto;
  margin-right: auto;
`;

const StoreDetail = styled.div`
  font-size: 15px;
  font-family: "Times New Roman";
  margin-left: 8%;
  margin-right: auto;
`;

const ProductsInCreateOrder = () => {
  const { storeId } = useParams();
  const [products, setProducts] = useState([]);
  const [storeInfo, setStoreInfo] = useState([]);
  const [cart, setCart, storeid, setstoreid] = useContext(CartContext);
  const [totalCartValue, setTotalCartValue] = useState(0);

  const navigate = useNavigate();
  const { getTokenInfo } = useContext(AuthContext);

  useEffect(async () => {
    if (getTokenInfo() === null) navigate("/login");
  }, [getTokenInfo, navigate]);

  useEffect(() => {
    setstoreid(storeId)
    API.getProductsOfStore(storeId, setProducts);
    API.getStoreInfo(storeId, setStoreInfo);
  }, [storeId]);

  const handleProceedToReview = () => {
    updateCartValue();
    navigate(`/neworder/stores/${storeId}/products/review`, {
      state: { isPathFollowed: 1, storeId: storeId, totalamount: totalCartValue },
    });
  };

  const updateCartValue = useCallback(() => {
    let total = 0;
    cart.map((product) => {
      total = total + parseFloat(product.count) * parseFloat(product.price);
    });
    setTotalCartValue(total);
  });

  useEffect(() => {
    updateCartValue();
  }, [setTotalCartValue, updateCartValue]);

  return (
    <div>
      <StoreDetail>
        <div
          style={{
            fontSize: "220%",
            marginLeft: "3%",
            paddingTop: "1%",
            marginTop: "1%",
          }}
        >
          {storeInfo.name}
          <div style={{ float: "right", marginRight: "15%", fontSize: "80%" }}>
            Cart Value: {totalCartValue} <br />
            {cart.length === 0 ? (
              <></>
            ) : (
              <Button onClick={handleProceedToReview} style={{backgroundColor: "gray", outline: "0"}}>
                Proceed To Checkout
              </Button>
            )}
            <br />
          </div>
        </div>
        <div style={{ marginLeft: "3%", fontSize: "100%", paddingTop: "1%" }}>
          <div>{storeInfo.address}</div>
          <div>{storeInfo.city}</div>
          <div>{storeInfo.pincode}</div>
        </div>
      </StoreDetail>
      <Content>
        <hr />
        <br />
        <b style={{ fontWeight: "500" }}>Product available</b>
        <br />
        {products.length === 0 ? (
          <EmptyStore />
        ) : (
          products.map((product) => {
            if (
              cart.findIndex(
                (o) => o.id.toString() === product.id.toString()
              ) !== -1
            ) {
              return (
                <ProductThumbInCreateOrder
                  key={product.id}
                  product={
                    cart.filter(
                      (p) => p.id.toString() === product.id.toString()
                    )[0]
                  }
                  products={products}
                  totalCartValue={totalCartValue}
                  updateCartValue={updateCartValue}
                ></ProductThumbInCreateOrder>
              );
            } else {
              return (
                <ProductThumbInCreateOrder
                  key={product.id}
                  product={product}
                  products={products}
                  totalCartValue={totalCartValue}
                  updateCartValue={updateCartValue}
                ></ProductThumbInCreateOrder>
              );
            }
          })
        )}
      </Content>
    </div>)
}

export default ProductsInCreateOrder;