export const SendJoinRequest = async (groupid, token) => {
  let returnVal = null;
  //console.log("calling the function api for getting order of group id");
  const option = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Token ${token}`,
    },
    //mode: "cors",
    crossDomain: true,
    body: JSON.stringify({ groupid }),
  };

  console.log(JSON.stringify(option));
  await fetch(`http://localhost:8000/user/joinGroup/`, option)
    .then((resp) => {
      if (resp.ok) return resp.json();
      else throw Error("Already sent requst");
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
