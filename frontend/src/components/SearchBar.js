import React, { useState, useEffect } from 'react';
import styled from "styled-components";

import API from '../API'

// Image
import searchIcon from '../images/search-icon.svg'

const Wrapper = styled.div`
    display: flex;
    align-items: center;
    height: 100px;
    background: #fff;
    padding: 0 20px;
`;

const Content = styled.div`
    position: relative;
    /* max-width: var(--maxWidth); */
    width: 50%;
    height: 55px;
    background: white;
    margin: 0 auto;
    color: var(--black);
    border-bottom: 1px solid black;

    img {
        position: absolute;
        left: 10px;
        top: 20px;
        width: 18px;
    }

    input {
        position: absolute;
        font-size: '2rem';
        left: 0;
        margin: 8px 0;
        padding: 0 0 0 60px;
        border: 0;
        width: 95%;
        background: transparent;
        height: 40px;
        color: black;

        :focus {
            outline: none;
        }
    }
`;

const  SearchBar = ({ stores, setStores, setStoresToDisplay }) => {
    const [state, setState] = useState('');

    useEffect(() => {
        API.getStores(setStores);
    }, [setStores])

    useEffect(() => {
        const timer = setTimeout(()=> {
        }, 500);
    
        try{
            const shouldStoreBeDisplayed = (store, state) => {
                // TODO We might want to add some more comparison.
                return store.name.toLowerCase().includes(state.toLowerCase()) 
            }
            const _stores = stores.sort((a, b) => 0.5 - Math.random())
            setStoresToDisplay(_stores.filter(store => shouldStoreBeDisplayed(store, state)))
        }catch(error){
            console.log('Search Failed with error ' + error)
        }

        return () => clearTimeout(timer)

    }, [state, stores, setStoresToDisplay])

    return (
        <Wrapper>
            <Content>
                <img src={searchIcon} alt='search-icon' />
                <input 
                    type='text'
                    placeholder='Search Store'
                    onChange={event => setState(event.currentTarget.value)}
                    value={state}
                />
            </Content>
        </Wrapper>
    )
}

export default SearchBar;
