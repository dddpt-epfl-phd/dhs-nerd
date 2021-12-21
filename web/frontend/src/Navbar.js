import React from "react";

import {
    Link
} from "react-router-dom";

import DropdownMenu from "./dropdownMenu/DropdownMenu.js";

import "./Navbar.scss";

const Navbar = ()=>(
<nav className="navbar">
    <ul className="navbar-ul">
        <li className="nav-li-nogrow">
            <Link className="nav-link" to="/">Home</Link>
        </li>
        <li className="nav-li-grow">
        </li>
        <li className="nav-li-nogrow">
            <DropdownMenu
                title={<Link className="nav-link" to="/docs">Docs</Link>}
            >
                <Link className="nav-link" to="/docs/catastici" key="catastici">Catastici</Link>
                <Link className="nav-link" to="/docs/cadaster"  key="cadaster">Cadaster</Link>
                <Link className="nav-link" to="/docs/vectorization" key="vectorization">Vectorization</Link>
            </DropdownMenu>
        </li>
        <li className="nav-li-nogrow">
            <Link className="nav-link" to="/about">About</Link>
        </li>
    </ul>
</nav>
)


export default Navbar;