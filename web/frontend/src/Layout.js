import React from "react";
import {Container, Row, Col} from "react-bootstrap"
import NavBarHeader from "./Navbar.js"

import "./style.scss"

export function CenteredLayout({children}){

    return (
      <div className="main">
        <NavBarHeader/>
        <Container className="centered-article-container">
          <Row className="justify-content-md-center">
            <Col lg="7" className="justify-content-md-center centered-article-content">
                {children}
            </Col>
          </Row>
        </Container>
      </div>
    );
  }