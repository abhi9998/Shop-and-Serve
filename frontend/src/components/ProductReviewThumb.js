import styled from "styled-components";
import { Card } from "react-bootstrap";

const Wrapper = styled.div`
  margin-left: 1%;
  display: inline-block;
  width: 24%;
`;

const Content = styled.div`
  align-items: left;
  display: inline-block;
  margin: 1%;
  width: 95%;
`;

const ProductReviewThumb = ({ product }) => {
  return (
    <Wrapper>
      <Content>
        <Card style={{ width: "100%" }}>
          <Card.Header>{product.name}</Card.Header>
          <Card.Body>
            {product.price}
            <div style={{ float: "right" }}>qty: {product.count}</div>
          </Card.Body>
        </Card>
      </Content>
    </Wrapper>
  );
};

export default ProductReviewThumb;
