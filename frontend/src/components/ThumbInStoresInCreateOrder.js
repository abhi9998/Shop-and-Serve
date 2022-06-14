import React from "react";
import { useNavigate } from "react-router-dom";
import styled from "styled-components";
import { InputGroup } from "react-bootstrap";
import Image from 'react-bootstrap/Image'

import LocationImg from '../images/location.png';
import CityImg from '../images/city.png';
import PostalImg from '../images/pincode.jpg';

import { Button, Card } from "react-bootstrap";

const Wrapper = styled.div`
  margin: 3%;
  background: var(--white);
  border-radius: 4px solid black;
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
`;

const ThumbInStoreInCreateOrder = ({ store }) => {
  const navigate = useNavigate();

  const handleClick = () => {
    navigate(`/neworder/stores/${store.id}/products`);
  };

  return (
    <Wrapper>
      <Card className="text-left">
        <Card.Body>
          {store.name}
          <div style={{ float: "right" }}>
            <Button variant="dark" onClick={handleClick}>
              Select
            </Button>
          </div>
        </Card.Body>
        <Card.Footer style={{ background: "#ddd", display: "inline", whiteSpace: "nowrap"}}>
          <Image src={LocationImg} alt="missing" style={{width: "5.5%", height: "5.5%", marginRight: "1%"}}/>
          {store.address}
          <Image src={CityImg} style={{width: "4.5%", height: "4%", marginLeft: "10%", marginRight: "1%"}}/>
          {store.city}
          <Image src={PostalImg} style={{width: "4.5%", height: "4%", marginLeft: "10%", marginRight: "1%"}}/>
          {store.pincode}
        </Card.Footer>
      </Card>
    </Wrapper>
  );
};

export default ThumbInStoreInCreateOrder;
