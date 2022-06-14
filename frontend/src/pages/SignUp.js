import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import styled from "styled-components";

import { Form, Button } from "react-bootstrap";
import API from "../API";
import {toast} from 'react-toastify';

toast.configure()

const Wrapper = styled.div`
  width: 30%;
  margin-left: auto;
  margin-right: auto;
  box-shadow: 0 10px 10px 10px rgba(0, 0, 0, 0.2),
    0 6px 20px 0 rgba(0, 0, 0, 0.19);
  padding: 2%;
  margin-top: 2%;
`;

const SignUp = () => {
  const [name, setName] = useState("");
  const [address, setAddress] = useState("");
  const [city, setCity] = useState("");
  const [pincode, setPincode] = useState("");
  const [password, setPassword] = useState("");
  const [email, setEmail] = useState("");
  const [contactno, setContactNo] = useState("");
  const navigate = useNavigate();

  let handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const data = {
        name: name,
        address: address,
        city: city,
        pincode: pincode,
        password: password,
        email: email,
        mobile: contactno,
      };
      const response = await API.signUp(data);
      if(response === false){
        toast('Please provide valid detail.')
      }else{
        toast('User sign up successfully.')
        navigate("/");
      }
    } catch (error) {
      console.log("Sign Up Failed."); // TODO
    }
  };

  return (
    <div style={{ alignItems: "center" }}>
      <Wrapper>
        <Form onSubmit={handleSubmit}>
          <div
            style={{
              marginLeft: "35%",
              marginBottom: "2%",
              fontSize: "125%",
            }}
          >
            Sign Up !
          </div>
          <Form.Group className="mb-3" controlId="name">
            <Form.Control
              type="text"
              placeholder="Name"
              onChange={(e) => setName(e.target.value)}
              style={{
                outline: "0",
                borderWidth: "0 0 2px",
                borderRadius: "0",
              }}
            />
          </Form.Group>

          <Form.Group className="mb-3" controlId="address">
            <Form.Control
              type="text"
              placeholder="Address"
              style={{
                outline: "0",
                borderWidth: "0 0 2px",
                borderRadius: "0",
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
                borderRadius: "0",
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
                borderRadius: "0",
              }}
              onChange={(e) => setPincode(e.target.value)}
            />
          </Form.Group>

          <Form.Group className="mb-3" controlId="email">
            <Form.Control
              type="email"
              placeholder="Enter email"
              style={{
                outline: "0",
                borderWidth: "0 0 2px",
                borderRadius: "0",
              }}
              onChange={(e) => setEmail(e.target.value)}
            />
          </Form.Group>

          <Form.Group className="mb-3" controlId="contactNo">
            <Form.Control
              type="text"
              placeholder="Contact No."
              style={{
                outline: "0",
                borderWidth: "0 0 2px",
                borderRadius: "0",
              }}
              onChange={(e) => setContactNo(e.target.value)}
            />
          </Form.Group>

          <Form.Group className="mb-3" controlId="password">
            <Form.Control
              type="password"
              placeholder="Password"
              style={{
                outline: "0",
                borderWidth: "0 0 2px",
                borderRadius: "0",
              }}
              onChange={(e) => setPassword(e.target.value)}
            />
          </Form.Group>

          <Form.Group className="mb-3" controlId="rePassword">
            <Form.Control
              type="password"
              placeholder="Re-Enter Password"
              style={{
                outline: "0",
                borderWidth: "0 0 2px",
                borderRadius: "0",
              }}
            />
          </Form.Group>

          <Button
            variant="dark"
            type="submit"
            style={{ marginLeft: "46%", marginTop: "2%", marginBottom: "2%" }}
          >
            Sign Up
          </Button>
        </Form>
      </Wrapper>
    </div>
  );
};

export default SignUp;
