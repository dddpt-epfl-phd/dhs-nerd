import React from "react";

export const CopyrightFooter = (originalPageLink="")=> {
    return (
        <div id="copyright-footer">
            The content of all HDS articles presented on this website are the work of their respective author from the original HDS. {[originalPageLink]} <br/>
            This work is available under the <a href="https://creativecommons.org/licenses/by-sa/4.0/" target="_blank">Creative Common Attribution-ShareAlike 4.0 International License (CC BY-SA 4.0) </a>
        </div>
    )
}