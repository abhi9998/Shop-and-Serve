import { API_URL } from '../config'

export const ChangeState = async (body, endpoint, token) => {
  let returnVal = null;
  //console.log("calling the function api for getting order of group id");
  console.log(token)
  console.log(endpoint)
  const option = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Token ${token}`,
    },
    crossDomain: true,
    body: JSON.stringify(body),
  };
  console.log("body", JSON.stringify(body), endpoint);

  await fetch(`${API_URL}${endpoint}`, option)
    .then((resp) => {
      return resp.json();
    })
    .then((data) => {
      console.log(data);
      returnVal = data;
    })
    .catch((e) => {
      console.log(e.message);
      console.log("error");
      returnVal = { error: "Error occured in this operation" };
    });

  return returnVal;
};
