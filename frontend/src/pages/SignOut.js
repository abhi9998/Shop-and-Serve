import { useContext, useEffect } from "react"
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";
import {toast} from 'react-toastify';

toast.configure()

const SignOut = () => {
    const { deleteTokenInfo } = useContext(AuthContext);
    const navigate = useNavigate();

    useEffect( () => {
      deleteTokenInfo()
      toast('Logged out Successfully.')
      navigate('/login')
    }, [deleteTokenInfo, navigate])

    return (
        <></>
    )
}

export default SignOut;