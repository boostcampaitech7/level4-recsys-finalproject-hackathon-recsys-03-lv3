import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

import ProjectSkillTag from "./ProjectSkillTag";

import "../style/FreelancerDetailPage.css";
import "../style/InfoCard.css";

const FreelancerSuggest = ({ isOpen, onClose, projectList }) => {
  const [selectedProject, setSelectedProject] = useState(null); // 선택된 프로젝트 ID 저장
  const navigate = useNavigate();

  const handleCardClick = (projectId) => {
    setSelectedProject(projectId); // 클릭한 카드 선택 (기존 선택된 카드 해제)
  };

  const handleSuggestClick = () => {
    if (selectedProject) {
      alert("제안이 완료되었습니다.");
      onClose(); // 팝업 닫기
      setTimeout(() => {
        navigate("/myproject");
      }, 10);
    }
  };

  const formatDate = (dateString) => {
    return dateString
      .replace(/(\d{4})(\d{2})(\d{2})/, "$1년 $2월 $3일")
      .replace(/\b0(\d)/g, "$1");
  };

  if (!isOpen) return null;

  return (
    <div className="popup-overlay">
      <div className="popup-content">
        <h3 className="history-header mb-3">제안할 프로젝트 선택</h3>
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
              <h5 className="sm-header mb-4">{project.projectName}</h5>
              <div className="history-info">
                <span className="info-label me-4">예상 금액</span>
                <span className="budget">
                  {" "}
                  {project.budget.toLocaleString()}원
                </span>
              </div>
              <span className="info-label me-3">근무 시작일</span>
              <span className="info-value">
                {formatDate(project.registerDate)} ({project.duration}일)
              </span>
              <p>
                <span className="info-label">
                  <i className="bi bi-geo-alt"></i> {project.locationName}
                </span>
              </p>
              {project.skillNameList.map((skill, index) => (
                <span key={index}>{<ProjectSkillTag text={skill} />}</span>
              ))}
            </div>
          </div>
        ))}

        {/* 제안하기 버튼 */}
        <div className="popup-actions">
          <button className="btnclose" onClick={onClose}>
            닫기
          </button>
          <button
            className={`btn-suggest ${selectedProject ? "active" : ""}`}
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
