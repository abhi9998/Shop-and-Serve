import React, { useEffect, useState } from "react";
import { Button } from "react-bootstrap";

import { useNavigate } from "react-router-dom";

const AdminHome = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(true); // TODO
  const navigate = useNavigate();

  useEffect(() => {
    if (!isLoggedIn) {
      navigate("/admin/login");
    }
  });

  const handleAddProduct = () => {
    navigate("/admin/addproduct");
  };

  const handleAddStore = () => {
    navigate("/admin/addstore");
  };

  const style1 = {
    height: "8%",
    width: "100%",
    align: "center",
    margin: "10% 10%",
    backgroundColor: "#706b6b",
    border: "0px"
  };

  const style2 = {
    height: "8%",
    width: "100%",
    align: "center",
    margin: "10% 10%",
    backgroundColor: "#706b6b",
    border: "0px"
  };

  return (
    <div style={{ height: "100vh", alignItems: "center" }}>
      <div className="d-flex" style={{ height: "100vh" }}>
        <Button
          onClick={handleAddProduct}
          style={style1}
          variant="outline-dark"
        >
          Add Product
        </Button>
        <div
          className="vr"
          style={{
            marginBottom: "auto",
            marginTop: "4%",
            align: "center",
            height: "70%",
            border: "1.5px solid black",
          }}
        ></div>

        <Button onClick={handleAddStore} style={style2} variant="outline-dark">
          Add Store
        </Button>
      </div>
    </div>
  );
};

export default AdminHome;
