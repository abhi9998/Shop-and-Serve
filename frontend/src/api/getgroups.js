export const GetGroupDetailsForJoining = async (token) => {
  let returnVal = null;

  const option = {
    method: "GET",
    headers: {
      Authorization: `Token ${token}`,
    },
    //mode: "cors",
    crossDomain: true,
  };

  await fetch(`http://localhost:8000/user/searchGroup/`, option)
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
