export const GetMyOrders = async (id, token) => {
  let returnVal = null;

  const option = {
    method: "GET",
    headers: {
      Authorization: `Token ${token}`,
    },
  };

  await fetch(`http://localhost:8000/api/order/placer/${id}`, option)
    .then((resp) => {
      return resp.json();
    })
    .then((data) => {
      //console.log(data);
      returnVal = data;
    })
    .catch((e) => {
      console.log(e.message);
      //console.log("error");
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
    //    console.log(JSON.stringify(obj));
    statusOfOrders.push(key);
  }
  //  console.log("heeee", JSON.stringify(statusWiseOrderArray));
  return [statusOfOrders, statusWiseOrderArray];
};
