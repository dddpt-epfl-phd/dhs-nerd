import React from "react";
import {Container, Row, Col} from "react-bootstrap"

export function CenteredArticleContainer({children}){

    return (
      <Container className="centered-article-container">
        <Row className="justify-content-md-center">
          <Col lg="7" className="justify-content-md-center centered-article-content">
              {children}
          </Col>
        </Row>
      </Container>
    );
  }