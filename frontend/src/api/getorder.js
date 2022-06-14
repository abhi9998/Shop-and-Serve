export const GetOrderCall = async (id, token) => {
  let returnVal = null;
  //console.log("calling the function api for getting order of group id");
  const option = {
    method: "GET",
    headers: {
      Authorization: `Token ${token}`,
    },
    //mode: "cors",
    crossDomain: true,
  };

  await fetch(
    `http://localhost:8000/api/order/group/${id}?status=pending`,
    option
  )
    .then((resp) => {
      return resp.json();
    })
    .then((data) => {
      console.log(data);
      returnVal = data;
    })
    .catch((e) => {
      //console.log(e.message);
      console.log("error");
      returnVal = { error: "Error occured in this operation" };
    });

  let storeWiseOrder = {};

  for (let i = 0; i < returnVal.length; i++) {
    let storename = returnVal[i]["storename"];

    //console.log(storeWiseOrder[storename]);
    if (storeWiseOrder[storename] === undefined) {
      storeWiseOrder[storename] = [];
    }
    storeWiseOrder[storename] = [...storeWiseOrder[storename], returnVal[i]];
  }
  let storeWiseOrderArray = [];
  let storeName = [];

  for (const [key, value] of Object.entries(storeWiseOrder)) {
    // console.log("key is ", key);
    const obj = {};
    obj[key] = value;
    storeWiseOrderArray.push(obj);
    storeName.push(key);
  }
  return [storeName, storeWiseOrderArray];
};
