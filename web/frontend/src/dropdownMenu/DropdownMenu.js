import React from 'react';
import './DropdownMenu.scss';


export default function DropdownMenu({
    title="",
    children=[]
}){
    
    return (
        <div className="dropdown">
            <div className="dropdown-title">
                {title}
            </div>
            <ul className="dropdown-ul">
                {children.map(c=>(
                  <li key={c.key}>{c}</li>
                ))}
            </ul>
        </div>
    )
}