import React, { useState } from "react";
import FormContainer from "../components/FormContainer";
import styled from "styled-components";

import { Form, Button } from "react-bootstrap";
import {toast} from 'react-toastify';

toast.configure()

const Container = styled.div`
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
  margin: 0% 25% 0% 25%;
  border-radius: 25px;
  font-weight: 400;
  height: 100%;
`;

const FormContainerStyle = styled.div`
  font-weight: 200;
`;

const AdminLogin = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  let handleSubmit = async () => {
    toast(
      "Log in attempt with email ->" + email + " ..password -> " + password
    );
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

            <Button type="submit" style={{marginTop: "3%", backgroundColor: "gray", border: "gray", width: "100%"}}>
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
        <div style={{ margin: "5%", fontSize: "25px", fontWeight: "500", textAlign: "center"}}>Log in as admin</div>
        {displayForm()}
      </Content>
    </Container>
  );
};
export default AdminLogin;
