import React, { useState } from "react";
import FormContainer from "../components/FormContainer";

import { Form, Button } from "react-bootstrap";
import API from "../API";
import { useNavigate } from "react-router-dom";
import styled from "styled-components";
import { STORE_IMAGE_BACKGROUND } from "../config";
import {toast} from 'react-toastify';

toast.configure()

const Wrapper = styled.div`
  background: ${() => `url('${STORE_IMAGE_BACKGROUND}')`};
  height: 100%;
  min-height: 100vh;
  padding-top: 3%;
`;

const Content = styled.div`
  background-color: white;
  width: 50%;
  margin-left: auto;
  margin-right: auto;
  margin-top: auto;
  margin-bottom: auto;
  padding: 0% 2% 2% 2%;
  box-shadow: 0 10px 10px 10px rgba(0, 0, 0, 0.2),
    0 6px 20px 0 rgba(0, 0, 0, 0.19);
`;

const AddStore = () => {
  const [name, setName] = useState("");
  const [address, setAddress] = useState("");
  const [city, setCity] = useState("");
  const [pincode, setPincode] = useState("");

  const navigate = useNavigate();

  let handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const data = {
        name: name,
        address: address,
        city: city,
        pincode: pincode,
      };
      const response = await API.addStore(data);
      toast("Store Submitted successfully.");

      navigate("/admin/addstore");
    } catch (error) {
      toast("Something went wrong.");
    }
  };

  return (
    <Wrapper>
      <Content>
        <FormContainer>
          <Form onSubmit={handleSubmit}>
            <div
              style={{
                fontWeight: "800",
                fontSize: "150%",
                textAlign: "center",
                margin: "10%",
              }}
            >
              Create New Store
            </div>
            <Form.Group className="mb-3" controlId="name">
              <Form.Control
                type="text"
                placeholder="Store Name"
                onChange={(e) => setName(e.target.value)} 
                style={{
                  outline: "0",
                  borderWidth: "0 0 2px",
                  borderRadius: "0" 
                }}
              />
            </Form.Group>

            <Form.Group className="mb-3" controlId="address">
              <Form.Control
                type="text"
                placeholder="Address" 
                style={{
                  outline: "0",
                  borderWidth: "0 0 2px" ,
                  marginTop: "8%",
                  borderRadius: "0"
                }}
                onChange={(e) => setAddress(e.target.value)}
              />
            </Form.Group>

            <Form.Group className="mb-3" controlId="city">
              <Form.Control
                type="text"
                placeholder="City" 
                style={{
                  outline: "0",
                  borderWidth: "0 0 2px",
                  marginTop: "8%",
                  borderRadius: "0" 
                }}
                onChange={(e) => setCity(e.target.value)}
              />
            </Form.Group>

            <Form.Group className="mb-3" controlId="pincode">
              <Form.Control
                type="text"
                placeholder="Pincode" 
                style={{
                  outline: "0",
                  borderWidth: "0 0 2px",
                  marginTop: "8%",
                  borderRadius: "0"
                }}
                onChange={(e) => setPincode(e.target.value)}
              />
            </Form.Group>

            <div style={{
                marginLeft: 'auto',
                marginRight: 'auto',
                float: 'center',
                width: '50%'
            }}>
              <Button variant="dark" style={{width: '100%', marginTop: "18%", marginBottom: "15%", borderRadius: '20px'}} type="submit">
                Submit
              </Button>
            </div>
          </Form>
        </FormContainer>
      </Content>
    </Wrapper>
  );
};

export default AddStore;
