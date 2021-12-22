import React from 'react'
import {Navbar, Nav, NavDropdown} from 'react-bootstrap'
import {LinkContainer} from 'react-router-bootstrap'
import {
    Link,
    useParams
} from "react-router-dom";

const LanguageChooser = ({}) => {
    const possibleLanguages = ["de", "fr"]
    const { language } = useParams();

    const links = possibleLanguages.filter(l=>l!= language).map(l=>{
            const urlToLng = window.location.pathname.replace(language,l)
            return  <LinkContainer key={l} to={urlToLng}>
                        <NavDropdown.Item>{l.toUpperCase()}</NavDropdown.Item>
                    </LinkContainer>
        }
    )
    return <NavDropdown className="language-chooser" title={language.toUpperCase()} id="basic-nav-dropdown">
            {links}
        </NavDropdown>
}

const NavBarHeader = () => {
    const { language, dhsId } = useParams();
    //console.log("NavBarHeader, language: ", language, ", dhsId: ", dhsId, "window.location.pathname=",window.location.pathname)
    return (
        <Navbar bg="light" expand="lg">
            <Navbar.Toggle aria-controls="basic-navbar-nav" />
            <Navbar.Collapse id="basic-navbar-nav">
                <Nav className="mr-auto">
                    <LinkContainer to={"/"+language+"/articles"}>
                        <Nav.Link>Articles</Nav.Link>
                  </LinkContainer>
                  <LanguageChooser/>
                </Nav>
            </Navbar.Collapse>
        </Navbar>
    )
}

export default NavBarHeader