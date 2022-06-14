export const GetGroupCall = async (id, token) => {
  let returnVal = null;

  const option = {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      "Access-Control-Allow-Origin": "*",
      Authorization: `Token ${token}`,
    },
    crossDomain: true,
  };

  await fetch(`http://localhost:8000/user/mygroups/`, option)
    .then((resp) => {
      return resp.json();
    })
    .then((data) => {
      // console.log("here i am printing data", data);

      let resp = [];
      data.map((group) => {
        let obj = {};
        obj["id"] = group.groupid.id;
        obj["name"] = group.groupid.name;
        resp.push(obj);
      });

      returnVal = resp;
    })
    .catch((e) => {
      //console.log(e.message);
      console.log("error");
      returnVal = { error: "Error occured in this operation" };
    });

  console.log("returning", returnVal);
  return returnVal;
};
