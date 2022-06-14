import React, { useState, useEffect, useContext } from "react";

import { Form, Button, FloatingLabel } from "react-bootstrap";

import API from "../API";

import styled from "styled-components";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";
import {toast} from 'react-toastify';

toast.configure()

const Container = styled.div`
  display: flex;
  margin-left: 20%;
  margin-top: 5%;
  width: 80%;
  min-width: 80vw;
`;

const User = () => {
  const [userInfo, setUserInfo] = useState(null);
  const [email, setEmail] = useState();
  const [name, setName] = useState();
  const [mobile, setMobile] = useState();
  const [address, setAddress] = useState();
  const [city, setCity] = useState();
  const [pincode, setPincode] = useState();
  
  const navigate = useNavigate();
  const { getTokenInfo } = useContext(AuthContext);

  useEffect(async () => {
    if (getTokenInfo() === null) navigate("/login");
  }, [getTokenInfo, navigate]);

  let handleSubmit = async () => {
    try {
      // TODOFINAL
      const data = {
        email: email,
        name: name,
        mobile: mobile,
        address: address,
        city: city,
        pincode: pincode
      };

      const response = await API.updateUserProfile(data)
      if(response === false){
        toast('Please provide valid detail.')
      }else{
        toast('User Profile updated successfully.')
      }      
    } catch (error) {
      console.log("Didn't made API call");
    }
  };

  useEffect(() => {
    API.getUserInfo(setUserInfo);
  }, []);

  return (
    <div style={{ display: "flex" }}>
      <Container>
        <Form style={{ width: "30%" }}>
          <Form.Group className="mb-3" controlId="name">
            <FloatingLabel label="Name">
              <Form.Control
                type="text"
                placeholder="Loading..."
                defaultValue={userInfo === null ? "" : userInfo.name}
                onChange={(e) => setName(e.target.value)}
                style={{
                  borderRadius: "0",
                }}
              />
            </FloatingLabel>
          </Form.Group>

          <Form.Group className="mb-3" controlId="email">
            <FloatingLabel label="Email">
              <Form.Control
                type="text"
                placeholder="Loading..."
                defaultValue={userInfo === null ? "" : userInfo.email}
                style={{
                  borderRadius: "0",
                }}
                onChange={(e) => setEmail(e.target.value)}
              />
            </FloatingLabel>
          </Form.Group>

          <Form.Group className="mb-3" controlId="address">
            <FloatingLabel label="Address">
              <Form.Control
                type="text"
                placeholder="Loading..."
                defaultValue={userInfo === null ? "" : userInfo.address}
                onChange={(e) => setAddress(e.target.value)}
                style={{
                  borderRadius: "0",
                }}
              />
            </FloatingLabel>
          </Form.Group>

          <Form.Group className="mb-3" controlId="city">
            <FloatingLabel label="City">
              <Form.Control
                type="text"
                placeholder="Loading"
                defaultValue={userInfo === null ? "" : userInfo.city}
                onChange={(e) => setCity(e.target.value)}
                style={{
                  borderRadius: "0",
                }}
              />
            </FloatingLabel>
          </Form.Group>

          <Form.Group className="mb-3" controlId="pincode">
            <FloatingLabel label="Pincode">
              <Form.Control
                type="text"
                placeholder="Loading..."
                defaultValue={userInfo === null ? "" : userInfo.pincode}
                onChange={(e) => setPincode(e.target.value)}
                style={{
                  borderRadius: "0",
                }}
              />
            </FloatingLabel>
          </Form.Group>

          <Form.Group className="mb-3" controlId="contactno">
            <FloatingLabel label="Contact No">
              <Form.Control
                type="text"
                placeholder="Loading"
                defaultValue={userInfo === null ? "" : userInfo.mobile}
                onChange={(e) => setMobile(e.target.value)}
              />
            </FloatingLabel>
          </Form.Group>
        </Form>

        <Button
          variant="dark"
          type="submit"
          style={{ marginLeft: "20%", marginTop: "17%", height: "10%", width: "30%"}}
          onClick={handleSubmit}
        >
          Update Profile
        </Button>
      </Container>
    </div>
  );
};

export default User;
