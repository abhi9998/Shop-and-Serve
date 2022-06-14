export const GetPickedOrder = async (id, token) => {
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

  await fetch(`http://localhost:8000/api/order/acceptor/${id}`, option)
    .then((resp) => {
      return resp.json();
    })
    .then((data) => {
      //  console.log(data);
      returnVal = data;
    })
    .catch((e) => {
      //  console.log(e.message);
      console.log("error");
      returnVal = { error: "Error occured in this operation" };
    });

  let statusWiseOrder = {};

  for (let i = 0; i < returnVal.length; i++) {
    let status = returnVal[i]["status"];

    console.log(statusWiseOrder[status]);
    if (statusWiseOrder[status] === undefined) {
      statusWiseOrder[status] = [];
    }
    statusWiseOrder[status] = [...statusWiseOrder[status], returnVal[i]];
  }
  let statusWiseOrderArray = [];
  let statusOfOrders = [];

  for (const [key, value] of Object.entries(statusWiseOrder)) {
    const obj = {};
    obj[key] = value;
    statusWiseOrderArray.push(obj);
    //console.log(JSON.stringify(obj));
    statusOfOrders.push(key);
  }

  return [statusOfOrders, statusWiseOrderArray];
};
