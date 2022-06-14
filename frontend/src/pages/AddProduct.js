import React, { useEffect, useState } from "react";
import FormContainer from "../components/FormContainer";

import { Form, Button } from "react-bootstrap";
import API from "../API";
import { useNavigate } from "react-router-dom";

import styled from "styled-components";
import {toast} from 'react-toastify';

toast.configure()

const Wrapper = styled.div`
  height: 100%;
  min-height: 100vh;
  padding-top: 3%;
  margin-bottom: 1%;
  padding-bottom: 3%;
`;

const Content = styled.div`
  background-color: #aaa;
  width: 60%;
  margin-left: auto;
  margin-right: auto;
  margin-bottom: auto;
`;

const AddProduct = () => {
  const [name, setName] = useState("");
  const [brand, setBrand] = useState("");
  const [imageLink, setImageLink] = useState("");
  const [description, setDescription] = useState("");
  const [price, setPrice] = useState("");
  const [weight, setWeight] = useState("");
  const [storeId, setStoreId] = useState("");
  const [stores, setStores] = useState([]);
  const navigate = useNavigate();

  let handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const data = {
        name: name,
        brand: brand,
        imagelink: imageLink,
        description: description,
        price: price,
        weight: weight,
        storeid: storeId,
      };

      const response = await API.addProduct(data);
      toast("Product added successfully.");

      navigate("/admin/addproduct");
    } catch (error) {
      toast("Something went wrong.");
    }
  };

  useEffect(() => {
    API.getStores(setStores);
  }, []);

  return (
    <Wrapper>
      <Content>
        <FormContainer>
          <div style={{ fontWeight: "600", margin: "8% auto 5% 0%", fontSize: "125%" }}>
            Add Product
          </div>
          <Form onSubmit={handleSubmit}>
            <Form.Group className="mb-3" controlId="storeid">
              <Form.Label>Store</Form.Label>
              <Form.Select onChange={(e) => setStoreId(e.target.value)}>
                {stores.map((store) => {
                  return (
                    <option key={store.id} value={store.id}>
                      {store.name}
                    </option>
                  );
                })}
              </Form.Select>
            </Form.Group>

            <Form.Group className="mb-3" controlId="name">
              <Form.Label>Product Name</Form.Label>
              <Form.Control
                type="text"
                placeholder="Name"
                onChange={(e) => setName(e.target.value)}
              />
            </Form.Group>

            <Form.Group className="mb-3" controlId="brand">
              <Form.Label>Brand</Form.Label>
              <Form.Control
                type="text"
                placeholder="Brand"
                onChange={(e) => setBrand(e.target.value)}
              />
            </Form.Group>

            <Form.Group className="mb-3" controlId="imagelink">
              <Form.Label>ImageLink</Form.Label>
              <Form.Control
                type="text"
                placeholder="Image Link"
                onChange={(e) => setImageLink(e.target.value)}
              />
            </Form.Group>

            <Form.Group className="mb-3" controlId="description">
              <Form.Label>Description</Form.Label>
              <Form.Control
                type="text"
                placeholder="Description"
                onChange={(e) => setDescription(e.target.value)}
              />
            </Form.Group>

            <Form.Group className="mb-3" controlId="price">
              <Form.Label>Price</Form.Label>
              <Form.Control
                type="text"
                placeholder="Price"
                onChange={(e) => setPrice(e.target.value)}
              />
            </Form.Group>

            <Form.Group className="mb-3" controlId="weight">
              <Form.Label>Weight</Form.Label>
              <Form.Control
                type="text"
                placeholder="Weight (gms)"
                onChange={(e) => setWeight(e.target.value)}
              />
            </Form.Group>

            <Button
              variant="dark"
              type="submit"
              style={{ marginBottom: "6%", marginTop: "3%", width: "100%" }}
            >
              Submit
            </Button>
          </Form>
        </FormContainer>
      </Content>
    </Wrapper>
  );
};

export default AddProduct;
