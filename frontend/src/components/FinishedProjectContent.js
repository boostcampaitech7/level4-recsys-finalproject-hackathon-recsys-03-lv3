import React from "react";
import InfoCard from "./InfoCard";
import ProjectSkillTag from "./ProjectSkillTag";
import ScoreDisplay from "./ScoreDisplay";
import RadarChart from "./RadarChart";
import "../style/FinishedProjectContent.css";

const FinishedProjectContent = ({ content, onReview }) => {
  const {
    projectId,
    projectName,
    duration,
    budget,
    workType, // 근무 형태(상주: 0, 원격: 1)
    status, // 진행 상태(시작 전: 0, 진행 중: 1, 완료: 2)
    registerDate,
    endDate,
    categoryRole = "개발", // 직군
    categoryName,
    skillIdList,
    skillNameList,
    radarData,
    feedbackScore,
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
          <div className="title-section">
            <h3 className="project-title">{projectName}</h3>
            {isReviewed && (
              <div className="rating">
                <ScoreDisplay score={content.feedbackScore} />
              </div>
            )}
          </div>

          <div className="project-info-grid">
            <div className="project-info-left">
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
            <div className="project-info-right">
              {/* 금액 표시 (평가 후에만 보이도록) */}
              <p
                className={`finished-project-price ${isReviewed ? "visible" : ""}`}
              >
                {budget.toLocaleString()}원
              </p>
              <p>
                <strong>{categoryRole}</strong>
              </p>
              <p>{categoryName}</p>
            </div>
          </div>
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
              <div className="radar-chart">
                <RadarChart data={radarData ?? [0, 0, 0, 0, 0]} />
              </div>
            </>
          )}
        </div>
      </div>
      {feedbackContent && <p className="review-comment">"{feedbackContent}"</p>}
    </InfoCard>
  );
};

export default FinishedProjectContent;
