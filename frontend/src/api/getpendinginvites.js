export const GetMyPendingInvites = async (id, token) => {
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

  await fetch(`http://localhost:8000/api/invite/user/${id}`, option)
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
