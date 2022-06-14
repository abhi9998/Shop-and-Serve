import React from "react";
import { useContext } from "react";
import { useEffect } from "react";
import { useState } from "react";
import { FloatingLabel, Form } from "react-bootstrap";
import { GetStats } from "../api/getstats";
import { AuthContext } from "../context/AuthContext";

const Home = () => {
  const { getTokenInfo } = useContext(AuthContext);
  const [stats, setStats] = useState([]);
  const [okdata, setOkData] = useState(false);
  useEffect(async () => {
    setOkData(false);
    let resp = await GetStats(getTokenInfo().id, getTokenInfo().token);
    if (resp["error"] == undefined) {
      setStats(resp);
      setOkData(true);
    }
  }, []);

  return okdata ? (
    <div style={{ textAlign: "center", marginTop: "1%" }}>
      <div style={{ fontSize: "30px" }}>
        <div>Order Completed</div>
        <div style={{ fontSize: "60px" }}>{stats["ordercompleted"]}</div>
      </div>
      <br />
      <div style={{ fontSize: "30px" }}>
        <div>Order Placed</div>
        <div style={{ fontSize: "60px" }}>{stats["orderplaced"]}</div>
      </div>
      <br />
      <div style={{ fontSize: "30px" }}>
        <div>Tip Given</div>
        <div style={{ fontSize: "60px" }}> $ {stats["tipgiven"]}</div>
      </div>
      <br />
      <div style={{ fontSize: "30px" }}>
        <div>Tip Received</div>
        <div style={{ fontSize: "60px" }}> $ {stats["tipreceived"]}</div>
      </div>
      <br />
      <div style={{ fontSize: "30px" }}>
        <div>Wallet Amount</div>
        <div style={{ fontSize: "60px" }}>$ {stats["walletamount"]}</div>
      </div>
    </div>
  ) : (
    <></>
  );
};

export default Home;
