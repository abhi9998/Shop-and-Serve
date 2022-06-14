import React from "react";
import { Card } from "react-bootstrap";

import styled from "styled-components";

const Wrapper = styled.div`
  margin: 3%;
  background: var(--white);
  border-radius: 4px solid black;
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
`;
const Content = styled.div``;

const GroupCard = ({ group, handleGroupSelect }) => {
  return (
    <>
      <Wrapper>
        <Content>
          <Card className="text-left">
            <Card.Body style={{ display: "inline-block", float: "left" }}>
              <div style={{ width: "60%" }}>
                <div>Name: {group.groupid.name}</div>
                <div>Type: {group.groupid.type}</div>
                <div>City: {group.groupid.city}</div>
              </div>
            </Card.Body>
            <Card.Footer style={{ backgroundColor: "#aaa" }}>
              <input
                type="checkbox"
                onChange={handleGroupSelect}
                value={group.groupid.id}
                style={{
                  marginLeft: "90%",
                  marginRight: "1%",
                  width: "30px",
                  height: "30px",
                  backgroundColor: "black",
                }}
              ></input>
            </Card.Footer>
          </Card>
        </Content>
      </Wrapper>
    </>
  );
};

export default GroupCard;
