import React from "react";

export const CopyrightFooter = ({children=[]})=> {
    console.log("CopyrightFooter children: ", children)
    return (
        <div id="copyright-footer">
            The content of all HDS articles presented on this website are the work of their respective author from the original HDS. {children}
            This work is available under the Creative Common Attribution-ShareAlike 4.0 International License (<a href="https://creativecommons.org/licenses/by-sa/4.0/" target="_blank">CC BY-SA 4.0</a>)
        </div>
    )
}