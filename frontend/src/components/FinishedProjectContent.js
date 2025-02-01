import React from "react";
import InfoCard from "./InfoCard";
import ProjectSkillTag from "./ProjectSkillTag";
import StarRating from "./StarRating";
import RadarChart from "./RadarChart";
import "../style/FinishedProjectContent.css";

const FinishedProjectContent = ({ content, onReview }) => {
  const {
    projectName,
    duration,
    registerDate,
    endDate,
    category = "개발",
    role,
    skillNameList = [],
    budget,
    radarData,
    feedbackContent,
    isReviewed, // 부모에서 직접 받은 값 사용
  } = content;

  return (
    <InfoCard>
      <div
        className={`finished-project-container ${isReviewed ? "review-mode" : ""}`}
      >
        {/* 왼쪽: 프로젝트 정보 */}
        <div className="left-section">
          <h3 className="finished-project-title">{projectName}</h3>

          {/* 금액 표시 (평가 후에만 보이도록) */}
          <p
            className={`finished-project-price ${isReviewed ? "visible" : ""}`}
          >
            <strong>금액:</strong> {budget.toLocaleString()}원
          </p>

          <div className="finished-project-info-grid">
            <div className="finished-project-info-left">
              <p>
                <strong>기간:</strong> {duration}일
              </p>
              <p>
                <strong>작업 시작일:</strong> {registerDate}
              </p>
              <p>
                <strong>작업 종료일:</strong> {endDate}
              </p>
            </div>
            <div className="finished-project-info-right">
              <p>
                <strong>{category}</strong>
              </p>
              <p>{role}</p>
              <div className="finished-skills">
                {skillNameList.length > 0 ? (
                  skillNameList.map((skill, index) => (
                    <ProjectSkillTag key={index} text={skill} />
                  ))
                ) : (
                  <span>스킬 정보 없음</span>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* 오른쪽: 평가 정보 */}
        <div className="right-section">
          {!isReviewed ? (
            <div className="before-review-container">
              <button
                className="review-button"
                onClick={onReview} // 부모에서 받은 함수 실행
              >
                평가하기
              </button>
              <p className="review-placeholder-text">
                평가를 완료하면 점수가 표시됩니다.
              </p>
            </div>
          ) : (
            <>
              <div className="rating">
                <StarRating />
              </div>
              <div className="radar-chart">
                <RadarChart data={radarData ?? [0, 0, 0, 0, 0]} />
              </div>
              {feedbackContent && (
                <p className="review-comment">"{feedbackContent}"</p>
              )}
            </>
          )}
        </div>
      </div>
    </InfoCard>
  );
};

export default FinishedProjectContent;
