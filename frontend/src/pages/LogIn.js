import React, { useContext, useEffect, useState } from "react";
import FormContainer from "../components/FormContainer";

import styled from "styled-components";
import { Form, Button, Row, Col } from "react-bootstrap";
import { useNavigate } from "react-router";

import { AuthContext } from "../context/AuthContext";
import { LoginCall } from "../api/loginapi";
import { USER_LOGIN_PAGE_BACKGROUND } from "../config";
import {toast} from 'react-toastify';

toast.configure()

const Container = styled.div`
  background: ${() => `url('${USER_LOGIN_PAGE_BACKGROUND}')`};
  background-size: cover;
  min-height: 88vh;
  min-width: 80vw;
  height: 100%;
  width: 100%;
  padding: 4%;
`;

const Content = styled.div`
  /* background: rgba(235, 228, 228, 1); */
  padding: 10px;
  width: 50%;
  height: 40%;
  text-align: left;
  margin: 0% 35% 0% 10%;
  border-radius: 25px;
  font-weight: 400;
  height: 100%;
`;

const FormContainerStyle = styled.div`
  font-weight: 200;
`;

const LogIn = () => {
  const [loadLogIn, setLoadLogIn] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  let navigate = useNavigate();

  const { storeTokenInfo, getTokenInfo } = useContext(AuthContext);

  useEffect(() => {
    if (getTokenInfo() !== null) navigate("/home");
    setLoadLogIn(true);
  }, [getTokenInfo, navigate]);

  let handleSubmit = async (e) => {
    e.preventDefault();
    const data = await LoginCall({ email, password });
    if(data.error !== undefined){
      toast('Log in attempt failed')
      navigate("/login")
    }else{
      storeTokenInfo(data);
      toast('Logged In successfully')
      navigate("/home");
    }
  };

  const displayForm = () => {
    return (
      <FormContainerStyle>
        <FormContainer>
          <Form onSubmit={handleSubmit}>
            <Form.Group className="mb-3" controlId="Email">
              <Form.Label>Email</Form.Label>
              <Form.Control
                type="email"
                placeholder="abc@email.com"
                onChange={(e) => setEmail(e.target.value)}
              />
            </Form.Group>

            <Form.Group className="mb-3" controlId="password">
              <Form.Label>Password</Form.Label>
              <Form.Control
                type="password"
                placeholder="password"
                onChange={(e) => setPassword(e.target.value)}
              />
            </Form.Group>

            <Button
              type="submit"
              style={{
                marginTop: "3%",
                backgroundColor: "gray",
                border: "gray",
                width: "100%",
              }}
            >
              Submit
            </Button>
          </Form>
        </FormContainer>
      </FormContainerStyle>
    );
  };

  return (
    <Container img="../images/grocery-shopping.jpg">
      <Content>
        <div
          style={{
            margin: "5%",
            fontSize: "25px",
            fontWeight: "500",
            textAlign: "center",
          }}
        >
          Welcome back
        </div>
        {displayForm()}
      </Content>
    </Container>
  );
};
export default LogIn;
