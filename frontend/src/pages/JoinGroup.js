import React, { useState, useEffect } from "react";
import { useContext } from "react";
import { Button, FloatingLabel } from "react-bootstrap";
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
import { GetGroupDetailsForJoining } from "../api/getgroups";
import { SendJoinRequest } from "../api/sendjoinrequest";

import { AuthContext } from "../context/AuthContext";

const JoinGroup = () => {
  const navigate = useNavigate();
  const { storeTokenInfo, getTokenInfo } = useContext(AuthContext);

  const [groupDetails, setGroupDetails] = useState([]);

  useEffect(async () => {
    if (getTokenInfo() === null) navigate("/login");

    const groupData = await GetGroupDetailsForJoining(getTokenInfo().token);

    setGroupDetails(groupData);
  }, [getTokenInfo, navigate]);

  const handleJoin = async (e, group) => {
    let displayText = "";
    if (group.type === "private") {
      displayText = "Invite Sent";
    } else {
      displayText = "Approved";
    }

    const resp = await SendJoinRequest(group.id, getTokenInfo().token);
    if (resp["error"] === undefined) {
      toast(displayText);
      let newDetails = [];
      for (let i = 0; i < groupDetails.length; i++) {
        console.log("hahaha", groupDetails[i].id == group.id);
        console.log("hahaha", groupDetails[i].id, group.id);

        if (groupDetails[i].id == group.id) {
          console.log(groupDetails[i].type);
          if (groupDetails[i].type === "private") {
            groupDetails[i].status = "Pending";
          } else groupDetails[i].status = "Approved";

          console.log(JSON.stringify(newDetails), "daaddd");
        }
        newDetails.push(groupDetails[i]);
      }
      console.log("before set", JSON.stringify(newDetails));
      setGroupDetails(newDetails);
      console.log("after set", JSON.stringify(newDetails));
    }
  };
  return (
    <div>
      <ul>
        {groupDetails.map((group) => {
          console.log(group.id);
          return (
            <>
              <div
                key={group.id}
                style={{
                  borderRadius: "4px solid black",
                  boxShadow:
                    "0 2px 4px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)",
                  width: "40%",
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
                  <div disabled>Group Name: {group.name}</div>
                  <div disabled>Type: {group.type}</div>
                  <div disabled>
                    Created At: {group.createdat.substr(0, 10)}
                  </div>
                  <div disabled>{group.city}</div>
                </FloatingLabel>
                <div style={{ marginTop: "2.5%" }}></div>
                {group.status === "Approved" ? (
                  <Button style={{ backgroundColor: "green" }} disabled>
                    Joined
                  </Button>
                ) : (
                  <>
                    {group.status === "Pending" ? (
                      <Button style={{ backgroundColor: "lightblue" }} disabled>
                        Invite Sent
                      </Button>
                    ) : (
                      <Button onClick={(e) => handleJoin(e, group)}>
                        Join the Group
                      </Button>
                    )}
                  </>
                )}
              </div>
            </>
          );
        })}
      </ul>
    </div>
  );
};

export default JoinGroup;
