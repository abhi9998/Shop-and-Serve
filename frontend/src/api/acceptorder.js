import { toast } from "react-toastify";

export const AcceptOrder = async (body, token) => {
  let returnVal = null;
  //console.log("calling the function api for getting order of group id");
  const option = {
    method: "POST",
    headers: {
      Authorization: `Token ${token}`,
      "Content-Type": "application/json",
    },
    //mode: "cors",
    crossDomain: true,
    body: JSON.stringify(body),
  };

  await fetch(`http://localhost:8000/api/order/accept`, option)
    .then((resp) => {
      console.log("Response", resp.status);
      if (resp.status == 403) {
        toast("Forbidden cannot accept your own order");
        throw Error("Forbidden cannot accept your order");
      }
      return resp.json();
    })
    .then((data) => {
      //console.log(data);
      returnVal = data;
    })
    .catch((e) => {
      //console.log(e.message);
      console.log("error");
      returnVal = { error: "Error occured in this operation" };
    });

  return returnVal;
};
