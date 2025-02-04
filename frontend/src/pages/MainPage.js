import React from "react";
import photo from "../assets/main_page.png";
import logo from "../assets/main_logo.png";
import "../style/MainPage.css";
import "../style/colors.css";
const MainPage = () => {
  return (
    <>
      <div className="magnet">
        <div className="magnet-content">
          <div className="magnet-image-container">
            <img src={photo} alt="Human Resource and Company Harmony" />
          </div>
          <div className="content">
            <div className="title">
              <div className="title-line line1">
                <span className="child">H</span>uman&nbsp;{" "}
                <span className="child">R</span>
                esource와
              </div>
              <div className="title-line line2">
                <div className="company">
                  Compan
                  <span className="child">y</span>의 조화를 이루는
                </div>
                <img src={logo} alt="Hrmony Logo" className="hrmony-logo" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};
export default MainPage;
