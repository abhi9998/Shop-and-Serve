import React, { useState, useEffect, useContext } from "react";
import { FloatingLabel } from "react-bootstrap";
import { useNavigate } from "react-router-dom";
import { GetMyPendingInvites } from "../api/getpendinginvites";

import { AuthContext } from "../context/AuthContext";

const ShowMyPendingInvites = () => {
  const navigate = useNavigate();
  const { storeTokenInfo, getTokenInfo } = useContext(AuthContext);

  const [myInvites, setMyInvites] = useState([]);

  useEffect(async () => {
    if (getTokenInfo() === null) navigate("/login");
    // console.log("going to fetch groups of user");
    const pendingInvites = await GetMyPendingInvites(
      getTokenInfo().id,
      getTokenInfo().token
    );

    setMyInvites(pendingInvites);
  }, [getTokenInfo, navigate]);

  return (
    <div>
      <ul>
        {myInvites.map((invite) => {
          console.log(invite.id);
          return (
            // <li key={invite.id} value={invite.id}>
            //   {JSON.stringify(invite)}
            // </li>
            <div
              key={invite.id}
              style={{
                borderRadius: "4px solid black",
                boxShadow:
                  "0 2px 4px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)",
                width: "60%",
                backgroundColor: "#e9ecef",
                marginTop: "1%",
              }}
            >
              <FloatingLabel
                style={{
                  marginTop: "3%",
                }}
                disabled
              >
                <div disabled>Group Name: {invite.name}</div>
                <div disabled>Status: {invite.status}</div>
                <div disabled>Created At: {invite.createAt.substr(0, 10)}</div>
              </FloatingLabel>
            </div>
          );
        })}
      </ul>
    </div>
  );
};

export default ShowMyPendingInvites;
