import { API_URL } from '../config'

export const LoginCall = async (details) => {
  let returnVal = null;
  
  const option = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Access-Control-Allow-Origin": "*",
    },
    mode: "cors",
    crossDomain: true,
    body: JSON.stringify(details),
  };

  await fetch(`${API_URL}/user/login`, option)
    .then((resp) => {
      if(resp.status === 200){
        return resp.json();
      }
      throw new Error("Unable to login");
    })
    .then((data) => {
      console.log(data);
      console.log("Successfully loggedin");
      returnVal = data;
    })
    .catch((e) => {
      console.log("Error")
      returnVal = { error: "Error occured in this operation" };
    });

  return returnVal;
};
