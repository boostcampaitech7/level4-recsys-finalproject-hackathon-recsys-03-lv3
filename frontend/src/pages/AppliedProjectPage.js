import React, { useState, useEffect } from "react";
import SwitchButton from "../components/SwitchButton";
import SingleSelector from "../components/SingleSelector";
import ProjectInfo from "../components/ProjectInfo";
import "../style/AppliedProjectPage.css";

const AppliedProjectPage = () => {
  const [sortOption, setSortOption] = useState("최신순");
  const [filterOption, setFilterOption] = useState("전체");
  const [showOnlyNotMatched, setShowOnlyUnreviewed] = useState(false);
  const [displayedProjects, setDisplayedProjects] = useState([]);

  const [projects, setProjects] = useState([
    {
      projectID: 1,
      projectName: "기업-매칭 프리랜서 매칭 플랫폼 프론트엔드 개발",
      duration: 30,
      budget: 300000,
      workType: 0, // 근무 형태(상주: 0, 원격: 1), 필터링에 사용할 속성
      // contractType: ,
      status: 0, // 진행 상태(시작 전: 0, 진행 중: 1, 완료: 2)
      registerDate: "20250113",
      // endDate: "20250112",
      categoryRole: "개발",
      categoryName: "소프트웨어/IT", // 직군
      // skillIdList: ,
      skillNameList: ["React", "TypeScript", "Next.js"],
      locationName: "서울특별시 강남구",
      matchingScore: 80,
      applied: 1, // 지원 여부 (안함: 0, 함: 1)
      // isReviewed: ,
    },
    {
      projectID: 2,
      projectName: "AI Chatbot Development",
      duration: 30,
      budget: 4000000,
      workType: 1, // 근무형태(상주: 0, 원격: 1), 필터링에 사용할 속성
      // contractType: ,
      status: 2, // 진행상태(시작 전: 0, 진행 중: 1, 완료: 2)
      registerDate: "20241213",
      categoryName: "소프트웨어/IT",
      categoryRole: "개발",
      // skillIdList: ,
      skillNameList: ["Python", "Machine Learning", "Deep Learning"],
      locationName: "서울특별시 서초구",
      matchingScore: 90,
      applied: 0, // 지원 여부 (안함: 0, 함: 1)
      // isReviewed: ,
    },
  ]);

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

          {/* 정렬용 SingleSelector */}
          <SingleSelector
            title="정렬"
            options={["최신순", "매칭 점수 높은순", "금액 높은순"]}
            onChange={setSortOption}
          />

          {/* SwitchButton을 클릭하면 setShowOnlyUnreviewed 값 변경 */}
          <SwitchButton
            text="매칭 전 프로젝트만 표시"
            onChange={setShowOnlyUnreviewed}
          />
        </div>
      </div>

      <div className="project-list-container">
        {displayedProjects.map((project) => (
          <ProjectInfo key={project.projectName} content={project} />
        ))}
      </div>
    </div>
  );
};

export default AppliedProjectPage;
