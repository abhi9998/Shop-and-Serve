import React from "react";


const Footer = () => {
    let footer_style = {
        display: 'block',
<<<<<<< HEAD
        position:"fixed",
        bottom:"0",
        width:"100%",
        textAlign: "center",
        margin: "0",
        background: "#ccc",
        borderTop: "1px solid #555",
=======
        position:"fixed", 
        bottom:"0", 
        width:"100%", 
        textAlign: "center",
        margin: "0",
        background: "#aaa",
        fontWeight: "300",
        fontSize: "10px"
>>>>>>> frontend
    }

    return (
        <footer style={footer_style}>
            <span>@Copyright-Notes</span>
        </footer>
    )
}

export default Footer;