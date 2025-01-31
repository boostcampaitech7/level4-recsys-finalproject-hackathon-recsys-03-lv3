import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import ProjectSkillTag from "../components/ProjectSkillTag";
import "../style/InfoCard.css";
import "../style/FreelancerDetailPage.css";

const FreelancerSuggest = () => {
  const [selectedProject, setSelectedProject] = useState(null); // 선택된 프로젝트 ID 저장
  const navigate = useNavigate();

  const projectList = [
    {
      projectId: 101,
      projectName: "기업 - 프리랜서 매칭 플랫폼 프론트엔드 개발",
      duration: 30,
      budget: 3000000,
      workType: "개발",
      contractType: 0,
      status: 1,
      registerDate: "20250212",
      categoryName: "IT•정보통신업",
      skillIdList: [1, 2, 3],
      skillNameList: ["스킬 1", "스킬 2", "스킬 3"],
      locationName: "서울시 종로구",
    },
    {
      projectId: 102,
      projectName: "기업 - 프리랜서 매칭 플랫폼 프론트엔드 개발",
      duration: 30,
      budget: 3000000,
      workType: "개발",
      contractType: 0,
      status: 1,
      registerDate: "20250212",
      categoryName: "IT•정보통신업",
      skillIdList: [1, 2, 3],
      skillNameList: ["스킬 1", "스킬 2", "스킬 3"],
      locationName: "서울시 종로구",
    },
  ];

  const handleCardClick = (projectId) => {
    setSelectedProject(projectId); // 클릭한 카드 선택 (기존 선택된 카드 해제)
  };

  const handleSuggestClick = () => {
    if (selectedProject) {
      alert("제안이 완료되었습니다.");
      navigate("/myproject");
    }
  };

  const formatDate = (dateString) => {
    return dateString
      .replace(/(\d{4})(\d{2})(\d{2})/, "$1년 $2월 $3일")
      .replace(/\b0(\d)/g, "$1");
  };

  return (
    <div className="suggest-page container-fluid">
      <div className="container-fluid detail-card scrollable">
        <h3>제안할 프로젝트 선택</h3>
        {projectList.map((project) => (
          <div
            key={project.projectId}
            className={`suggest-project ${
              selectedProject === project.projectId ? "selected" : ""
            }`}
            onClick={() => handleCardClick(project.projectId)}
            style={{ width: "inherit" }}
          >
            <div className="card-content">
              <h5>{project.projectName}</h5>
              <p>
                <strong>예상 금액</strong> {project.budget.toLocaleString()}원
                <span className="ml-3">
                  <strong>예상 기간</strong> {project.duration}일
                </span>
              </p>
              <p>
                <strong>근무 시작일</strong> {formatDate(project.registerDate)}
              </p>
              <p>
                <span className="location">
                  <i class="bi bi-geo-alt"></i> {project.locationName}
                </span>
              </p>
              <div className="skill-list">
                {project.skillNameList.map((skill, index) => (
                  <span key={index} className="skill-badge">
                    {<ProjectSkillTag text={skill} />}
                  </span>
                ))}
              </div>
            </div>
          </div>
        ))}
        {/* 제안하기 버튼 */}
        <div className="suggest-button-container">
          <button
            className={`suggest-button ${selectedProject ? "active" : ""}`}
            disabled={!selectedProject}
            onClick={handleSuggestClick}
          >
            제안하기
          </button>
        </div>
      </div>
    </div>
  );
};

export default FreelancerSuggest;
