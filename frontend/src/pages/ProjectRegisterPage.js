import React from "react";
import { useNavigate } from "react-router-dom";
import "../style/ProjectRegisterPage.css";
import botphoto from "../assets/chat_logo.png";
import { useLocation } from "react-router-dom";
import ProfileIcon from "../components/ProfileIcon";
import SimilarProject from "../components/SimilarProject";
import ProjectSkillTag from "../components/ProjectSkillTag";

const projectSummary = JSON.parse(
  sessionStorage.getItem("projectSummary") || "[]"
);

const similarProjects = [
  {
    projectId: 101,
    projectName: "Python 개발 프로젝트",
    duration: 30,
    budget: 5000000,
    workType: 1,
    contractType: 0,
    status: 0,
    registerDate: "20250125",
    categoryName: "IT•정보통신업",
    skillIdList: [1, 2, 3],
    skillNameList: ["Python", "Django", "API"],
    locationName: "서울특별시 강남구",
    similarityScore: 15,
  },
  {
    projectId: 102,
    projectName: "Java 백엔드 개발",
    duration: 60,
    budget: 10000000,
    workType: 0,
    contractType: 1,
    status: 0,
    registerDate: "20250120",
    categoryName: "IT•정보통신업",
    skillIdList: [4, 5, 6],
    skillNameList: ["Java", "Spring", "REST"],
    locationName: "서울특별시 서초구",
    similarityScore: 12,
  },
  {
    projectId: 101,
    projectName: "Python 개발 프로젝트",
    duration: 30,
    budget: 5000000,
    workType: 1,
    contractType: 0,
    status: 0,
    registerDate: "20250125",
    categoryName: "IT•정보통신업",
    skillIdList: [1, 2, 3],
    skillNameList: ["Python", "Django", "API"],
    locationName: "서울특별시 강남구",
    similarityScore: 15,
  },
];

const ProjectRegisterPage = () => {
  const location = useLocation();
  const { projectData } = location.state || {};
  const skillNameList = ["Java", "Spring", "REST"];
  const navigate = useNavigate();

  if (!projectData) {
    return <div>프로젝트 데이터가 없습니다. 다시 시도해주세요.</div>;
  }

  return (
    <div className="chat-page result">
      {/* Header */}
      <div className="chat-header">
        <span>새 프로젝트 등록</span>
      </div>

      {/* Chat Body */}
      <div className="chat-body">
        <div className="chat-bubble bot">
          <div className="chat-icon m-2">
            <ProfileIcon
              profileImage={botphoto}
              style={{
                width: "45px",
                height: "47px",
                margin: "0",
              }}
            />
          </div>
          <div className="chat-content bot">
            <div className="content-box">
              <p className="label">요청하신 프로젝트의 내용을 확인해주세요.</p>
              <table className="custom-table rounded-table">
                <tbody>
                  <tr>
                    <td className="table-label">프로젝트 명</td>
                    <td className="table-value">
                      {projectSummary.projectName || "미정"}
                    </td>
                  </tr>
                  <tr>
                    <td className="table-label">프로젝트 기간</td>
                    <td className="table-value">
                      {projectSummary.duration || "미정"}일
                    </td>
                  </tr>
                  <tr>
                    <td className="table-label">근무 형태</td>
                    <td className="table-value">
                      {projectSummary.workType === 0
                        ? "대면"
                        : "원격" || "미정"}
                    </td>
                  </tr>
                  <tr>
                    <td className="table-label">계약 유형</td>
                    <td className="table-value">
                      {projectSummary.contractType === 0
                        ? "월 단위"
                        : "프로젝트 단위" || "미정"}
                    </td>
                  </tr>
                  <tr>
                    <td className="table-label">계약 시 우선순위</td>
                    <td className="table-value">
                      {projectSummary.priority === 0
                        ? "스킬"
                        : projectSummary.priority === 1
                          ? "금액"
                          : "상관없음" || "미정"}
                    </td>
                  </tr>
                  <tr>
                    <td className="table-label">예상 금액</td>
                    <td className="table-value">
                      {projectSummary.expectedBudget || "미정"}원 /
                      {projectSummary.contractType === 0
                        ? "월"
                        : "프로젝트" || "월"}
                    </td>
                  </tr>
                  <tr>
                    <td className="table-label">프로젝트 세부내용</td>
                  </tr>
                  {/* Solar 결과 넣기 */}
                  <tr className="table-full-row">
                    <td colSpan="2" className="table-extra">
                      <span className="fw-bold">프로젝트 진행 상황:</span>
                      <p>
                        기획/디자인/개발환경 세팅이 완료된 상태입니다. 플랫폼의
                        ERD 및 개발 소스는 보유 중입니다.
                      </p>
                      <span className="fw-bold">주요 담당 업무:</span>
                      <p>
                        Java로 변환/구축하는 작업 수행, 초기에 개발 환경 조성 및
                        세팅 작업.
                      </p>
                      <span className="fw-bold">상세 업무 범위:</span>
                      <p>
                        기존 플랫폼의 언어 변환 작업, 유지보수 작업과 함께 MSSQL
                        서버 사용 예정.
                      </p>
                      <span className="fw-bold">기타 전달 사항:</span>
                      <p>
                        작업 최대한 빠르게 투입 가능한 분을 선정하고자 합니다.
                      </p>
                    </td>
                  </tr>
                </tbody>
              </table>
              <div className="register-btn-container">
                {/* 수정 필요 */}
                <button
                  className="register-btn btn-edit"
                  type="button"
                  id="sendRequest"
                  onClick={() => {
                    alert("요청이 완료되었습니다.");
                    window.location.reload(); //window.location.href = "https://example.com";
                  }}
                >
                  수정
                </button>
                <button
                  className="register-btn btn-confirm"
                  type="button"
                  id="sendRequest"
                  onClick={() => {
                    alert("요청이 완료되었습니다.");
                    navigate("/registered-projects");
                  }}
                >
                  등록
                </button>
              </div>
            </div>
          </div>
        </div>
        <div className="predict-things">
          <div className="predict-left">
            <SimilarProject projects={projectSummary.similarProjects} />
          </div>
          <div className="predict-right">
            <div className="predict-top">
              <h3 className="section-title">
                예상 견적 <span className="unit">(월 단위)</span>
              </h3>
              <p className="description">
                왼쪽 유사한 프로젝트 데이터를 바탕으로 AI가 분석한 예상
                견적입니다.
              </p>
              <div className="estimate-values">
                <div className="estimate-row">
                  <p className="estimate-label">기업의 예상 금액</p>
                  <p className="company-estimate">3,000,000원</p>
                </div>
                <div className="estimate-row">
                  <p className="estimate-label">AI의 예상 금액</p>
                  <p className="ai-estimate">{projectSummary.expectedBudget}</p>
                </div>
              </div>
              <div className="slider-container">
                <span className="min-value">
                  최저 {projectSummary.minBudget}
                </span>
                <input
                  type="range"
                  min="1000000"
                  max="4000000"
                  value="3000000"
                  readOnly
                />
                <span className="max-value">
                  최고 {projectSummary.maxBudget}
                </span>
              </div>
            </div>
            <div className="predict-bottom">
              <h3 className="section-title">예상 기술 요구사항</h3>
              <p className="description">
                왼쪽 유사한 프로젝트의 스킬을 바탕으로 AI가 분석한 예상 기술
                요구사항입니다.
              </p>
              <div className="skill-container">
                {projectSummary.simSkillNameList.map((skill, i) => (
                  <span key={i} className="badge">
                    <ProjectSkillTag text={skill} />
                  </span>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProjectRegisterPage;
