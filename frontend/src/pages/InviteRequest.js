import React, { useState, useEffect, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { GetMyGroupInvites } from "../api/getgroupinvites";
import { InviteDecision } from "../api/postinvitedecision";
import { AuthContext } from "../context/AuthContext";
import { toast } from "react-toastify";
import { Button, FloatingLabel, Form } from "react-bootstrap";

toast.configure();

const InviteRequest = () => {
  const navigate = useNavigate();
  const { storeTokenInfo, getTokenInfo } = useContext(AuthContext);

  const [showPendingInvites, setShowPendingInvites] = useState([]);
  const [groupPendingList, setGroupPendingList] = useState([]);
  const [groupArray, setGroupArray] = useState([]);

  useEffect(async () => {
    if (getTokenInfo() === null) navigate("/login");
    // console.log("going to fetch groups of user");
    const [groupArray, groupPendingList] = await GetMyGroupInvites(
      getTokenInfo().id,
      getTokenInfo().token
    );
    console.log("invite groups ", JSON.stringify(groupArray));
    console.log("pending list groups ", JSON.stringify(groupPendingList));

    setGroupPendingList(groupPendingList);
    setGroupArray(groupArray);
  }, [getTokenInfo, navigate]);

  const handleGroupSelect = async (e) => {
    // console.log(e.target.value, "this group selected");

    setShowPendingInvites([]);
    // console.log("here showing grouppending list", groupPendingList.length);
    for (let i = 0; i < groupPendingList.length; i++) {
      if (groupArray[i]["groupname"] === e.target.value) {
        setShowPendingInvites(groupPendingList[i]);
        return;
      }
    }
  };

  const handleDecision = async (e, invite) => {
    // console.log(e.target.value, "this is pressed");
    // console.log("data sent in ", invite);

    let body = {};
    body = {
      ...body,
      userid: invite["userid"],
      groupid: invite["groupid"],
      status: e.target.value,
    };
    let responseData = {};
    responseData = await InviteDecision(
      body,
      invite["id"],
      getTokenInfo().token
    );

    if (responseData["error"] === undefined) {
      toast("invite decision updated");
      for (let i = 0; i < groupArray.length; i++) {
        console.log(groupArray[i]["groupid"]["id"] === invite["groupid"]);
        console.log(
          "Hereeeeeee",
          groupArray[i]["groupid"]["id"],
          invite["groupid"]
        );
        if (groupArray[i]["groupid"]["id"] == invite["groupid"]) {
          if (groupPendingList[i].length === 1) {
            groupPendingList[i] = [];
            setGroupPendingList(groupPendingList);
            setShowPendingInvites([]);
            // console.log("invite groups ", groupArray);
            // console.log("pending list groups ", groupPendingList);
            break;
          } else {
            let ans = [];
            for (let j = 0; j < groupPendingList[i].length; j++) {
              if (groupPendingList[i][j]["id"] != invite["id"]) {
                ans.push(groupPendingList[i][j]);
              }
            }
            groupPendingList[i] = ans;

            setGroupPendingList(groupPendingList);
            setShowPendingInvites(groupPendingList[i]);
          }
        }
      }
    }
  };

  return (
    <div className="invite-requests">
      {/* <select onChange={handleGroupSelect}>
        <option key={-1}>select group</option>
        {groupArray.map((group) => {
          return (
            <option key={group.groupname} value={group.groupname}>
              {group["groupname"]}
            </option>
          );
        })}
      </select> */}

      <Form
        style={{
          width: "50%",
          marginLeft: "auto",
          marginRight: "auto",
          textAlign: "center",
          paddingTop: "2%",
        }}
      >
        <Form.Group className="mb-3">
          <Form.Select onChange={handleGroupSelect}>
            <option key={-1}> Select Status Of Order </option>
            {groupArray.map((group) => {
              return (
                <option key={group.groupname} value={group.groupname}>
                  {group["groupname"]}
                </option>
              );
            })}
          </Form.Select>
        </Form.Group>
      </Form>

      {showPendingInvites.map((invite) => {
        return (
          <div key={invite.id}>
            <div
              key={invite.id}
              style={{
                borderRadius: "4px solid black",
                boxShadow:
                  "0 2px 4px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)",
                width: "30%",
                backgroundColor: "#e9ecef",
                marginTop: "1%",
                float: "center",
                marginLeft: "auto",
                marginRight: "auto",
                padding: "1%",
              }}
            >
              <FloatingLabel
                style={{
                  marginTop: "3%",
                }}
                disabled
              >
                <div disabled>Requestor Name: {invite.name}</div>
                <div disabled>Address: {invite.address}</div>
                <div disabled>City: {invite.city}</div>
                <div disabled>Mobile: {invite.mobile}</div>
                <div disabled>Created At: {invite.createAt.substr(0, 10)}</div>
                <div disabled>Email: {invite.email}</div>
              </FloatingLabel>
              <Button
                style={{ marginTop: "1%" }}
                onClick={(e) => handleDecision(e, invite)}
                key="accept"
                value="accepted"
              >
                Accept
              </Button>
              <Button
                style={{ marginTop: "1%", marginLeft: "3%" }}
                onClick={(e) => handleDecision(e, invite)}
                key="reject"
                value="rejected"
              >
                Reject
              </Button>
            </div>

            {/* </div> */}
          </div>
        );
      })}
    </div>
  );
};

export default InviteRequest;
