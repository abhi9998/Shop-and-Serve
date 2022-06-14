import React, { useContext } from "react";

import { Nav, Navbar } from "react-bootstrap";

import { useLocation } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";

const Header = (props) => {
  const { getTokenInfo } = useContext(AuthContext);

  //assigning location variable
  const location = useLocation();

  // Will be useful for deciding which tab to make active.
  const getComparator = (path) => {
    if (path.includes("/neworder")) {
      return "/neworder";
    }
    if (path.includes("changeorderstatus")) {
      return "";
    }
    if (path.substr(path.length - 1) === "/") {
      return path.substr(0, path.length - 1);
    }
    return path;
  };

  const isAdmin = () => {
    if (location.pathname.includes("admin")) {
      return true;
    } else {
      return false;
    }
  };

  const isLoggedIn = () => {
    if (getTokenInfo() === null) return false;
    return true;
  };

  const AdminHeader = () => {
    return (
      <>
        <Nav.Link href="/admin" eventKey="/admin/home">
          Home
        </Nav.Link>
        <Nav.Link href="/admin/login" eventKey="/admin/login">
          Login
        </Nav.Link>
        <Nav.Link href="/admin/addstore" eventKey="/admin/addstore">
          Add Store
        </Nav.Link>
        <Nav.Link href="/admin/addproduct" eventKey="/admin/addproduct">
          Add Product
        </Nav.Link>
      </>
    );
  };

  const UserHeader = () => {
    return (
      <>
        <Nav.Link href="/home" eventKey="/home">
          Home
        </Nav.Link>
        {isLoggedIn() ? (
          <>
            <Nav.Link href="/neworder" eventKey="/neworder">
              NewOrder
            </Nav.Link>
            <Nav.Link href="/user" eventKey="/user">
              User
            </Nav.Link>
            <Nav.Link href="/pickorder" eventKey="/pickorder">
              PickOrder
            </Nav.Link>
            <Nav.Link href="/showpickedorder" eventKey="/showpickedorder">
              Orders <span style={{ fontSize: "80%" }}>to do</span>
            </Nav.Link>
            <Nav.Link href="/showmyorder" eventKey="/showmyorder">
              Orders <span style={{ fontSize: "80%" }}>I put</span>
            </Nav.Link>
            <Nav.Link href="/showmyinvites" eventKey="/showmyinvites">
              My Pending <span style={{ fontSize: "80%" }}>Invites</span>
            </Nav.Link>
            <Nav.Link href="/inviterequest" eventKey="/inviterequest">
              Decide for <span style={{ fontSize: "80%" }}>Invites</span>
            </Nav.Link>
            <Nav.Link href="/joingroup" eventKey="/joingroup">
              JoinGroup
            </Nav.Link>
            <Nav.Link
              style={{ textAlign: "right" }}
              href="/signout"
              eventKey="/signout"
            >
              Signout
            </Nav.Link>
          </>
        ) : (
          <>
            <Nav.Link href="/signup" eventKey="/signup">
              SignUp
            </Nav.Link>

            <Nav.Link href="/login" eventKey="/login">
              LogIn
            </Nav.Link>
          </>
        )}
      </>
    );
  };

  return (
    <Navbar collapseOnSelect expand="sm" bg="dark" variant="dark">
      <Navbar.Toggle aria-controls="responsive-navbar-nav" />
      <Navbar.Collapse id="responsive-navbar-nav">
        <Nav activeKey={getComparator(location.pathname)}>
          {isAdmin() ? <AdminHeader /> : <UserHeader />}
        </Nav>
      </Navbar.Collapse>
    </Navbar>
  );
};

export default Header;
