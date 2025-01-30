import React from "react";
import "../style/InfoCard.css";
import "../style/FreelancerDetailPage.css";

const FreelancerSuggest = () => {
  const projectList = [
    {
      projectId: 101,
      projectName: "AI 기반 추천 시스템 개발",
      duration: 6,
      budget: 5000000,
      workType: 1,
      contractType: 0,
      status: 1,
      registerDate: "20250127",
      categoryName: "IT•정보통신업",
      skillIdList: [1, 2, 3],
      skillNameList: ["Python", "Machine Learning", "Deep Learning"],
      locationName: "서울시 강남구",
    },
    {
      projectId: 102,
      projectName: "AI 기반 추천 시스템 개발2",
      duration: 6,
      budget: 5000000,
      workType: 1,
      contractType: 0,
      status: 1,
      registerDate: "20250126",
      categoryName: "IT•정보통신업",
      skillIdList: [1, 2, 3],
      skillNameList: ["Python", "Machine Learning", "Deep Learning"],
      locationName: "서울시 강남구",
    },
  ];

  return (
    <div className="suggest-page container-fluid">
      <div className="container-fluid detail-card scrollable">
        <div className="row">
          {projectList.map((project, index) => (
            <div
              className="info-card suggest-project col-md-12"
              style={{ minWidth: 0, width: "800px" }}
            ></div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default FreelancerSuggest;
