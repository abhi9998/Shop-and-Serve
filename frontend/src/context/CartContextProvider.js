import React, { useState, createContext } from "react";

export const CartContext = createContext()

const CartContextProvider = (props) => {
  const [productsInCart, setProductsInCart] = useState([]);
  const [storeId, setStoreId] = useState([]);

  return (
    <CartContext.Provider value={[ productsInCart, setProductsInCart, storeId, setStoreId ]}>
      {props.children}
    </CartContext.Provider>
  );
};

export default CartContextProvider;