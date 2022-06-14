import { API_URL } from "./config";

const getAuthToken = () => {
  let token = JSON.parse(localStorage.getItem("userToken"));
  if (token === null) {
    return "Token null";
  } else {
    return "Token " + token.token;
  }
  // return "Token " + .token
};

const defaultPOSTConfig = {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    Authorization: getAuthToken(),
  },
};

const defaultGETConfig = {
  method: "GET",
  headers: {
    "Content-Type": "application/json",
    Authorization: getAuthToken(),
  },
};

const apiSettings = {
  // POST call
  signUp: async (data) => {
    const endpoint = `${API_URL}/user/create`;
    const response = await await fetch(endpoint, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    if (response.ok === true) {
      return response.json();
    } else {
      return false;
    }
  },
  // GET call
  getStores: async (setStores) => {
    const endpoint = `${API_URL}/api/store/info?status=active`;
    const stores = await (
      await fetch(endpoint, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: getAuthToken(),
        },
      })
    ).json();

    setStores(stores);
  },
  // GET call
  getProductsOfStore: async (storeId, setProducts) => {
    const endpoint = `${API_URL}/api/product/info/store/${storeId}?status=active`;

    const products = await (
      await fetch(endpoint, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: getAuthToken(),
        },
      })
    ).json();

    setProducts(products);
  },
  // GET call
  getStoreInfo: async (storeId, setStoreInfo) => {
    const endpoint = `${API_URL}/api/store/info/${storeId}`;

    const info = await (
      await fetch(endpoint, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: getAuthToken(),
        },
      })
    ).json();

    setStoreInfo(info);
  },
  // POST call
  addStore: async (data) => {
    const endpoint = `${API_URL}/api/store/`;

    const response = await (
      await fetch(endpoint, {
        ...defaultPOSTConfig,
        body: JSON.stringify(data),
      })
    ).json();
    return response;
  },
  // POST call
  addProduct: async (data) => {
    const endpoint = `${API_URL}/api/product/`;

    const response = await (
      await fetch(endpoint, {
        ...defaultPOSTConfig,
        body: JSON.stringify(data),
      })
    ).json();
    return response;
  },
  // GET call
  getUserInfo: async (setUserInfo) => {
    const endpoint = `${API_URL}/user/myprofile`;

    const response = await (
      await fetch(endpoint, {
        ...defaultGETConfig,
      })
    ).json();

    setUserInfo(response);
  },
  updateUserProfile: async (data) => {
    const endpoint = `${API_URL}/user/myprofile`;
    const response = await await fetch(endpoint, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
        Authorization: getAuthToken(),
      },
      body: JSON.stringify(data),
    });
    if (response.ok === true) {
      return response.json();
    } else {
      return false;
    }
  },
  getGroupNames: async (setGroups) => {
    const endpoint = `${API_URL}/user/mygroups/`;
    const response = await await fetch(endpoint, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: getAuthToken(),
      },
    });
    if (response.ok === true) {
      let data = await response.json();
      setGroups(data);
      return true;
    } else {
      return false;
    }
  },
  placeOrder: async (data) => {
    const endpoint = `${API_URL}/api/order/`;
    const response = await await fetch(endpoint, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: getAuthToken(),
      },
      body: JSON.stringify(data),
    });

    if (response.ok === true) {
      return true;
    } else {
      return false;
    }
  },
};

export default apiSettings;
