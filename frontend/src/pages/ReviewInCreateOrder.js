import React, { useState, useEffect, useContext } from "react";
import { Form, Button, FloatingLabel } from "react-bootstrap";
import { useLocation } from "react-router-dom";
import { useNavigate } from "react-router-dom";

import { CartContext } from "../context/CartContextProvider";
import ProductReviewThumb from "../components/ProductReviewThumb";
import { AuthContext } from "../context/AuthContext";
import {toast} from 'react-toastify';

toast.configure()

const EmptyCart = () => {
  const navigate = useNavigate();
  const { getTokenInfo } = useContext(AuthContext);

  useEffect(async () => {
    if (getTokenInfo() === null) navigate("/login");
  }, [getTokenInfo, navigate]);

  useEffect( () => {
    toast("Empty cart can't be reviewed.")
    navigate('/neworder')
  }
  , [navigate])

  return (
    <>
      <p>Cart is Empty.</p>
    </>
  );
};

const ReviewInCreateOrder = () => {
  const [cart, setCart, storeid, setStoreId] = useContext(CartContext);
  const location = useLocation();
  const navigate = useNavigate();
  const [tip, setTip ] = useState();
  const [description, setDescription ] = useState();

  useEffect(() => {
    if (
      !location.state ||
      !location.state.isPathFollowed ||
      location.state == null ||
      location.state.isPathFollowed == null ||
      location.state.storeId == null
    ) {
      setCart(null);
      navigate("/home");
    }
  }, [location.state, navigate, setCart]);

  const handleFinalize = (event) => {
    navigate('/neworder/groups/', { state: { description: description, tip: tip, totalamount: location.state.totalamount}})
  };

  const editOrder = (event) => {
    navigate(`/neworder/stores/${location.state.storeId}/products`);
  };

  return (
    <div style={{ marginLeft: "auto", marginRight: "auto", width: "100%" }}>
      {cart.length === 0 ? (
        <EmptyCart />
      ) : (
        cart.map((product) => {
          return (
            <ProductReviewThumb
              key={product.id}
              product={product}
            ></ProductReviewThumb>
          );
        })
      )}
      <br></br>
      <div style={{ marginTop: "2%" }}>
      <Form style={{ width: "30%", marginLeft: "auto", marginRight: "auto" }}>
          <Form.Group className="mb-3" controlId="tip">
            <FloatingLabel label="Enter tip amount">
              <Form.Control
                type="number"
                min="0"
                placeholder="Tip amount"
                onChange={(e) => setTip(e.target.value)}
                style={{
                  borderRadius: "0",
                }}
              />
            </FloatingLabel>
            <FloatingLabel label="Enter Description">
              <Form.Control
                type="textarea"
                placeholder="Description"
                onChange={(e) => setDescription(e.target.value)}
                style={{
                  borderRadius: "0",
                  marginTop: "3%"
                }}
              />
            </FloatingLabel>
          </Form.Group>
</Form>
        <Button
          onClick={editOrder}
          style={{ marginLeft: "38%", marginRight: "auto" }}
          variant="dark"
        >
          Edit Order
        </Button>
        <Button
          onClick={handleFinalize}
          style={{ marginLeft: "8%", marginRight: "auto" }}
          variant="success"
        >
          Finalize
        </Button>
        </div>
    </div>
  );
};

export default ReviewInCreateOrder;
