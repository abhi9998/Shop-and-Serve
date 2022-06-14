import {
  BrowserRouter as Router,
  Route,
  Routes,
  Navigate,
} from "react-router-dom";

import Header from "./components/Header";
import Footer from "./components/Footer";
import Home from "./pages/Home";
import LogIn from "./pages/LogIn";
import ProductsInCreateOrder from "./pages/ProductsInCreateOrder";
import ReviewInCreateOrder from "./pages/ReviewInCreateOrder";
import SignUp from "./pages/SignUp";
import SignOut from "./pages/SignOut";
import StoresInCreateOrder from "./pages/StoresInCreateOrder";
import ShowOrders from "./pages/ShowOrders";
import DetailOrder from "./pages/DetailOrder";
import PickedOrder from "./pages/PickedOrder";
import ChangeOrderStatus from "./pages/ChangeOrderStatus";
import MyOrder from "./pages/MyOrder";
import NotFound from "./pages/NotFound";
import AdminLogin from "./pages/AdminLogin";
import AdminHome from "./pages/AdminHome";
import AddProduct from "./pages/AddProduct";
import AddStore from "./pages/AddStore";
import User from "./pages/User";
import GroupSelectNewOrder from "./pages/GroupSelectNewOrder";
import ShowMyPendingInvites from "./pages/ShowMyPendingInvites";
import InviteRequest from "./pages/InviteRequest";
import { toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import JoinGroup from "./pages/JoinGroup";

toast.configure();

const App = () => {
  return (
    <Router>
      <Header />
      <Routes>
        <Route path="/signup" element={<SignUp />} />
        <Route path="/signout" element={<SignOut />} />
        <Route path="/login" element={<LogIn />} />

        <Route path="/" element={<Navigate replace to="/home" />} />
        <Route path="/home" element={<Home />} />

        <Route
          path="/neworder"
          element={<Navigate replace to="/neworder/stores" />}
        />
        <Route path="/neworder/stores" element={<StoresInCreateOrder />} />

        <Route
          path="/neworder/stores/:storeId/products"
          element={<ProductsInCreateOrder />}
        />

        <Route
          path="/neworder/stores/:storeId/products/review"
          element={<ReviewInCreateOrder />}
        />
        <Route path="/neworder/groups" element={<GroupSelectNewOrder />} />

        <Route path="/admin" element={<Navigate replace to="/admin/home" />} />
        <Route path="/admin/login" element={<AdminLogin />} />
        <Route path="/admin/home" element={<AdminHome />} />
        <Route path="/admin/addproduct" element={<AddProduct />} />
        <Route path="/admin/addstore" element={<AddStore />} />

        <Route path="/user" element={<User />} />

        <Route path="/pickorder" element={<ShowOrders />} />
        <Route path="/detailorder" element={<DetailOrder />} />
        <Route path="/showpickedorder" element={<PickedOrder />} />
        <Route path="/changeorderstatus" element={<ChangeOrderStatus />} />
        <Route path="/showmyorder" element={<MyOrder />} />
        <Route path="/showmyinvites" element={<ShowMyPendingInvites />} />
        <Route path="/inviterequest" element={<InviteRequest />} />
        <Route path="/joingroup" element={<JoinGroup />} />
        <Route path="/*" element={<NotFound />} />
      </Routes>

      <Footer />
    </Router>
  );
};

export default App;
