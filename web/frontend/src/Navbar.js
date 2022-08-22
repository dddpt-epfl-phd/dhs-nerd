import React from 'react'
import {Navbar, Nav, NavDropdown, Alert} from 'react-bootstrap'
import {LinkContainer} from 'react-router-bootstrap'
import {
    Link,
    useParams
} from "react-router-dom";

import {ArticleSearch} from "./ArticleSearch"

const LanguageChooser = ({}) => {
    const possibleLanguages = ["de", "fr", "it"]
    const { language } = useParams();

    const links = possibleLanguages.filter(l=>l!= language).map(l=>{
            const urlToLng = (window.location+"").split("#")[1].replace(language,l)
            return  <LinkContainer key={l} to={urlToLng}>
                        <NavDropdown.Item>{l.toUpperCase()}</NavDropdown.Item>
                    </LinkContainer>
        }
    )
    return <NavDropdown className="language-chooser" title={language.toUpperCase()} id="basic-nav-dropdown">
            {links}
            <Alert variant="info">the chosen language only affects articles contents.</Alert>
        </NavDropdown>
}

const NavBarHeader = () => {
    const { language, dhsId } = useParams();
    //console.log("NavBarHeader, language: ", language, ", dhsId: ", dhsId, "window.location.pathname=",window.location.pathname)
    return (
        <Navbar id="ldhs-navbar" expand="md" className="justify-content-center">
            <Navbar.Toggle aria-controls="ldhs-collapsible-navbar" />
            <Navbar.Collapse id="ldhs-collapsible-navbar">
                <Nav className="justify-content-center">
                    <LinkContainer to={"/"+language+"/articles"}>
                        <Nav.Link>Home</Nav.Link>
                  </LinkContainer>
                    <LinkContainer to={"/"+language+"/about"}>
                        <Nav.Link>About</Nav.Link>
                  </LinkContainer>
                  <LanguageChooser/>
                </Nav>
            </Navbar.Collapse>

            <div id="search-wrapper">
                <ArticleSearch/>
            </div>
        </Navbar>
    )
}

export default NavBarHeader