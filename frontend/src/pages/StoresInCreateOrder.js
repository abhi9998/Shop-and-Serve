import React, { useContext, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import styled from "styled-components";

import SearchBar from "../components/SearchBar";
import ThumbInStoreInCreateOrder from "../components/ThumbInStoresInCreateOrder";
import { AuthContext } from "../context/AuthContext";

const StoreContainer = styled.div`
  width: 40%;
  align-items: left;
  display: block;
  margin-left: auto;
  margin-right: auto;
`;

const NoStoreFound = () => {
  return (
    <>
      No Store Found...
    </>
  )
}

const StoresInCreateOrder = () => {
  const [stores, setStores] = useState([]);
  const [storesToDisplay, setStoresToDisplay] = useState([]);
  const navigate = useNavigate();
  const { getTokenInfo } = useContext(AuthContext);
  useEffect(async () => {
    if (getTokenInfo() === null) navigate("/login");
  }, [getTokenInfo, navigate]);

  return (
    <div>
      <SearchBar
        stores={stores}
        setStores={setStores}
        setStoresToDisplay={setStoresToDisplay}
      />
      <StoreContainer>
        {storesToDisplay.length === 0 ? <NoStoreFound/>: storesToDisplay.map((store) => (
          <ThumbInStoreInCreateOrder key={store.id} store={store} />
        ))}
      </StoreContainer>
    </div>
  );
};

export default StoresInCreateOrder;
