import React, { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import axios from "axios";
import SimilarProject from "../components/SimilarProject";
import ProjectSkillTag from "../components/ProjectSkillTag";
import ProjectKeywordIcon from "../components/ProjectKeywordIcon";
import "../style/ProjectDetail.css";

const API_BASE_URL = `${process.env.REACT_APP_BASE_URL}/api/project`;

const ProjectDetailPage = () => {
  const location = useLocation();
  // const { projectId } = location.state || null;
  const projectId = 0;

  // 로그인 정보 상태(state) 저장
  const [token, setToken] = useState(
    sessionStorage.getItem("token") || localStorage.getItem("token")
  );
  const [userId, setUserId] = useState(
    sessionStorage.getItem("userId") || localStorage.getItem("userId")
  );
  const [userName, setUserName] = useState(
    sessionStorage.getItem("userName") || localStorage.getItem("userName")
  );
  const [userType, setUserType] = useState(
    sessionStorage.getItem("userType") || localStorage.getItem("userType")
  );
  const [project, setProject] = useState(null);
  const [similarProjects, setSimilarProjects] = useState(null);
  const [isApply, setIsApply] = useState(null);

  const headers = {
    Accept: "application/json",
    Authorization: `Bearer ${token}`,
  };

  useEffect(() => {
    const fetchProjectData = async () => {
      try {
        const [projectRes, similarProjectsRes] = await Promise.all([
          axios.get(`${API_BASE_URL}/${projectId}`, { headers }),
          axios.get(`${API_BASE_URL}/${projectId}/similar`, { headers }),
        ]);

        setProject(projectRes.data);
        console.log(project);
        setSimilarProjects(similarProjectsRes.data);
      } catch (error) {
        console.error("프로젝트 데이터를 불러오는 데 실패했습니다:", error);
      }
    };

    fetchProjectData();
  }, [projectId]);

  if (!project || !similarProjects) {
    return <div>로딩 중...</div>;
  }

  const handleApply = () => {
    try {
      axios.post(`${API_BASE_URL}/${projectId}/apply`, {}, { headers });
    } catch (err) {
      if (err.response && err.response.status === 409) {
        return { data: [] };
      }
      throw err;
    }
  };

  return (
    <div className="container2">
      <div className="left-card">
        <div className="project-container">
          <div className="status">
            {project.status === 0 ? (
              <ProjectKeywordIcon
                color="var(--color-secondary)"
                text="모집 중"
              />
            ) : (
              <ProjectKeywordIcon color="var(--color-star)" text="모집 완료" />
            )}
            {project.workType === 0 ? (
              <ProjectKeywordIcon color="var(--color-secondary)" text="상주" />
            ) : (
              <ProjectKeywordIcon color="var(--color-secondary)" text="원격" />
            )}
            <ProjectKeywordIcon color="var(--color-primary)" text="NEW" />
          </div>
          <div className="div-line">
            <h3 className="project-title">{project.projectName}</h3>
            <p className="category">{project.categoryName}</p>
          </div>
          <div className="project-info">
            <div className="info-item">
              <span className="info-label">예상 금액</span>{" "}
              <span className="budget">
                {project.budget.toLocaleString()}원
              </span>
              <span className="info-value">
                <i class="bi bi-geo-alt ps-3 pe-1"></i>
                {project.locationName}
              </span>
            </div>
            <div className="info-item">
              <span className="info-label">예상 기간</span>
              <span className="info-value">{project.duration}일</span>
            </div>
            <div className="info-item">
              <span className="info-label">시작 예정일</span>{" "}
              <span className="info-value">
                {project.registerDate.replace(
                  /(\d{4})(\d{2})(\d{2})/,
                  "$1년 $2월 $3일"
                )}
              </span>
            </div>
            <div>
              {project.skillNameList.map((skill, i) => (
                <ProjectSkillTag text={skill} />
              ))}
            </div>
          </div>
        </div>
        <div className="detail-section">
          <h3 className="projects-title">프로젝트 세부 내용</h3>
          <span className="detail-value">{project.projectContent}</span>
        </div>
      </div>
      <div className="right-cards">
        {userType === "0" ? (
          <div className="top-card">
            <div className="plzbold">
              <strong>지금 보는 프로젝트에 관심이 있나요?</strong>
            </div>
            <div className="plzblack">프로젝트에 지원해보세요!</div>
            <div className="button-container2">
              <button className="edit-button" onClick={handleApply}>
                지원하기
              </button>
            </div>
          </div>
        ) : (
          <></>
        )}
        <div className="bottom-card">
          <SimilarProject projects={similarProjects} />
        </div>
      </div>
    </div>
  );
};

export default ProjectDetailPage;
