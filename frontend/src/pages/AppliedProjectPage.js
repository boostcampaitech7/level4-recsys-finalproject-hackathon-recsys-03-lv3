import React, { useState, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import axios from "axios";
import SwitchButton from "../components/SwitchButton";
import SingleSelector from "../components/SingleSelector";
import ProjectInfo from "../components/ProjectInfo";
import "../style/AppliedProjectPage.css";

const API_BASE_URL = `${process.env.REACT_APP_BASE_URL}/api/mymony/applied-project`;
const freelancerId = sessionStorage.getItem("userId");

const AppliedProjectPage = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [sortOption, setSortOption] = useState("최신순");
  const [filterOption, setFilterOption] = useState("전체");
  const [showOnlyNotMatched, setShowOnlyUnreviewed] = useState(false);
  const [displayedProjects, setDisplayedProjects] = useState([]);

  useEffect(() => {
    const token = sessionStorage.getItem("token");

    if (!token) {
      setError("인증 토큰이 없습니다. 로그인 후 이용해주세요.");
      setLoading(false);
      return;
    }

    const fetchProjects = async () => {
      try {
        const response = await axios.get(API_BASE_URL, {
          headers: {
            Accept: "application/json",
            Authorization: `Bearer ${token}`,
          },
        });

        // 기존 프로젝트와 전달된 새 프로젝트를 함께 설정
        const newProject = location.state?.newProject;
        const updatedProjects = newProject
          ? [...response.data, newProject]
          : response.data;

        setProjects(updatedProjects);

        // location.state 초기화 (중복 추가 방지)
        if (newProject) {
          navigate("/applied", { replace: true, state: {} });
        }
      } catch (err) {
        console.error("기업 데이터를 불러오는 데 실패했습니다:", err);
        setError("기업 데이터를 불러오는 데 실패했습니다.");
      } finally {
        setLoading(false);
      }
    };

    fetchProjects();
  }, [freelancerId]);

  // 필터링 & 정렬 기능 적용
  useEffect(() => {
    let updatedProjects = [...projects];

    // 매칭 전 프로젝트만 보기 기능 적용
    if (showOnlyNotMatched) {
      updatedProjects = updatedProjects.filter(
        (project) => project.status === 0
      );
    }

    // 필터링 적용 (근무 형태: 전체 / 상주(0) / 원격(1))
    if (filterOption !== "전체") {
      const mappedValue = Number(filterOption); // "0" → 0, "1" → 1 변환
      updatedProjects = updatedProjects.filter(
        (project) => project.workType === mappedValue
      );
    }

    // 정렬 적용 (최신순 / 매칭 점수 높은순 / 금액 높은순)
    if (sortOption === "최신순") {
      updatedProjects.sort((a, b) =>
        b.registerDate.localeCompare(a.registerDate)
      );
    } else if (sortOption === "매칭 점수 높은순") {
      updatedProjects.sort(
        (a, b) => (b.matchingScore || 0) - (a.matchingScore || 0)
      );
    } else if (sortOption === "금액 높은순") {
      updatedProjects.sort((a, b) => Number(b.budget) - Number(a.budget));
    }

    setDisplayedProjects([...updatedProjects]);
  }, [sortOption, filterOption, showOnlyNotMatched, projects]); // 옵션(정렬/필터/스위치) 변경 시 실행

  if (loading) return <div>로딩 중...</div>;
  if (error) return <div className="error-message">{error}</div>;

  return (
    <div className="applied-project-page-container">
      <div className="header-container">
        <h3 className="header">신청한 프로젝트</h3>
        <p>총 {displayedProjects.length}개의 신청한 프로젝트가 있습니다.</p>
      </div>
      <div className="filters">
        <div className="filter-group-left">
          {/* 필터용 SingleSelector */}
          <SingleSelector
            title="근무 형태"
            options={["전체", "상주", "원격"]}
            onChange={(value) => {
              const mapping = { 전체: "전체", 상주: "0", 원격: "1" }; // 숫자가 아닌 문자열로 저장
              setFilterOption(mapping[value]);
            }}
          />
        </div>

        <div className="filter-group-right">
          {/* SwitchButton을 클릭하면 setShowOnlyUnreviewed 값 변경 */}
          <SwitchButton
            text="매칭 전 프로젝트만 표시"
            onChange={setShowOnlyUnreviewed}
          />

          {/* 정렬용 SingleSelector */}
          <SingleSelector
            title="정렬"
            options={["최신순", "매칭 점수 높은순", "금액 높은순"]}
            onChange={setSortOption}
          />
        </div>
      </div>

      <div className="project-list-container">
        {displayedProjects.map((project) => (
          <ProjectInfo
            onClick={() =>
              navigate("/project-detail", {
                state: { projectId: project.projectId },
              })
            }
            key={project.projectId}
            content={{
              projectName: project.projectName,
              skillNameList: project.skillNameList,
              locationName: project.locationName,
              registerDate: project.registerDate,
              duration: project.duration,
              budget: project.budget,
              categoryRole: "개발",
              categoryName: project.categoryName,
              status: project.status,
            }}
          />
          //<ProjectInfo key={project.projectName} content={project} />
        ))}
      </div>
    </div>
  );
};

export default AppliedProjectPage;
